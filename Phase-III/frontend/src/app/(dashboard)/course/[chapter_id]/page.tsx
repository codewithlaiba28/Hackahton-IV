'use client';

import { useParams, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useChapter } from '@/hooks/useChapters';
import { useUpdateProgress } from '@/hooks/useProgress';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { CheckCircle, ArrowLeft, ArrowRight, BookOpen, Clock } from 'lucide-react';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/atom-one-dark.css';

export default function ChapterReaderPage() {
  const params = useParams();
  const router = useRouter();
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const userId = (session?.user as any)?.id;

  const { data: chapterResponse, isLoading } = useChapter(params.chapter_id as string, apiKey);
  const updateProgress = useUpdateProgress();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-96 rounded-xl" />
      </div>
    );
  }

  const chapter = chapterResponse?.data;

  if (!chapter) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-2">Chapter Not Found</h2>
        <Link href="/course">
          <Button variant="outline">Back to Course</Button>
        </Link>
      </div>
    );
  }

  const handleMarkComplete = async () => {
    if (!userId) return;

    await updateProgress.mutateAsync({
      userId,
      chapterId: chapter.id,
      status: 'completed',
      apiKey,
    });

    router.push(`/course/${chapter.id}/quiz`);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Link href="/course">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Course
          </Button>
        </Link>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <BookOpen className="h-4 w-4" />
          Chapter {chapter.sequence_order}
        </div>
      </div>

      {/* Header */}
      <div className="space-y-4">
        <h1 className="text-4xl font-bold">{chapter.title}</h1>
        <div className="flex items-center gap-4 text-muted-foreground">
          <div className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {chapter.estimated_read_min || 0} min read
          </div>
          <span className={`px-2 py-1 rounded text-xs ${chapter.difficulty === 'beginner' ? 'bg-success/10 text-success' :
            chapter.difficulty === 'intermediate' ? 'bg-warning/10 text-warning' :
              'bg-error/10 text-error'
            }`}>
            {chapter.difficulty}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="prose prose-invert prose-lg max-w-none bg-bg-surface rounded-xl p-8 border border-border">
        <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
          {chapter.content}
        </ReactMarkdown>
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between pt-8 border-t border-border">
        {chapter.prev_chapter_id ? (
          <Link href={`/course/${chapter.prev_chapter_id}`}>
            <Button variant="outline">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Previous Chapter
            </Button>
          </Link>
        ) : (
          <div />
        )}

        {chapter.next_chapter_id ? (
          <Link href={`/course/${chapter.next_chapter_id}`}>
            <Button>
              Next Chapter
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </Link>
        ) : (
          <Button onClick={handleMarkComplete}>
            <CheckCircle className="h-4 w-4 mr-2" />
            Mark as Complete
          </Button>
        )}
      </div>
    </div>
  );
}
