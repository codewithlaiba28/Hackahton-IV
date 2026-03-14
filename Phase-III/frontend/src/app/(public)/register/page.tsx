'use client';

import { useState, useEffect } from 'react';
import { signIn, useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (status === 'authenticated') {
      router.push('/dashboard');
    }
  }, [status, router]);

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Checking session...</p>
        </div>
      </div>
    );
  }
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    tier: 'free',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // First, register the user via API
      await api.auth.register(formData.email, formData.password, formData.name, formData.tier);

      // Then, sign them in
      const result = await signIn('credentials', {
        email: formData.email,
        password: formData.password,
        redirect: false,
      });

      if (result?.error) {
        setError('Account created but sign in failed. Please try logging in.');
      } else {
        router.push('/dashboard');
        router.refresh();
      }
    } catch (err: any) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-bg-surface to-accent-secondary/10 px-4">
      <Card className="w-full max-w-md bg-bg-surface border-border">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Create an account</CardTitle>
          <CardDescription>
            Start your AI Agent Development journey today
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-destructive bg-destructive/10 border border-destructive rounded-md">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                disabled={isLoading}
                autoComplete="new-password"
              />
            </div>

            <div className="space-y-3">
              <Label>Select Tier</Label>
              <div className="grid grid-cols-2 gap-4">
                <div
                  onClick={() => setFormData({ ...formData, tier: 'free' })}
                  className={`cursor-pointer p-4 rounded-xl border-2 transition-all ${formData.tier === 'free'
                      ? 'border-primary bg-primary/5'
                      : 'border-white/5 bg-white/5 opacity-50'
                    }`}
                >
                  <p className="text-xs font-black uppercase tracking-tight text-white mb-1">Standard</p>
                  <p className="text-[10px] text-white/40 font-medium uppercase tracking-widest">Free Access</p>
                </div>
                <div
                  onClick={() => setFormData({ ...formData, tier: 'premium' })}
                  className={`cursor-pointer p-4 rounded-xl border-2 transition-all relative overflow-hidden ${formData.tier === 'premium'
                      ? 'border-accent bg-accent/5'
                      : 'border-white/5 bg-white/5 opacity-50'
                    }`}
                >
                  <div className="absolute top-0 right-0 p-1 bg-accent text-[8px] font-bold text-black uppercase tracking-tighter">Recommended</div>
                  <p className="text-xs font-black uppercase tracking-tight text-accent mb-1">Premium</p>
                  <p className="text-[10px] text-white/40 font-medium uppercase tracking-widest">Full Access</p>
                </div>
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-primary hover:bg-primary/90"
              disabled={isLoading}
            >
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Create Account
            </Button>
          </form>

          <div className="mt-4 text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <button
              onClick={() => router.push('/login')}
              className="text-primary hover:underline"
            >
              Sign in
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
