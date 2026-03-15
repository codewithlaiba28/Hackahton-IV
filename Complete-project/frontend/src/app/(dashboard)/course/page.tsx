'use client';

import { useSession } from 'next-auth/react';
import { useChapters } from '@/hooks/useChapters';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { BookOpen, Lock, CheckCircle, PlayCircle, Clock, TrendingUp, Sparkles, BrainCircuit } from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

const difficultyColors = {
  beginner: 'bg-success/10 text-success border-success/20',
  intermediate: 'bg-warning/10 text-warning border-warning/20',
  advanced: 'bg-error/10 text-error border-error/20',
};

export default function CoursePage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const { data: chaptersData, isLoading } = useChapters(apiKey);

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto space-y-8 p-6 animate-pulse">
        <Skeleton className="h-10 w-48 bg-white/5" />
        <div className="grid gap-6 md:grid-cols-2">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-48 rounded-2xl bg-white/5 border border-white/5" />
          ))}
        </div>
      </div>
    );
  }

  const chaptersResponse = chaptersData as any;
  const chapters = Array.isArray(chaptersResponse?.data?.chapters)
    ? chaptersResponse.data.chapters
    : [];

  return (
    <div className="max-w-7xl mx-auto space-y-10 py-6 px-4">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter mb-2">Knowledge <span className="text-primary">Architecture</span></h1>
        <p className="text-xs font-medium text-white/40 uppercase tracking-widest leading-loose">
          The structural blueprints for your evolution into an autonomous agent architect.
        </p>
      </motion.div>

      <div className="grid gap-6 md:grid-cols-2">
        {chapters.map((chapter: any, index: number) => {
          const isLocked = chapter.is_locked;
          const status = chapter.status || 'not_started';

          return (
            <motion.div
              key={chapter.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card
                className={`group relative bg-white/5 border-white/5 transition-all hover:border-primary/30 rounded-3xl overflow-hidden ${isLocked ? 'opacity-40 grayscale pointer-events-none' : ''
                  }`}
              >
                <div className="absolute top-0 right-0 p-8 opacity-[0.02] group-hover:opacity-10 transition-opacity">
                  <BrainCircuit className="w-24 h-24 text-primary" />
                </div>

                <CardContent className="p-8">
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                        <BookOpen className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <div className="text-[10px] font-black text-white/30 uppercase tracking-widest">
                          Chapter {chapter.sequence_order || index + 1}
                        </div>
                        <h3 className="text-lg font-black text-white uppercase tracking-tighter">{chapter.title}</h3>
                      </div>
                    </div>
                    <Badge className={`uppercase tracking-widest text-[8px] font-black h-5 px-2 rounded-md border ${difficultyColors[chapter.difficulty as keyof typeof difficultyColors] || difficultyColors.beginner}`}>
                      {chapter.difficulty}
                    </Badge>
                  </div>

                  <div className="flex items-center gap-6 mb-8 text-[10px] font-black uppercase tracking-widest text-white/40">
                    <div className="flex items-center gap-1.5">
                      <Clock className="h-3 w-3" />
                      {chapter.estimated_read_min || 0} MIN read
                    </div>
                    {status !== 'not_started' && (
                      <div className="flex items-center gap-1.5 text-primary">
                        <TrendingUp className="h-3 w-3" />
                        {chapter.quiz_score || 0}% quiz
                      </div>
                    )}
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {isLocked ? (
                        <div className="flex items-center gap-2 text-white/20">
                          <Lock className="h-3 w-3" />
                          <span className="text-[10px] font-black uppercase tracking-widest">LOCKED (PREMIUM)</span>
                        </div>
                      ) : status === 'completed' ? (
                        <div className="flex items-center gap-2 text-success">
                          <CheckCircle className="h-3 w-3" />
                          <span className="text-[10px] font-black uppercase tracking-widest">COMPLETED</span>
                        </div>
                      ) : status === 'in_progress' ? (
                        <div className="flex items-center gap-2 text-primary">
                          <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                          <span className="text-[10px] font-black uppercase tracking-widest">ACTIVE SESSION</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2 text-white/40">
                          <div className="w-1.5 h-1.5 rounded-full bg-white/10" />
                          <span className="text-[10px] font-black uppercase tracking-widest">READY FOR UPLINK</span>
                        </div>
                      )}
                    </div>

                    <Link href={`/course/${chapter.id}`}>
                      <Button size="sm" className={`h-10 px-6 rounded-xl font-black uppercase tracking-widest text-[9px] transition-all ${status === 'completed'
                        ? 'bg-white/5 border border-white/10 text-white/60 hover:bg-white/10'
                        : 'bg-primary text-primary-foreground hover:bg-primary/90 shadow-[0_0_15px_var(--color-primary)]'
                        }`}>
                        {status === 'completed' ? 'Review Log' : status === 'in_progress' ? 'Resume' : 'Initialize'}
                        {!isLocked && status !== 'completed' && <PlayCircle className="ml-2 h-3.5 w-3.5 fill-primary-foreground" />}
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {chapters.length === 0 && (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <BookOpen className="h-16 w-16 text-white/10 mb-6" />
          <h3 className="text-xl font-black text-white uppercase tracking-tighter mb-2">No Chapters Indexed</h3>
          <p className="text-white/40 text-sm font-medium uppercase tracking-wider">
            Curriculum data retrieval in progress. Checkout again lateral.
          </p>
        </div>
      )}
    </div>
  );
}
