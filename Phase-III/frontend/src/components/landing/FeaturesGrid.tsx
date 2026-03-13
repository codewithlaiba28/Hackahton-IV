'use client';

import { BookOpen, Route, MessageSquare, Award, TrendingUp, Lock } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { motion } from 'framer-motion';

const features = [
  {
    icon: BookOpen,
    title: 'Content Delivery',
    description: 'Access comprehensive AI Agent Development course content with clear explanations.',
  },
  {
    icon: Route,
    title: 'Smart Navigation',
    description: 'Navigate through chapters with intelligent sequencing and progress tracking.',
  },
  {
    icon: MessageSquare,
    title: 'Grounded Q&A',
    description: 'Get answers based on course content with AI-powered explanations.',
  },
  {
    icon: Award,
    title: 'Interactive Quizzes',
    description: 'Test your knowledge with instant feedback and detailed explanations.',
  },
  {
    icon: TrendingUp,
    title: 'Progress Tracking',
    description: 'Monitor your learning journey with detailed analytics and streaks.',
  },
  {
    icon: Lock,
    title: 'Freemium Access',
    description: 'Start free with chapters 1-3, upgrade for full course access.',
  },
];

export default function FeaturesGrid() {
  return (
    <section className="py-24 bg-background overflow-hidden">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            Everything You Need <span className="text-primary">to Succeed</span>
          </h2>
          <p className="text-lg text-muted-foreground/60 max-w-2xl mx-auto">
            Comprehensive learning platform designed for modern students and AI builders.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="bg-bg-surface/50 border-white/5 hover:border-primary/40 transition-all hover:bg-bg-surface group h-full">
                <CardContent className="pt-8 px-8">
                  <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    <feature.icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3 group-hover:text-primary transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground/60 leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
