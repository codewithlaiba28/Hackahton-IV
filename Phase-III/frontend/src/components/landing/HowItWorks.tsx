'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Rocket, Book, CheckSquare, Plus, Minus } from 'lucide-react';

const steps = [
  {
    title: 'Initialize Account',
    description: 'Create your digital profile in seconds and set your learning goals.',
    icon: Rocket,
  },
  {
    title: 'Execute Curriculum',
    description: 'Access the core modules and start your journey with AI-driven guidance.',
    icon: Book,
  },
  {
    title: 'Validate Knowledge',
    description: 'Synthesize what you have learned with socratic tests and quizzes.',
    icon: CheckSquare,
  },
];

export default function HowItWorks() {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <section className="py-24 bg-background relative" id="how-it-works">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent" />

      <div className="max-w-7xl mx-auto px-4 text-center">
        <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
          Master the <span className="text-primary">Workflow</span>
        </h2>
        <p className="text-lg text-muted-foreground/60 mb-16 max-w-2xl mx-auto">
          Start your AI learning journey with our data-driven three-step execution path.
        </p>

        <div className="grid md:grid-cols-3 gap-12 relative">
          {steps.map((step, index) => (
            <div key={index} className="relative z-10 group">
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-[60px] left-[calc(50%+60px)] w-[calc(100%-120px)] h-px bg-gradient-to-r from-primary via-primary/50 to-transparent opacity-20 group-hover:opacity-100 transition-opacity" />
              )}

              <motion.div
                className="flex flex-col items-center cursor-pointer px-4"
                onClick={() => setActiveStep(index)}
                whileHover={{ y: -5 }}
              >
                {/* Icon Circle */}
                <div className={`w-28 h-28 mb-8 rounded-3xl border transition-all duration-300 flex items-center justify-center ${activeStep === index
                    ? 'bg-primary/20 border-primary shadow-[0_0_30px_var(--color-primary)] opacity-40'
                    : 'bg-bg-surface border-white/10 hover:border-primary/30 opacity-70'
                  }`}>
                  <step.icon className={`w-10 h-10 ${activeStep === index ? 'text-primary' : 'text-white/40'}`} />
                </div>

                <h3 className={`text-xl font-bold mb-4 transition-colors ${activeStep === index ? 'text-primary' : 'text-white'}`}>
                  {step.title}
                </h3>

                <p className="text-muted-foreground/60 leading-relaxed max-w-xs">
                  {step.description}
                </p>

                <div className="mt-8">
                  <div className={`w-10 h-10 rounded-full border border-white/10 flex items-center justify-center transition-colors ${activeStep === index ? 'bg-primary text-primary-foreground' : 'text-white/40'}`}>
                    {activeStep === index ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                  </div>
                </div>

                <AnimatePresence>
                  {activeStep === index && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-6 p-6 bg-bg-surface/80 rounded-2xl border border-primary/20 backdrop-blur-sm"
                    >
                      <p className="text-sm text-primary/80 font-medium leading-relaxed">
                        Optimized with adaptive learning algorithms to ensure 100% retention rate.
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
