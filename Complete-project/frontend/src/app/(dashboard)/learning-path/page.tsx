'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Compass, Sparkles, Clock, TrendingUp, RefreshCw, Lock } from 'lucide-react';
import Link from 'next/link';
import PremiumGate from '@/components/premium/PremiumGate';

export default function LearningPathPage() {
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userTier = (session?.user as any)?.tier;

  const [generated, setGenerated] = useState(false);

  const { data: recommendation, isLoading, refetch } = useQuery({
    queryKey: ['adaptive-path'],
    queryFn: () => api.adaptive.generate(apiKey),
    enabled: false,
  });

  const handleGenerate = async () => {
    await refetch();
    setGenerated(true);
  };

  const isPremium = userTier === 'premium' || userTier === 'pro';

  if (!isPremium) {
    return <PremiumGate featureName="Adaptive Learning Path" />;
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 rounded-xl" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  const path = recommendation?.data;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Adaptive Learning Path</h1>
        <p className="text-muted-foreground">
          Personalized study recommendations based on your performance
        </p>
      </div>

      {!generated || !path ? (
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6 text-center py-12">
            <Compass className="h-16 w-16 text-primary mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">
              Generate Your Learning Path
            </h2>
            <p className="text-muted-foreground mb-6">
              Get personalized chapter recommendations based on your strengths and weaknesses
            </p>
            <Button onClick={handleGenerate} size="lg">
              <Sparkles className="h-4 w-4 mr-2" />
              Generate My Learning Path
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Overview */}
          <Card className="bg-bg-surface border-border">
            <CardContent className="pt-6 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Your Personalized Plan</h2>
                <Button onClick={handleGenerate} variant="outline" size="sm">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
              </div>

              <p className="text-muted-foreground">{path.overall_assessment}</p>

              <div className="grid gap-4 md:grid-cols-3">
                <div className="p-4 rounded-lg bg-bg-elevated">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="h-4 w-4 text-success" />
                    <span className="text-sm font-medium">Strengths</span>
                  </div>
                  <ul className="space-y-1">
                    {path.strengths.map((strength, i) => (
                      <li key={i} className="text-sm text-muted-foreground">
                        • {strength}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-lg bg-bg-elevated">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="h-4 w-4 text-warning" />
                    <span className="text-sm font-medium">Areas to Improve</span>
                  </div>
                  <ul className="space-y-1">
                    {path.weak_areas.map((area, i) => (
                      <li key={i} className="text-sm text-muted-foreground">
                        • {area}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-lg bg-bg-elevated">
                  <div className="flex items-center gap-2 mb-2">
                    <Compass className="h-4 w-4 text-primary" />
                    <span className="text-sm font-medium">Daily Goal</span>
                  </div>
                  <p className="text-2xl font-bold text-primary">
                    {path.suggested_daily_minutes} min
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Recommended study time
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recommended Chapters */}
          <Card className="bg-bg-surface border-border">
            <CardContent className="pt-6">
              <h2 className="text-xl font-semibold mb-4">Recommended Chapters</h2>
              
              <div className="space-y-4">
                {path.recommended_chapters.map((chapter, index) => (
                  <div
                    key={chapter.chapter_id}
                    className="p-4 rounded-lg border border-border bg-bg-elevated"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-4 flex-1">
                        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold shrink-0">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold mb-1">{chapter.title}</h3>
                          <p className="text-sm text-muted-foreground mb-2">
                            {chapter.reason}
                          </p>
                          <div className="flex items-center gap-4 text-sm">
                            <div className="flex items-center gap-1 text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              {chapter.estimated_time} min
                            </div>
                            <Badge>Priority {chapter.priority}/5</Badge>
                          </div>
                        </div>
                      </div>
                      <Link href={`/course/${chapter.chapter_id}`}>
                        <Button>Start</Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
