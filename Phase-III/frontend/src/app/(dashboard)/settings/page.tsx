'use client';

import { useSession } from 'next-auth/react';
import { useQuery } from '@tantml:function_calls';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { User, CreditCard, DollarSign, AlertTriangle } from 'lucide-react';
import { format } from 'date-fns';

export default function SettingsPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userTier = (session?.user as any)?.tier;

  const { data: costSummary, isLoading } = useQuery({
    queryKey: ['cost-summary'],
    queryFn: () => api.users.costSummary(apiKey),
    enabled: userTier === 'premium' || userTier === 'pro',
  });

  const tierColors = {
    free: 'bg-muted text-muted-foreground',
    premium: 'bg-primary text-primary-foreground',
    pro: 'bg-accent text-accent-foreground',
  };

  const tierBenefits = {
    free: ['Chapters 1-3', 'Basic quizzes', 'Progress tracking'],
    premium: ['All chapters', 'All quizzes', 'Progress analytics', 'Adaptive learning path'],
    pro: ['Everything in Premium', 'AI-graded assessments', 'Priority support', 'Team features'],
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account and subscription
        </p>
      </div>

      {/* Profile */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-6">
            <User className="h-5 w-5 text-muted-foreground" />
            <h2 className="text-xl font-semibold">Profile</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm text-muted-foreground mb-1 block">Name</label>
              <p className="font-medium">{session?.user?.name}</p>
            </div>
            <div>
              <label className="text-sm text-muted-foreground mb-1 block">Email</label>
              <p className="font-medium">{session?.user?.email}</p>
            </div>
            <div>
              <label className="text-sm text-muted-foreground mb-1 block">Member Since</label>
              <p className="font-medium">
                {new Date().toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Subscription */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-6">
            <CreditCard className="h-5 w-5 text-muted-foreground" />
            <h2 className="text-xl font-semibold">Subscription</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium mb-1">Current Plan</p>
                <p className="text-sm text-muted-foreground">
                  {tierBenefits[userTier]?.join(', ')}
                </p>
              </div>
              <Badge className={tierColors[userTier]}>
                {userTier?.toUpperCase()}
              </Badge>
            </div>

            {userTier === 'free' && (
              <Button className="w-full">
                Upgrade to Premium - $9.99/mo
              </Button>
            )}

            {userTier === 'premium' && (
              <Button variant="outline" className="w-full">
                Upgrade to Pro - $19.99/mo
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* LLM Usage (Premium Only) */}
      {(userTier === 'premium' || userTier === 'pro') && (
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-6">
              <DollarSign className="h-5 w-5 text-muted-foreground" />
              <h2 className="text-xl font-semibold">AI Usage This Month</h2>
            </div>

            {isLoading ? (
              <Skeleton className="h-32 rounded-lg" />
            ) : costSummary ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Total Cost</span>
                  <span className="text-2xl font-bold text-primary">
                    ${costSummary.total_cost_usd.toFixed(2)}
                  </span>
                </div>

                <div className="pt-4 border-t border-border">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-muted-foreground">Monthly Cap</span>
                    <span className="text-sm font-medium">${costSummary.monthly_cap.toFixed(2)}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Remaining</span>
                    <span className="text-sm font-medium text-success">
                      ${costSummary.remaining_budget.toFixed(2)}
                    </span>
                  </div>
                </div>

                {costSummary.feature_breakdown.map((feature, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between text-sm p-3 rounded-lg bg-bg-elevated"
                  >
                    <span>{feature.feature_name}</span>
                    <div className="text-right">
                      <div className="font-medium">{feature.calls} calls</div>
                      <div className="text-muted-foreground">
                        ${feature.cost_usd.toFixed(2)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted-foreground">No usage data available</p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Danger Zone */}
      <Card className="bg-bg-surface border-border border-error/50">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-6">
            <AlertTriangle className="h-5 w-5 text-error" />
            <h2 className="text-xl font-semibold text-error">Danger Zone</h2>
          </div>

          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <Button variant="destructive">
              Delete Account
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
