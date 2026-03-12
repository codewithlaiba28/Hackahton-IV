'use client';

import { useSession, signOut } from 'next-auth/react';
import { useUIStore } from '@/store/useUIStore';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Menu, LogOut, Flame } from 'lucide-react';

export default function Navbar() {
  const { data: session } = useSession();
  const { toggleSidebar } = useUIStore();

  const tierColors = {
    free: 'bg-muted text-muted-foreground',
    premium: 'bg-primary text-primary-foreground',
    pro: 'bg-accent text-accent-foreground',
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-bg-surface/95 backdrop-blur supports-[backdrop-filter]:bg-bg-surface/80">
      <div className="flex h-16 items-center px-4 gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
          className="shrink-0"
        >
          <Menu className="h-5 w-5" />
        </Button>

        <div className="flex-1" />

        <div className="flex items-center gap-4">
          {session && (
            <>
              <div className="hidden md:flex items-center gap-2">
                <Flame className="h-4 w-4 text-accent" />
                <span className="text-sm text-muted-foreground">0 day streak</span>
              </div>

              <Badge className={tierColors[session.user?.tier as keyof typeof tierColors] || tierColors.free}>
                {session.user?.tier?.toUpperCase() || 'FREE'}
              </Badge>

              <div className="flex items-center gap-2">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    {session.user?.name?.charAt(0) || 'U'}
                  </AvatarFallback>
                </Avatar>
                <span className="hidden md:block text-sm font-medium">
                  {session.user?.name}
                </span>
              </div>

              <Button
                variant="ghost"
                size="icon"
                onClick={() => signOut({ callbackUrl: '/' })}
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
