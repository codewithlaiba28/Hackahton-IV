'use client';

import { useSession } from 'next-auth/react';
import { useProgress } from '@/hooks/useProgress';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Progress } from '@/components/ui/progress';
import { BookOpen, Target, Trophy, Flame, Zap, Clock, TrendingUp, Award, Calendar } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { useUIStore } from '@/store/useUIStore';

export default function ProgressPage() {
  const router = useRouter();
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;
  const { openUpgradeModal } = useUIStore();

  const { data: progressResponse, isLoading } = useProgress(userId, apiKey);
  const progress = progressResponse?.data;

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto space-y-8 p-6 animate-pulse">
        <Skeleton className="h-10 w-48 bg-white/5" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-2xl bg-white/5 border border-white/5" />
          ))}
        </div>
        <Skeleton className="h-80 rounded-2xl bg-white/5 border border-white/5" />
      </div>
    );
  }

  if (!progress || (progress.chapters_completed?.length || 0) === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center">
        <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-6 border border-white/5">
          <BookOpen className="h-10 w-10 text-white/20" />
        </div>
        <h2 className="text-2xl font-black text-white uppercase tracking-tighter mb-2">No Uplink Established</h2>
        <p className="text-white/40 text-sm font-medium max-w-xs uppercase tracking-wider mb-8">
          Complete your first chapter to initialize progress systems.
        </p>
        {session?.user && (session.user as any).tier === 'free' && (
          <Button
            onClick={openUpgradeModal}
            className="bg-accent text-black font-bold uppercase tracking-widest px-8"
          >
            Upgrade Clearance
          </Button>
        )}
      </div>
    );
  }

  // Prepare chart data
  const chartData = (progress.daily_activity || [])
    .slice(-7)
    .map((activity) => ({
      date: new Date(activity.date).toLocaleDateString('en-US', {
        weekday: 'short',
      }),
      studyTime: Math.round(activity.study_time / 60), // Convert to hours
      chapters: activity.chapters_completed,
    }));

  const badges = [
    { name: 'First Quiz', icon: Target, earned: (progress.best_quiz_score || 0) > 0 },
    { name: '7-Day Streak', icon: Flame, earned: (progress.current_streak_days || 0) >= 7 },
    { name: 'First Chapter', icon: BookOpen, earned: (progress.chapters_completed?.length || 0) >= 1 },
    { name: 'Halfway There', icon: Zap, earned: (progress.chapters_completed?.length || 0) >= 3 },
    { name: 'Course Complete', icon: Trophy, earned: (progress.chapters_completed?.length || 0) >= 5 },
  ];

  const mainStats = [
    { label: 'Chapters', value: `${progress.chapters_completed?.length || 0}/${progress.total_chapters || 0}`, icon: BookOpen, color: 'text-primary', bg: 'bg-primary/10' },
    { label: 'Current Streak', value: `${progress.current_streak_days || 0} days`, icon: Flame, color: 'text-orange-500', bg: 'bg-orange-500/10' },
    { label: 'Best Score', value: `${progress.best_quiz_score || 0}%`, icon: Trophy, color: 'text-accent', bg: 'bg-accent/10' },
    { label: 'Study Time', value: `${Math.floor((progress.total_study_time || 0) / 60)}h ${(progress.total_study_time || 0) % 60}m`, icon: Clock, color: 'text-info', bg: 'bg-info/10' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-10 py-6 px-4">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter mb-2">Performance <span className="text-primary">Sync</span></h1>
        <p className="text-xs font-medium text-white/40 uppercase tracking-widest leading-loose">
          Real-time tracking of your cognitive development and course mastery.
        </p>
      </motion.div>

      {/* Stats Overview */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {mainStats.map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card className="bg-white/5 border-white/5 hover:border-primary/20 transition-all rounded-2xl overflow-hidden group">
              <CardContent className="pt-8 pb-8 px-6">
                <div className="flex items-center gap-5">
                  <div className={`p-4 ${stat.bg} rounded-2xl border border-white/5 transition-transform group-hover:scale-110`}>
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

      {/* Study Activity Chart */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4 }}
      >
        <Card className="bg-white/5 border-white/5 rounded-2xl overflow-hidden">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-10">
              <Calendar className="h-5 w-5 text-primary" />
              <h2 className="text-xs font-black text-white uppercase tracking-widest">Temporal Activity (Last 7 Cycles)</h2>
            </div>

            {chartData.length > 0 ? (
              <div className="h-[350px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid vertical={false} stroke="#ffffff05" strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      stroke="#ffffff20"
                      fontSize={10}
                      fontWeight={900}
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#ffffff40' }}
                    />
                    <YAxis
                      stroke="#ffffff20"
                      fontSize={10}
                      fontWeight={900}
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#ffffff40' }}
                    />
                    <Tooltip
                      cursor={{ fill: 'rgba(255,255,255,0.03)' }}
                      contentStyle={{
                        backgroundColor: '#0F0F0B',
                        border: '1px solid rgba(255,255,255,0.05)',
                        borderRadius: '12px',
                        boxShadow: '0 10px 30px rgba(0,0,0,0.5)'
                      }}
                      itemStyle={{ fontSize: '10px', fontWeight: '900', textTransform: 'uppercase' }}
                    />
                    <Bar dataKey="chapters" radius={[4, 4, 0, 0]} name="Chapters">
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill="#00E5B4" opacity={0.6 + (index / 10)} />
                      ))}
                    </Bar>
                    <Bar dataKey="studyTime" radius={[4, 4, 0, 0]} name="Hours">
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-study-${index}`} fill="#0066FF" opacity={0.6 + (index / 10)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="text-center py-12 text-white/20 uppercase tracking-widest text-[10px] font-black">
                Insufficient Data Logged
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Achievement Badges */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card className="bg-white/5 border-white/5 rounded-2xl overflow-hidden p-8">
          <div className="flex items-center gap-3 mb-10">
            <Award className="h-5 w-5 text-accent" />
            <h2 className="text-xs font-black text-white uppercase tracking-widest">Milestone Clearance</h2>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-6">
            {badges.map((badge, i) => (
              <div
                key={badge.name}
                className={`group relative p-6 rounded-2xl border text-center transition-all ${badge.earned
                  ? 'bg-primary/5 border-primary/20'
                  : 'bg-white/5 border-white/5 opacity-30 grayscale'
                  }`}
              >
                <div className={`w-14 h-14 mx-auto mb-4 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110 ${badge.earned ? 'bg-primary/10 border border-primary/20' : 'bg-white/5 border border-white/5'}`}>
                  <badge.icon className={`w-6 h-6 ${badge.earned ? 'text-primary' : 'text-white/40'}`} />
                </div>
                <p className="text-[10px] font-black text-white uppercase tracking-tight">{badge.name}</p>
                {!badge.earned && (
                  <p className="text-[8px] font-medium text-white/20 uppercase tracking-widest mt-1">Locked</p>
                )}
                {badge.earned && (
                  <div className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-primary shadow-[0_0_8px_var(--color-primary)]" />
                )}
              </div>
            ))}
          </div>
        </Card>
      </motion.div>
    </div>
  );
}
