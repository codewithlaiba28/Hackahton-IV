'use client';

import { useSession } from 'next-auth/react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { User, CreditCard, DollarSign, AlertTriangle, Cpu, ShieldCheck, Zap } from 'lucide-react';
import { motion } from 'framer-motion';
import { useUIStore } from '@/store/useUIStore';
import { useUserProfile } from '@/hooks/useUser';

export default function SettingsPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const { data: userProfile } = useUserProfile();
  const { openUpgradeModal } = useUIStore();

  const userTier = userProfile?.tier || (session?.user as any)?.tier || 'free';

  const { data: costResponse, isLoading } = useQuery({
    queryKey: ['cost-summary'],
    queryFn: () => api.users.getCostSummary(apiKey),
    enabled: !!apiKey && (userTier === 'premium' || userTier === 'pro'),
  });

  const costSummary = (costResponse as any)?.data;

  const tierBenefits = {
    free: ['Chapters 1-3 Indexed', 'Basic Rule-Based Quizzes', 'Standard Progress Tracking'],
    premium: ['Complete Knowledge Archive', 'Adaptive Learning Engine', 'Priority Neural Sync'],
    pro: ['Agent Factory Access', 'LLM-Graded Assessments', 'Deep Feedback Loops', 'System Architect Status'],
  };

  const currentBenefits = tierBenefits[userTier as keyof typeof tierBenefits] || tierBenefits.free;

  return (
    <div className="max-w-4xl mx-auto space-y-10 py-6 px-4">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter mb-2">System <span className="text-primary">Configuration</span></h1>
        <p className="text-xs font-medium text-white/40 uppercase tracking-widest leading-loose">
          Calibrate your interface and subscription parameters.
        </p>
      </motion.div>

      {/* Identity Profile */}
      <Card className="bg-white/5 border-white/5 rounded-3xl overflow-hidden">
        <CardContent className="p-8">
          <div className="flex items-center gap-3 mb-8">
            <User className="h-5 w-5 text-primary" />
            <h2 className="text-xs font-black text-white uppercase tracking-widest">Identity Profile</h2>
          </div>

          <div className="grid gap-8 md:grid-cols-2">
            <div className="space-y-1">
              <label className="text-[10px] font-black text-white/20 uppercase tracking-widest">Subject Name</label>
              <p className="text-lg font-bold text-white uppercase tracking-tight">{session?.user?.name}</p>
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-black text-white/20 uppercase tracking-widest">Comms Channel</label>
              <p className="text-lg font-bold text-white/60">{session?.user?.email}</p>
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-black text-white/20 uppercase tracking-widest">Initialization Date</label>
              <p className="text-sm font-bold text-white/40 uppercase">March 12, 2026</p>
            </div>
            <div className="space-y-1">
              <label className="text-[10px] font-black text-white/20 uppercase tracking-widest">System API Key</label>
              <code className="text-[10px] bg-white/5 px-2 py-1 rounded-md text-primary font-mono select-all">
                {apiKey ? `${apiKey.substring(0, 8)}...${apiKey.substring(apiKey.length - 4)}` : 'UNKNOWN'}
              </code>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Subscription Tier */}
      <Card className="bg-white/5 border-white/5 rounded-3xl overflow-hidden relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent pointer-events-none" />
        <CardContent className="p-8">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <CreditCard className="h-5 w-5 text-primary" />
              <h2 className="text-xs font-black text-white uppercase tracking-widest">Tier Authorization</h2>
            </div>
            <Badge className={`px-4 py-1.5 rounded-xl font-black uppercase tracking-widest text-[10px] shadow-lg ${userTier === 'pro' ? 'bg-accent text-accent-foreground shadow-accent/20' :
              userTier === 'premium' ? 'bg-primary text-primary-foreground shadow-primary/20' :
                'bg-white/10 text-white/40'
              }`}>
              {userTier}
            </Badge>
          </div>

          <div className="space-y-6">
            <div className="grid gap-4 sm:grid-cols-2">
              {currentBenefits.map((benefit, i) => (
                <div key={i} className="flex items-center gap-3 text-sm font-medium text-white/60">
                  <ShieldCheck className="h-4 w-4 text-primary shrink-0" />
                  <span>{benefit}</span>
                </div>
              ))}
            </div>

            <div className="pt-6 border-t border-white/5 flex flex-col sm:flex-row gap-4">
              {userTier === 'free' && (
                <button
                  onClick={openUpgradeModal}
                  className="flex-1 h-14 bg-primary text-primary-foreground font-black uppercase tracking-widest text-xs rounded-2xl shadow-[0_0_20px_var(--color-primary)] hover:bg-primary/90 transition-all"
                >
                  Upgrade to Premium
                </button>
              )}
              {userTier !== 'pro' && (
                <Button variant="outline" className={`flex-1 h-14 border-accent/20 text-accent font-black uppercase tracking-widest text-xs rounded-2xl hover:bg-accent/10 ${userTier === 'free' ? 'opacity-50' : ''}`}>
                  Uplink to Pro
                </Button>
              )}
              <Button variant="ghost" className="text-white/20 text-[10px] font-black uppercase tracking-widest hover:text-white/40">
                Cancel Authorization
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Intelligence Usage Metrics */}
      {(userTier === 'premium' || userTier === 'pro') && (
        <Card className="bg-white/5 border-white/5 rounded-3xl overflow-hidden">
          <CardContent className="p-8">
            <div className="flex items-center justify-between mb-10">
              <div className="flex items-center gap-3">
                <Cpu className="h-5 w-5 text-accent" />
                <h2 className="text-xs font-black text-white uppercase tracking-widest">Intelligence Logistics</h2>
              </div>
              <div className="text-[10px] font-black text-white/20 uppercase tracking-widest">Cycle: March 2026</div>
            </div>

            {isLoading ? (
              <div className="space-y-4">
                <Skeleton className="h-20 rounded-2xl bg-white/5" />
                <Skeleton className="h-40 rounded-2xl bg-white/5" />
              </div>
            ) : costSummary ? (
              <div className="space-y-10">
                <div className="grid grid-cols-2 gap-8">
                  <div className="space-y-2">
                    <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Current Cost Accumulation</div>
                    <div className="text-5xl font-black text-white tracking-tighter">${costSummary.total_cost_usd.toFixed(2)}</div>
                  </div>
                  <div className="space-y-2 text-right">
                    <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">Residual Budget</div>
                    <div className="text-5xl font-black text-accent tracking-tighter">${costSummary.remaining_budget.toFixed(2)}</div>
                  </div>
                </div>

                <div className="relative h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(costSummary.total_cost_usd / costSummary.monthly_cap) * 100}%` }}
                    className="absolute inset-y-0 left-0 bg-primary shadow-[0_0_10px_var(--color-primary)]"
                  />
                </div>

                <div className="grid gap-4">
                  <div className="text-[10px] font-black text-white/20 uppercase tracking-widest mb-2">Feature Breakdown</div>
                  {costSummary.feature_breakdown.map((feature: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/5 group hover:border-primary/20 transition-all">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
                          <Zap className="h-5 w-5" />
                        </div>
                        <div>
                          <div className="text-xs font-black text-white uppercase tracking-tight">{feature.feature_name.replace(/_/g, ' ')}</div>
                          <div className="text-[10px] font-medium text-white/30 uppercase">{feature.calls} Neural Calls</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-black text-white">${feature.cost_usd.toFixed(4)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-white/20 uppercase tracking-widest text-[10px] font-black">
                No telemetry recorded for this cycle
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Security Overrides */}
      <Card className="bg-white/5 border-error/5 rounded-3xl overflow-hidden border">
        <CardContent className="p-8">
          <div className="flex items-center gap-3 mb-6">
            <AlertTriangle className="h-5 w-5 text-error" />
            <h2 className="text-xs font-black text-error uppercase tracking-widest">Security Overrides</h2>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
            <p className="text-[10px] font-medium text-white/40 uppercase tracking-wider max-w-sm">
              Account termination will result in the immediate and permanent erasure of all cognitive logs and progress data.
            </p>
            <Button variant="outline" className="h-12 border-error/20 text-error hover:bg-error/10 hover:text-error font-black uppercase tracking-widest text-[10px] rounded-xl px-8">
              Terminate Identity
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
