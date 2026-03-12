'use client';

import { usePathname } from 'next/navigation';
import { useUIStore } from '@/store/useUIStore';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  BookOpen,
  TrendingUp,
  Compass,
  Settings,
  Sparkles,
} from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/course', label: 'Course', icon: BookOpen },
  { href: '/progress', label: 'Progress', icon: TrendingUp },
  { href: '/learning-path', label: 'Learning Path', icon: Compass, premium: true },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { isSidebarOpen } = useUIStore();

  if (!isSidebarOpen) {
    return null;
  }

  return (
    <aside className="fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 border-r border-border bg-bg-surface transition-transform">
      <nav className="flex flex-col gap-1 p-4">
        {navItems.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              pathname === item.href
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            )}
          >
            <item.icon className="h-4 w-4" />
            <span>{item.label}</span>
            {item.premium && (
              <Sparkles className="ml-auto h-3 w-3 text-accent" />
            )}
          </a>
        ))}
      </nav>

      <div className="absolute bottom-4 left-4 right-4">
        <div className="rounded-lg border border-border bg-bg-elevated p-4">
          <h4 className="text-sm font-semibold mb-2">Upgrade to Premium</h4>
          <p className="text-xs text-muted-foreground mb-3">
            Get adaptive learning paths and AI-graded assessments
          </p>
          <button className="w-full text-xs bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90 transition-colors">
            Upgrade Now
          </button>
        </div>
      </div>
    </aside>
  );
}
