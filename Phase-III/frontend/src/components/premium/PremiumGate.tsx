'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Lock, Sparkles, CheckCircle } from 'lucide-react';

interface PremiumGateProps {
  featureName: string;
  onUpgrade?: () => void;
}

export default function PremiumGate({ featureName, onUpgrade }: PremiumGateProps) {
  const features = [
    'Adaptive learning paths',
    'AI-graded assessments',
    'Detailed progress analytics',
    'Priority support',
  ];

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <Card className="max-w-2xl bg-bg-surface border-border">
        <CardContent className="pt-6 text-center space-y-6">
          <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
            <Lock className="h-10 w-10 text-primary" />
          </div>

          <div>
            <h2 className="text-2xl font-bold mb-2">
              {featureName} is a Premium Feature
            </h2>
            <p className="text-muted-foreground">
              Upgrade to unlock this and other premium features
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4 text-left">
            {features.map((feature, index) => (
              <div key={index} className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-success" />
                <span className="text-sm">{feature}</span>
              </div>
            ))}
          </div>

          <div className="flex gap-4 justify-center pt-4">
            <Button
              onClick={onUpgrade}
              className="bg-primary hover:bg-primary/90"
              size="lg"
            >
              <Sparkles className="h-4 w-4 mr-2" />
              Upgrade to Premium - $9.99/mo
            </Button>
          </div>

          <p className="text-xs text-muted-foreground">
            Cancel anytime. No hidden fees.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
