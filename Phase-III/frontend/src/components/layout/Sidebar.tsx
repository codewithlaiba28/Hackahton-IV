'use client';

import { usePathname } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useUIStore } from '@/store/useUIStore';
import { useUserProfile } from '@/hooks/useUser';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  BookOpen,
  TrendingUp,
  Search,
  Compass,
  Settings,
  Sparkles,
  Zap,
} from 'lucide-react';
import { motion } from 'framer-motion';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/course', label: 'Course', icon: BookOpen },
  { href: '/progress', label: 'Progress', icon: TrendingUp },
  { href: '/search', label: 'Search', icon: Search },
  { href: '/learning-path', label: 'Learning Path', icon: Compass, premium: true },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { data: session } = useSession();
  const { isSidebarOpen, openUpgradeModal } = useUIStore();
  const { data: userProfile } = useUserProfile();

  const userTier = userProfile?.tier || (session?.user as any)?.tier || 'free';
  const isPremium = ['premium', 'pro'].includes(userTier.toLowerCase());

  if (!isSidebarOpen) {
    return null;
  }

  return (
    <aside className="fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 border-r border-white/5 bg-background transition-transform">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent pointer-events-none" />

      <nav className="relative z-10 flex flex-col gap-1.5 p-4 mt-4">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <a
              key={item.href}
              href={item.href}
              className={cn(
                'group relative flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition-all',
                isActive
                  ? 'bg-primary/10 text-primary'
                  : 'text-white/40 hover:bg-white/5 hover:text-white/80'
              )}
            >
              <item.icon className={cn('h-5 w-5 transition-transform group-hover:scale-110', isActive ? 'text-primary' : 'text-white/40')} />
              <span>{item.label}</span>
              {item.premium && (
                <Sparkles className="ml-auto h-3 w-3 text-primary animate-pulse" />
              )}
              {isActive && (
                <motion.div
                  layoutId="active-pill"
                  className="absolute left-0 w-1 h-6 bg-primary rounded-r-full shadow-[0_0_10px_var(--color-primary)]"
                />
              )}
            </a>
          );
        })}
      </nav>

      {!isPremium && (
        <div className="absolute bottom-6 left-6 right-6">
          <div className="relative rounded-2xl border border-primary/20 bg-primary/5 p-5 overflow-hidden group">
            <div className="absolute -top-8 -right-8 w-24 h-24 bg-primary/10 blur-2xl group-hover:bg-primary/20 transition-all" />
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <Zap className="w-4 h-4 text-primary fill-primary" />
                <h4 className="text-xs font-black text-white uppercase tracking-tighter">Pro Status</h4>
              </div>
              <p className="text-[10px] font-medium text-white/40 mb-4 leading-relaxed">
                Unlock adaptive learning paths and AI-graded assessments.
              </p>
              <button
                onClick={openUpgradeModal}
                className="w-full text-[10px] font-black uppercase tracking-widest bg-primary text-primary-foreground py-2.5 rounded-xl hover:bg-primary/90 transition-all shadow-[0_0_15px_var(--color-primary)]"
              >
                Upgrade Now
              </button>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
