'use client';

import { Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useRouter } from 'next/navigation';

export default function PricingPreview() {
  const router = useRouter();

  const plans = [
    {
      name: 'Free',
      price: '$0',
      description: 'Perfect for getting started',
      features: [
        'Chapters 1-3 access',
        'Basic quizzes',
        'Progress tracking',
        'ChatGPT tutoring',
      ],
      cta: 'Start Free',
      highlighted: false,
    },
    {
      name: 'Premium',
      price: '$9.99/mo',
      description: 'For serious learners',
      features: [
        'All 5 chapters access',
        'All quizzes & assessments',
        'Progress analytics',
        'Adaptive learning path',
        'AI-graded assessments',
        'Priority support',
      ],
      cta: 'Go Premium',
      highlighted: true,
    },
  ];

  return (
    <section className="py-20 bg-bg-surface">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-4">
          Simple, Transparent Pricing
        </h2>
        <p className="text-lg text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          Start free, upgrade when you're ready
        </p>
        
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan, index) => (
            <Card
              key={index}
              className={`bg-bg-elevated border-border ${
                plan.highlighted ? 'border-primary border-2' : ''
              }`}
            >
              <CardContent className="pt-6">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <div className="text-4xl font-bold text-primary mb-2">{plan.price}</div>
                  <p className="text-muted-foreground">{plan.description}</p>
                </div>
                
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-success" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <Button
                  className={`w-full ${
                    plan.highlighted
                      ? 'bg-primary hover:bg-primary/90'
                      : 'bg-muted hover:bg-muted/90'
                  }`}
                  onClick={() => router.push('/register')}
                >
                  {plan.cta}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
