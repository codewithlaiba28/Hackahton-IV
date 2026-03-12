'use client';

import { useSession } from 'next-auth/react';
import { useChapters } from '@/hooks/useChapters';
import { useUIStore } from '@/store/useUIStore';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { BookOpen, Lock, CheckCircle, PlayCircle, Clock, TrendingUp } from 'lucide-react';
import Link from 'next/link';

const difficultyColors = {
  beginner: 'bg-success/10 text-success',
  intermediate: 'bg-warning/10 text-warning',
  advanced: 'bg-error/10 text-error',
};

export default function CoursePage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const { data: chaptersData, isLoading } = useChapters(apiKey);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid gap-4 md:grid-cols-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-48 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  const chapters = chaptersData?.data || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Course Curriculum</h1>
        <p className="text-muted-foreground">
          Master AI Agent Development with our comprehensive course
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {chapters.map((chapter, index) => {
          const isLocked = chapter.is_locked;
          const status = chapter.status || 'not_started';

          return (
            <Card
              key={chapter.id}
              className={`bg-bg-surface border-border transition-all hover:border-primary/50 ${
                isLocked ? 'opacity-60' : ''
              }`}
            >
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                      <BookOpen className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">
                        Chapter {chapter.sequence_order}
                      </div>
                      <h3 className="text-lg font-semibold">{chapter.title}</h3>
                    </div>
                  </div>
                  <Badge className={difficultyColors[chapter.difficulty]}>
                    {chapter.difficulty}
                  </Badge>
                </div>

                <div className="flex items-center gap-4 mb-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {chapter.estimated_read_time} min
                  </div>
                  {status !== 'not_started' && (
                    <div className="flex items-center gap-1">
                      <TrendingUp className="h-4 w-4" />
                      {chapter.quiz_score || 0}% quiz
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {isLocked ? (
                    <>
                      <Lock className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm text-muted-foreground">
                        Premium Only
                      </span>
                      <Button size="sm" variant="outline" className="ml-auto">
                        Upgrade
                      </Button>
                    </>
                  ) : status === 'completed' ? (
                    <Link href={`/course/${chapter.id}`} className="ml-auto">
                      <Button size="sm" variant="secondary">
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Review
                      </Button>
                    </Link>
                  ) : status === 'in_progress' ? (
                    <Link href={`/course/${chapter.id}`} className="ml-auto">
                      <Button size="sm">
                        <PlayCircle className="h-4 w-4 mr-2" />
                        Continue
                      </Button>
                    </Link>
                  ) : (
                    <Link href={`/course/${chapter.id}`} className="ml-auto">
                      <Button size="sm">
                        Start
                      </Button>
                    </Link>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {chapters.length === 0 && (
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6 text-center py-12">
            <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">No Chapters Available</h3>
            <p className="text-muted-foreground">
              Check back later for new content
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
