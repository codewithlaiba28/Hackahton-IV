'use client';

import { useSession } from 'next-auth/react';
import { useProgress } from '@/hooks/useProgress';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Trophy, Flame, BookOpen, Award, Calendar } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function ProgressPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;

  const { data: progress, isLoading } = useProgress(userId, apiKey);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  if (!progress || progress.chapters_completed === 0) {
    return (
      <div className="text-center py-12">
        <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">No Progress Yet</h2>
        <p className="text-muted-foreground mb-4">
          Complete your first chapter to see your progress analytics
        </p>
      </div>
    );
  }

  // Prepare chart data
  const chartData = progress.daily_activity
    .slice(-7)
    .map((activity) => ({
      date: new Date(activity.date).toLocaleDateString('en-US', {
        weekday: 'short',
      }),
      studyTime: Math.round(activity.study_time / 60), // Convert to hours
      chapters: activity.chapters_completed,
    }));

  const badges = [
    { name: 'First Quiz', icon: '🎯', earned: progress.best_quiz_score > 0 },
    { name: '7-Day Streak', icon: '🔥', earned: progress.current_streak >= 7 },
    { name: 'First Chapter', icon: '📚', earned: progress.chapters_completed >= 1 },
    { name: 'Halfway There', icon: '⭐', earned: progress.chapters_completed >= 3 },
    { name: 'Course Complete', icon: '🏆', earned: progress.chapters_completed >= 5 },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
        <p className="text-muted-foreground">
          Track your learning journey and achievements
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <BookOpen className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Chapters</p>
                <p className="text-2xl font-bold">{progress.chapters_completed}/{progress.total_chapters}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-accent/10 rounded-full">
                <Flame className="h-6 w-6 text-accent" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Current Streak</p>
                <p className="text-2xl font-bold">{progress.current_streak} days</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-success/10 rounded-full">
                <Trophy className="h-6 w-6 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Best Score</p>
                <p className="text-2xl font-bold">{progress.best_quiz_score}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-info/10 rounded-full">
                <Award className="h-6 w-6 text-info" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Study Time</p>
                <p className="text-2xl font-bold">{Math.floor(progress.total_study_time / 60)}h {progress.total_study_time % 60}m</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Study Activity Chart */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-6">
            <Calendar className="h-5 w-5 text-muted-foreground" />
            <h2 className="text-xl font-semibold">Study Activity (Last 7 Days)</h2>
          </div>
          
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="date" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#111',
                    border: '1px solid #2A2A2A',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="chapters" fill="#00E5B4" name="Chapters" />
                <Bar dataKey="studyTime" fill="#0066FF" name="Study Time (hrs)" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center py-12 text-muted-foreground">
              No activity data yet
            </div>
          )}
        </CardContent>
      </Card>

      {/* Achievement Badges */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-6">
            <Award className="h-5 w-5 text-muted-foreground" />
            <h2 className="text-xl font-semibold">Achievements</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {badges.map((badge) => (
              <div
                key={badge.name}
                className={`p-4 rounded-lg border text-center transition-all ${
                  badge.earned
                    ? 'bg-primary/10 border-primary'
                    : 'bg-bg-elevated border-border opacity-50'
                }`}
              >
                <div className="text-4xl mb-2">{badge.icon}</div>
                <p className="text-sm font-medium">{badge.name}</p>
                {!badge.earned && (
                  <p className="text-xs text-muted-foreground mt-1">Locked</p>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
