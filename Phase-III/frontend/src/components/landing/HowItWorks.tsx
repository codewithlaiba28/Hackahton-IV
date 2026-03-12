'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const steps = [
  {
    title: 'Sign Up for Free',
    description: 'Create your account in seconds. No credit card required.',
    icon: '🚀',
  },
  {
    title: 'Start Learning',
    description: 'Access chapters 1-3 for free. Learn at your own pace with AI guidance.',
    icon: '📚',
  },
  {
    title: 'Test Yourself',
    description: 'Take quizzes to reinforce your knowledge and track progress.',
    icon: '✅',
  },
];

export default function HowItWorks() {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <section className="py-20 bg-bg-surface">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-4">
          How It Works
        </h2>
        <p className="text-lg text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          Start your AI learning journey in three simple steps
        </p>
        
        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-1/2 w-full h-0.5 bg-gradient-to-r from-primary/50 to-transparent" />
              )}
              
              <div
                className={`relative z-10 text-center cursor-pointer transition-all ${
                  activeStep === index ? 'scale-105' : ''
                }`}
                onClick={() => setActiveStep(index)}
              >
                {/* Icon Circle */}
                <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-4xl shadow-lg">
                  {step.icon}
                </div>
                
                {/* Title */}
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                
                {/* Description */}
                <p className="text-muted-foreground">{step.description}</p>
                
                {/* Expand Button */}
                <button className="mt-4 text-primary hover:text-primary/80 transition-colors">
                  {activeStep === index ? (
                    <ChevronUp className="h-5 w-5 mx-auto" />
                  ) : (
                    <ChevronDown className="h-5 w-5 mx-auto" />
                  )}
                </button>
                
                {/* Expanded Content */}
                {activeStep === index && (
                  <div className="mt-4 p-4 bg-bg-elevated rounded-lg border border-border animate-in fade-in slide-in-from-top-2">
                    <p className="text-sm text-muted-foreground">
                      This step includes personalized AI tutoring, interactive content, 
                      and progress tracking to ensure you master the material.
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
