'use client';

import { Card, CardContent } from '@/components/ui/card';
import { motion } from 'framer-motion';
import { Quote } from 'lucide-react';

const testimonials = [
  {
    name: 'Sarah Khan',
    role: 'Software Developer',
    content: 'This AI tutor helped me understand AI agents in just 2 weeks. The adaptive learning path is incredible!',
    avatar: 'SK',
  },
  {
    name: 'Ahmed Hassan',
    role: 'Computer Science Student',
    content: 'Finally, a platform that explains complex concepts in simple terms. The 24/7 availability is a game-changer.',
    avatar: 'AH',
  },
  {
    name: 'Emily Chen',
    role: 'Data Analyst',
    content: 'The quizzes and instant feedback helped me prepare for my AI certification. Highly recommend!',
    avatar: 'EC',
  },
];

export default function Testimonials() {
  return (
    <section className="py-24 bg-background overflow-hidden">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            Trusted by <span className="text-primary">Global Builders</span>
          </h2>
          <p className="text-lg text-muted-foreground/60 max-w-2xl mx-auto">
            Join thousands of students who have accelerated their careers with Course Companion.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="bg-bg-surface/50 border-white/5 transition-all hover:bg-bg-surface group h-full relative overflow-hidden">
                <Quote className="absolute -top-4 -right-4 w-24 h-24 text-primary opacity-[0.03] group-hover:opacity-[0.08] transition-opacity" />

                <CardContent className="pt-10 px-8 pb-10 flex flex-col h-full">
                  <p className="text-white/80 italic text-lg leading-relaxed mb-8 flex-1">
                    "{testimonial.content}"
                  </p>

                  <div className="flex items-center gap-4 border-t border-white/5 pt-8">
                    <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center text-primary font-bold">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <div className="font-bold text-white uppercase tracking-tight">{testimonial.name}</div>
                      <div className="text-xs text-muted-foreground/50 font-semibold">{testimonial.role}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
