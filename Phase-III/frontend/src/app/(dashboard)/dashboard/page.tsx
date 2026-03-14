'use client';

import { useSession } from 'next-auth/react';
import { useProgress } from '@/hooks/useProgress';
import { useChapters } from '@/hooks/useChapters';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { BookOpen, Award, Clock, TrendingUp, Play, Zap, BrainCircuit, Target } from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;

  const { data: progressResponse, isLoading: progressLoading } = useProgress(userId, apiKey);
  const { data: chaptersData, isLoading: chaptersLoading } = useChapters(apiKey);

  const progress = progressResponse?.data;

  if (progressLoading || chaptersLoading) {
    return (
      <div className="space-y-8 animate-pulse p-4">
        <Skeleton className="h-10 w-64 bg-white/5" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-2xl bg-white/5 border border-white/5" />
          ))}
        </div>
        <Skeleton className="h-64 rounded-2xl bg-white/5 border border-white/5" />
      </div>
    );
  }

  const chapters = chaptersData?.data?.chapters || [];
  const nextChapter = (chapters as any[]).find((ch) => ch.status === 'in_progress') || chapters[0];

  const stats = [
    { label: 'Chapters Done', value: `${progress?.chapters_completed?.length || 0}/${progress?.total_chapters || 5}`, icon: BookOpen, color: 'text-primary', bg: 'bg-primary/10' },
    { label: 'Avg Quiz Score', value: `${progress?.best_quiz_score || 0}%`, icon: Award, color: 'text-accent', bg: 'bg-accent/10' },
    { label: 'Learning Time', value: `${Math.floor((progress?.total_study_time || 0) / 60)}H ${progress?.total_study_time ? (progress.total_study_time % 60) : 0}M`, icon: Clock, color: 'text-info', bg: 'bg-info/10' },
    { label: 'Mastery Level', value: `${progress?.overall_percentage || 0}%`, icon: TrendingUp, color: 'text-success', bg: 'bg-success/10' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-10 py-6 px-4">
      {/* Greeting */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative group"
      >
        <div className="absolute -inset-4 bg-primary/5 blur-3xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
        <h1 className="text-4xl font-black text-white tracking-tighter uppercase mb-2">
          Systems Online, <span className="text-primary">{session?.user?.name || 'Vanguard'}</span>
        </h1>
        <p className="text-sm font-medium text-white/40 tracking-wider uppercase">
          Ready to continue your evolution toward master agent?
        </p>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card className="bg-white/5 border-white/5 hover:border-primary/20 transition-all rounded-2xl overflow-hidden group">
              <CardContent className="pt-8 pb-8 px-6">
                <div className="flex items-center gap-5">
                  <div className={`p-4 ${stat.bg} rounded-2xl border border-white/5 group-hover:scale-110 transition-transform`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                  <div>
                    <p className="text-[10px] font-black text-white/30 uppercase tracking-widest mb-1">{stat.label}</p>
                    <p className="text-2xl font-black text-white tracking-tighter">{stat.value}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Continue Learning */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2"
        >
          {nextChapter ? (
            <Card className="bg-white/5 border-white/5 border-l-primary/30 border-l-4 rounded-2xl overflow-hidden relative">
              <div className="absolute top-0 right-0 p-8 opacity-5">
                <BrainCircuit className="w-32 h-32 text-primary" />
              </div>
              <CardContent className="p-8">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8 relative z-10">
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                      <span className="text-[10px] font-black text-primary uppercase tracking-widest">Active Module</span>
                    </div>
                    <h2 className="text-2xl font-black text-white tracking-tighter uppercase mb-2">{nextChapter.title}</h2>
                    <p className="text-xs text-white/40 font-medium">Estimated Completion: {nextChapter.estimated_read_time} Minutes</p>
                  </div>
                  <Link href={`/course/${nextChapter.id}`}>
                    <Button className="h-12 px-8 bg-primary hover:bg-primary/90 text-primary-foreground font-black uppercase tracking-widest text-xs rounded-xl shadow-[0_0_20px_var(--color-primary)] transition-all">
                      <Play className="h-4 w-4 mr-2 fill-primary-foreground" />
                      Resume Course
                    </Button>
                  </Link>
                </div>
                <div className="space-y-3 relative z-10">
                  <div className="flex items-center justify-between text-[10px] font-black uppercase tracking-widest text-white/50">
                    <span>Course Progress</span>
                    <span>{progress?.overall_percentage || 0}%</span>
                  </div>
                  <div className="h-3 bg-white/5 rounded-full overflow-hidden border border-white/5">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${progress?.overall_percentage || 0}%` }}
                      transition={{ duration: 1, ease: 'easeOut' }}
                      className="h-full bg-primary shadow-[0_0_10px_var(--color-primary)]"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="bg-white/5 border-white/5 rounded-2xl overflow-hidden h-full flex flex-col items-center justify-center p-12 text-center group">
              <div className="absolute -inset-10 bg-primary/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="relative z-10">
                <BookOpen className="h-16 w-16 text-white/20 mb-6 mx-auto" />
                <h3 className="text-xl font-black text-white uppercase tracking-tighter mb-4">Start Your Operation</h3>
                <p className="text-sm text-white/40 font-medium mb-8 max-w-xs mx-auto">
                  No active learning modules found. Initialize your first training sequence.
                </p>
                <Link href="/course">
                  <Button className="bg-white/5 border border-white/10 hover:border-primary/50 text-white font-black uppercase tracking-widest text-[10px] py-4 px-8 rounded-xl transition-all">
                    Browse Curriculum
                  </Button>
                </Link>
              </div>
            </Card>
          )}
        </motion.div>

        {/* Quick Actions / Goals */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card className="bg-white/5 border-white/5 rounded-2xl h-full flex flex-col p-8 bg-gradient-to-b from-white/5 to-transparent">
            <div className="flex items-center gap-3 mb-8">
              <Target className="w-5 h-5 text-accent" />
              <h3 className="text-xs font-black text-white uppercase tracking-widest">Target Goals</h3>
            </div>

            <div className="space-y-6 flex-1">
              {[
                { label: 'Complete Chapter 02', status: 'Pending', icon: Zap },
                { label: 'Pass AI Logic Quiz', status: 'Locked', icon: Target },
                { label: 'Master Prompt Engineering', status: 'In Progress', icon: BrainCircuit },
              ].map((goal, i) => (
                <div key={i} className="flex items-center gap-4 p-4 rounded-xl border border-white/5 hover:bg-white/5 transition-colors group cursor-default">
                  <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center border border-white/5 group-hover:border-primary/30 transition-colors">
                    <goal.icon className="w-4 h-4 text-white/40 group-hover:text-primary transition-colors" />
                  </div>
                  <div>
                    <h4 className="text-[10px] font-black text-white uppercase tracking-tight mb-1">{goal.label}</h4>
                    <span className="text-[9px] font-medium text-white/20 uppercase tracking-widest">{goal.status}</span>
                  </div>
                </div>
              ))}
            </div>

            <Button variant="ghost" className="mt-8 w-full border border-white/5 hover:bg-white/5 text-[10px] font-black uppercase tracking-widest text-white/40">
              Show All Goals
            </Button>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
