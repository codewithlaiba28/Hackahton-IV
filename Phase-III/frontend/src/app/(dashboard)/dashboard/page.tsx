'use client';

import { useSession } from 'next-auth/react';
import { useProgress } from '@/hooks/useProgress';
import { useChapters } from '@/hooks/useChapters';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { BookOpen, Award, Clock, TrendingUp, Play } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;

  const { data: progress, isLoading: progressLoading } = useProgress(userId, apiKey);
  const { data: chaptersData, isLoading: chaptersLoading } = useChapters(apiKey);

  if (progressLoading || chaptersLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  const chapters = chaptersData?.data || [];
  const nextChapter = chapters.find((ch) => ch.status === 'in_progress') || chapters[0];

  return (
    <div className="space-y-6">
      {/* Greeting */}
      <div>
        <h1 className="text-3xl font-bold">
          Good morning, {session?.user?.name || 'Student'} 👋
        </h1>
        <p className="text-muted-foreground">
          Ready to continue your learning journey?
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <BookOpen className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Chapters Completed</p>
                <p className="text-2xl font-bold">
                  {progress?.chapters_completed || 0}/{progress?.total_chapters || 5}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-accent/10 rounded-full">
                <Award className="h-6 w-6 text-accent" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Best Quiz Score</p>
                <p className="text-2xl font-bold">{progress?.best_quiz_score || 0}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-info/10 rounded-full">
                <Clock className="h-6 w-6 text-info" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Study Time</p>
                <p className="text-2xl font-bold">
                  {Math.floor((progress?.total_study_time || 0) / 60)}h {progress?.total_study_time ? (progress.total_study_time % 60) : 0}m
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-success/10 rounded-full">
                <TrendingUp className="h-6 w-6 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Overall Progress</p>
                <p className="text-2xl font-bold">{progress?.overall_progress || 0}%</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Continue Learning */}
      {nextChapter && (
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Continue Learning</h2>
              <Link href={`/course/${nextChapter.id}`}>
                <Button className="bg-primary hover:bg-primary/90">
                  <Play className="h-4 w-4 mr-2" />
                  Continue
                </Button>
              </Link>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">{nextChapter.title}</span>
                <span className="text-sm text-muted-foreground">
                  {nextChapter.estimated_read_time} min read
                </span>
              </div>
              <Progress value={progress?.overall_progress || 0} className="h-2" />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Empty State */}
      {(!progress || progress.chapters_completed === 0) && (
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6 text-center py-12">
            <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Start Your Learning Journey</h3>
            <p className="text-muted-foreground mb-4">
              Complete your first chapter to see your progress
            </p>
            <Link href="/course">
              <Button className="bg-primary hover:bg-primary/90">
                Browse Chapters
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
