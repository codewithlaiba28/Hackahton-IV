'use client';

import { useState } from 'react';
import { Check, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function PricingPreview() {
  const router = useRouter();
  const [selectedPlan, setSelectedPlan] = useState('Premium');

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
    },
    {
      name: 'Premium',
      price: '$9.99',
      unit: '/mo',
      description: 'For serious AI builders',
      features: [
        'All 5 chapters access',
        'Advanced written tests',
        'Learning analytics',
        'Adaptive study path',
        'AI Mentor access',
        'Priority support',
      ],
      cta: 'Go Premium',
    },
  ];

  return (
    <section className="py-24 bg-background relative overflow-hidden">
      <div className="absolute top-1/2 left-0 w-full h-[500px] bg-primary/5 blur-[120px] -translate-y-1/2 pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            Simple, Transparent <span className="text-primary">Pricing</span>
          </h2>
          <p className="text-lg text-muted-foreground/60 max-w-2xl mx-auto">
            Unlock the power of Digital FTE tutoring with our flexible tiers.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => {
            const isHighlighted = selectedPlan === plan.name;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                onClick={() => setSelectedPlan(plan.name)}
                className="cursor-pointer h-full"
              >
                <Card
                  className={`bg-bg-surface/80 backdrop-blur-sm border-white/5 transition-all overflow-hidden relative h-full flex flex-col ${isHighlighted ? 'ring-2 ring-primary shadow-[0_0_40px_rgba(0,245,212,0.15)] scale-[1.02] z-10' : 'hover:border-white/20'
                    }`}
                >
                  {plan.name === 'Premium' && isHighlighted && (
                    <div className="absolute top-0 right-0 bg-primary text-primary-foreground px-4 py-1 text-[10px] font-black uppercase tracking-tighter rounded-bl-xl">
                      MOST POPULAR
                    </div>
                  )}
                  {plan.name === 'Free' && isHighlighted && (
                    <div className="absolute top-0 right-0 bg-primary text-primary-foreground px-4 py-1 text-[10px] font-black uppercase tracking-tighter rounded-bl-xl">
                      SELECTED
                    </div>
                  )}

                  <CardContent className="pt-12 p-8 flex flex-col flex-grow">
                    <div className="mb-8">
                      <h3 className="text-xl font-bold text-white mb-2 uppercase tracking-widest">{plan.name}</h3>
                      <div className="flex items-baseline gap-1">
                        <span className="text-5xl font-black text-white">{plan.price}</span>
                        {plan.unit && <span className="text-muted-foreground/60 font-medium">{plan.unit}</span>}
                      </div>
                      <p className="text-sm text-muted-foreground/60 mt-4">{plan.description}</p>
                    </div>

                    <div className="h-px bg-white/5 w-full mb-8" />

                    <ul className="space-y-4 mb-10 flex-grow">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-center gap-3">
                          <div className="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                            <Check className="h-3 w-3 text-primary" />
                          </div>
                          <span className="text-sm text-white/70">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <Button
                      className={`w-full h-14 rounded-2xl font-bold transition-all mt-auto ${isHighlighted
                        ? 'bg-primary hover:bg-primary/90 text-primary-foreground shadow-[0_0_20px_var(--color-primary)] hover:text-primary-foreground'
                        : 'bg-white/5 hover:bg-white/10 text-white hover:text-white'
                        }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        router.push('/register');
                      }}
                    >
                      {isHighlighted && <Sparkles className="w-4 h-4 mr-2" />}
                      {plan.cta}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
