'use client';

import { useRouter } from 'next/navigation';
import { useSession, signOut } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import {
  Sparkles,
  ArrowRight,
  Zap,
  Bot,
  Cpu,
  Layers,
  LogOut,
  LayoutDashboard
} from 'lucide-react';
import Link from 'next/link';

export default function Hero() {
  const router = useRouter();
  const { data: session, status } = useSession();

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden bg-background pt-32 pb-24">
      {/* Navigation Bar */}
      <div className="absolute top-0 left-0 right-0 z-50 p-6 flex justify-between items-center max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-[0_0_15px_rgba(var(--primary),0.5)]">
            <Bot className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold text-white tracking-tighter">Companion<span className="text-primary">FTE</span></span>
        </div>

        <div className="flex items-center gap-4">
          {status === 'loading' ? (
            <div className="w-20 h-8 animate-pulse bg-white/5 rounded-lg" />
          ) : session ? (
            <>
              <Button
                variant="ghost"
                className="text-white/70 hover:text-white hover:bg-white/5 font-semibold"
                onClick={() => router.push('/dashboard')}
              >
                <LayoutDashboard className="w-4 h-4 mr-2" />
                Dashboard
              </Button>
              <Button
                variant="outline"
                className="border-white/10 text-white hover:bg-white/5 font-semibold rounded-xl"
                onClick={() => signOut({ callbackUrl: '/' })}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button
                variant="ghost"
                className="text-white/70 hover:text-white hover:bg-white/5 font-semibold"
                onClick={() => router.push('/login')}
              >
                Sign In
              </Button>
              <Button
                className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold rounded-xl shadow-[0_0_10px_rgba(var(--primary),0.3)] transition-all"
                onClick={() => router.push('/register')}
              >
                Sign Up
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Background Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary/10 rounded-[100%] blur-[120px] pointer-events-none" />

      {/* Horizon Line Effect */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[1200px] h-[300px] bg-primary/5 rounded-[100%] blur-[80px] pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-5xl mx-auto flex flex-col items-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold mb-8"
        >
          <Sparkles className="w-3 h-3" />
          <span>Building the Future of Education</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-6xl md:text-8xl font-black tracking-tight text-white mb-8 leading-[1.1]"
        >
          Fueling the Future <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary/60">
            One Agent at a Time
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-xl md:text-2xl text-muted-foreground/80 mb-12 max-w-3xl mx-auto font-medium"
        >
          Course Companion FTE is the world's most advanced educational platform designed to
          accelerate your AI journey. 168 hours of tutoring, 90% cost savings.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-6 justify-center"
        >
          <Button
            size="lg"
            className="h-14 px-8 bg-primary hover:bg-primary/90 text-primary-foreground hover:text-primary-foreground font-bold rounded-xl shadow-[0_0_15px_var(--color-primary)] transition-all hover:scale-105"
            onClick={() => router.push(session ? '/dashboard' : '/register')}
          >
            {session ? 'Go to Dashboard' : 'Start Learning Free'}
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="h-14 px-8 border-white/10 text-white hover:bg-white/5 hover:text-white font-semibold rounded-xl"
            onClick={() => {
              const el = document.getElementById('how-it-works');
              el?.scrollIntoView({ behavior: 'smooth' });
            }}
          >
            See Our Tech Stack
          </Button>
        </motion.div>

        {/* Tech Partner Icons Mockup */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
          className="mt-24 flex flex-wrap justify-center items-center gap-12 opacity-40 hover:opacity-100 transition-opacity"
        >
          <div className="flex items-center gap-2"><Cpu className="w-5 h-5" /> <span className="text-sm font-semibold">FastAPI</span></div>
          <div className="flex items-center gap-2"><Layers className="w-5 h-5" /> <span className="text-sm font-semibold">Next.js</span></div>
          <div className="flex items-center gap-2"><Bot className="w-5 h-5" /> <span className="text-sm font-semibold">OpenAI</span></div>
          <div className="flex items-center gap-2"><Zap className="w-5 h-5" /> <span className="text-sm font-semibold">Claude</span></div>
        </motion.div>
      </div>
    </section>
  );
}
