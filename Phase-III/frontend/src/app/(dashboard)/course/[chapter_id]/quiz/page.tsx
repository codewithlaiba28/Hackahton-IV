'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useQuiz, useSubmitQuiz } from '@/hooks/useQuiz';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Clock, CheckCircle, XCircle, Trophy, ArrowRight, Sparkles } from 'lucide-react';
import QuizResults from '@/components/quiz/QuizResults';
import { useUIStore } from '@/store/useUIStore';

type QuizState = 'start' | 'taking' | 'submitting' | 'results';

export default function QuizPage() {
  const params = useParams();
  const router = useRouter();
  const { data: session } = useSession();
  const apiKey = (session?.user as any)?.apiKey;
  const chapterId = params.chapter_id as string;

  const { data: questions, isLoading } = useQuiz(chapterId, apiKey);
  const submitQuiz = useSubmitQuiz();
  const { openUpgradeModal } = useUIStore();

  const [quizState, setQuizState] = useState<QuizState>('start');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  // Premium Gating
  const userTier = (session?.user as any)?.tier || 'free';
  const isPremium = ['premium', 'pro'].includes(userTier.toLowerCase());

  if (!isPremium) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4 text-center">
        <div className="bg-bg-surface border border-border p-12 rounded-3xl space-y-8 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

          <div className="w-24 h-24 bg-accent/10 rounded-full flex items-center justify-center mx-auto border border-accent/20 relative">
            <Sparkles className="h-10 w-10 text-accent animate-pulse" />
            <div className="absolute inset-0 bg-accent/20 blur-2xl rounded-full" />
          </div>

          <div className="space-y-4 relative">
            <h2 className="text-3xl font-black text-white uppercase tracking-tighter italic">Neural Link <span className="text-accent">Encryption</span></h2>
            <p className="text-sm font-medium text-white/60 leading-relaxed max-w-sm mx-auto uppercase tracking-wide">
              Advanced cognitive assessments are reserved for top-tier operatives. Upgrade your clearance level to unlock neural synchronization.
            </p>
          </div>

          <div className="flex flex-col gap-3 relative">
            <Button
              onClick={openUpgradeModal}
              className="w-full bg-accent hover:bg-accent/90 text-black font-black uppercase tracking-widest py-6"
            >
              Initialize Upgrade
            </Button>
            <Button
              variant="ghost"
              onClick={() => router.push(`/course/${chapterId}`)}
              className="text-[10px] font-black uppercase tracking-widest text-white/40 hover:text-white"
            >
              Return to Chapter
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const quizQuestions = questions?.data || [];

  if (!quizQuestions.length) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-2">No Quiz Available</h2>
        <p className="text-muted-foreground mb-4">
          This chapter doesn't have a quiz yet.
        </p>
        <Button onClick={() => router.push(`/course/${chapterId}`)}>
          Back to Chapter
        </Button>
      </div>
    );
  }

  const handleStart = () => {
    setQuizState('taking');
    setCurrentQuestion(0);
    setAnswers({});
    setSelectedAnswer(null);
  };

  const handleSelectAnswer = (optionIndex: number) => {
    setSelectedAnswer(optionIndex);
  };

  const handleNextQuestion = () => {
    const question = quizQuestions[currentQuestion];
    setAnswers(prev => ({ ...prev, [question.id]: selectedAnswer! }));

    if (currentQuestion < quizQuestions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
      setSelectedAnswer(null);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setQuizState('submitting');
    try {
      await submitQuiz.mutateAsync({
        chapterId,
        answers,
        apiKey,
      });
      setQuizState('results');
    } catch (error) {
      console.error('Quiz submission failed:', error);
      setQuizState('taking');
    }
  };

  if (quizState === 'start') {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center space-y-4">
          <Trophy className="h-20 w-20 text-primary mx-auto" />
          <h1 className="text-3xl font-bold">Chapter Quiz</h1>
          <p className="text-muted-foreground">
            Test your knowledge with {quizQuestions.length} questions
          </p>
        </div>

        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6 space-y-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Questions</span>
              <span className="font-semibold">{quizQuestions.length}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Passing Score</span>
              <span className="font-semibold">80%</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Time Limit</span>
              <span className="font-semibold">No limit</span>
            </div>

            <Button onClick={handleStart} className="w-full mt-6" size="lg">
              Start Quiz
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (quizState === 'taking') {
    const question = quizQuestions[currentQuestion];
    const progress = ((currentQuestion + 1) / quizQuestions.length) * 100;

    return (
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Progress */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">
              Question {currentQuestion + 1} of {quizQuestions.length}
            </span>
            <span className="text-muted-foreground">
              {Math.round(progress)}%
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question */}
        <Card className="bg-bg-surface border-border">
          <CardContent className="pt-6 space-y-6">
            <h2 className="text-xl font-semibold">{question.question_text}</h2>

            <div className="space-y-3">
              {question.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectAnswer(index)}
                  className={`w-full p-4 text-left rounded-lg border transition-all ${selectedAnswer === index
                    ? 'border-primary bg-primary/10'
                    : 'border-border hover:border-primary/50'
                    }`}
                >
                  <span className="font-medium mr-2">
                    {String.fromCharCode(65 + index)}.
                  </span>
                  {option}
                </button>
              ))}
            </div>

            <div className="flex items-center justify-between pt-4">
              <Button
                variant="ghost"
                onClick={() => {
                  if (currentQuestion > 0) {
                    setCurrentQuestion(prev => prev - 1);
                    setSelectedAnswer(answers[quizQuestions[currentQuestion - 1].id]);
                  }
                }}
                disabled={currentQuestion === 0}
              >
                Previous
              </Button>
              <Button
                onClick={handleNextQuestion}
                disabled={selectedAnswer === null}
              >
                {currentQuestion < quizQuestions.length - 1 ? 'Next' : 'Submit'}
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (quizState === 'submitting') {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-muted-foreground">Submitting your answers...</p>
      </div>
    );
  }

  if (quizState === 'results') {
    const result = submitQuiz.data?.data;
    if (!result) return null;

    return <QuizResults result={result} onRetake={handleStart} onContinue={() => router.push(`/course/${chapterId}`)} />;
  }

  return null;
}
