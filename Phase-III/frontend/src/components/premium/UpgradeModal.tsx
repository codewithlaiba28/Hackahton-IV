'use client';

import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { CheckCircle } from 'lucide-react';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpgrade: () => void;
  isLoading?: boolean;
}

const premiumFeatures = [
  'Access to all 5 chapters',
  'AI-graded assessments',
  'Adaptive learning paths',
  'Detailed progress analytics',
  'Priority support',
  'Certificate of completion',
];

export default function UpgradeModal({ isOpen, onClose, onUpgrade, isLoading }: UpgradeModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-bg-surface border-border">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-center">
            Upgrade to Premium
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="text-center">
            <div className="text-5xl font-bold text-primary mb-2">$9.99</div>
            <p className="text-muted-foreground">per month</p>
          </div>

          <div className="space-y-3">
            {premiumFeatures.map((feature, index) => (
              <div key={index} className="flex items-center gap-3">
                <CheckCircle className="h-5 w-5 text-success shrink-0" />
                <span>{feature}</span>
              </div>
            ))}
          </div>

          <div className="flex gap-4 pt-4">
            <Button
              onClick={onClose}
              variant="outline"
              className="flex-1"
            >
              Maybe Later
            </Button>
            <Button
              onClick={onUpgrade}
              disabled={isLoading}
              className="flex-1 bg-primary hover:bg-primary/90"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                  <span>Upgrading...</span>
                </div>
              ) : (
                'Upgrade Now'
              )}
            </Button>
          </div>

          <p className="text-xs text-center text-muted-foreground">
            Cancel anytime. 7-day free trial available.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
