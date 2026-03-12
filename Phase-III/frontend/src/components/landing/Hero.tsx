'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';

export default function Hero() {
  const router = useRouter();

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-gradient-to-br from-background via-bg-surface to-accent-secondary/10">
      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary mb-6">
          Your AI Tutor for AI Agent Development
        </h1>
        
        <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
          24/7 personalized tutoring, adaptive learning paths, and instant feedback — powered by AI.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button 
            size="lg" 
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold"
            onClick={() => router.push('/register')}
          >
            Start Learning Free
          </Button>
          <Button 
            size="lg" 
            variant="outline"
            className="border-secondary text-secondary hover:bg-secondary/10"
          >
            See How It Works
          </Button>
        </div>
      </div>
    </section>
  );
}
