'use client';

import { useSession, signOut } from 'next-auth/react';
import { useUIStore } from '@/store/useUIStore';
import { useProgress } from '@/hooks/useProgress';
import { useUserProfile } from '@/hooks/useUser';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Menu, LogOut, Flame, Sparkles, Home } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function Navbar() {
  const { data: session } = useSession();
  const { toggleSidebar } = useUIStore();

  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;
  const { data: progressResponse } = useProgress(userId, apiKey);
  const { data: userProfile } = useUserProfile();

  const userTier = userProfile?.tier || (session?.user as any)?.tier || 'free';
  const streak = progressResponse?.data?.current_streak_days || 0;

  const tierStyles = {
    free: 'border-white/10 bg-white/5 text-white/60',
    premium: 'border-primary/50 bg-primary/10 text-primary shadow-[0_0_10px_var(--color-primary)]',
    pro: 'border-accent/50 bg-accent/10 text-accent shadow-[0_0_10px_var(--color-accent)]',
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/5 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-6 gap-4">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="shrink-0 hover:bg-white/5 text-white/70"
          >
            <Menu className="h-5 w-5" />
          </Button>

          <Link href="/" className="flex items-center gap-2 select-none hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30">
              <Sparkles className="w-4 h-4 text-primary" />
            </div>
            <span className="hidden md:block font-black text-white tracking-tighter uppercase text-sm">
              Course <span className="text-primary">Companion</span>
            </span>
          </Link>
        </div>

        <div className="flex-1" />

        <div className="flex items-center gap-3 md:gap-6">
          <Link href="/">
            <Button
              variant="ghost"
              size="sm"
              className="hidden sm:flex items-center gap-2 text-white/60 hover:text-white hover:bg-white/5"
            >
              <Home className="h-4 w-4" />
              <span>Landing Page</span>
            </Button>
          </Link>

          {session && (
            <>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5"
              >
                <Flame className="h-4 w-4 text-orange-500 fill-orange-500" />
                <span className="text-xs font-bold text-white/80">{streak} DAY STREAK</span>
              </motion.div>

              <Badge
                className={`py-1 px-3 h-auto uppercase tracking-widest text-[10px] font-black rounded-lg border transition-all ${tierStyles[userTier as keyof typeof tierStyles] || tierStyles.free
                  }`}
              >
                {userTier}
              </Badge>

              <div className="flex items-center gap-3 pl-4 border-l border-white/5">
                <div className="text-right hidden sm:block">
                  <div className="text-xs font-black text-white leading-none uppercase">{session.user?.name}</div>
                  <div className="text-[10px] font-medium text-white/40 leading-none mt-1">Student ID: #7721</div>
                </div>
                <Avatar className="h-9 w-9 border border-white/10 ring-1 ring-white/5">
                  <AvatarFallback className="bg-primary/20 text-white text-xs font-black">
                    {session.user?.name?.charAt(0).toUpperCase() || 'U'}
                  </AvatarFallback>
                </Avatar>
              </div>

              <Button
                variant="ghost"
                size="icon"
                onClick={() => signOut({ callbackUrl: '/' })}
                className="hover:bg-destructive/10 hover:text-destructive text-white/40 ml-2"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
