'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useAssessmentQuestions, useSubmitAssessment } from '@/hooks/useAssessment';
import AssessmentForm from '@/components/assessment/AssessmentForm';
import AssessmentFeedback from '@/components/assessment/AssessmentFeedback';
import PremiumGate from '@/components/premium/PremiumGate';
import { Skeleton } from '@/components/ui/skeleton';
import { Sparkles, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useUIStore } from '@/store/useUIStore';

export default function AssessmentPage() {
    const params = useParams();
    const router = useRouter();
    const { data: session } = useSession();
    const apiKey = (session?.user as any)?.apiKey;
    const userTier = (session?.user as any)?.tier || 'free';
    const chapterId = params.chapter_id as string;
    const { openUpgradeModal } = useUIStore();

    const { data: questionsResponse, isLoading: questionsLoading } = useAssessmentQuestions(chapterId, apiKey);
    const submitAssessment = useSubmitAssessment();

    const [showFeedback, setShowFeedback] = useState(false);
    const [assessmentResult, setAssessmentResult] = useState<any>(null);

    // Premium Gating: Features for 'premium' or 'pro' tiers
    const isPremium = ['premium', 'pro'].includes(userTier.toLowerCase());

    if (!isPremium) {
        return (
            <PremiumGate
                featureName="AI-Graded Assessments"
                onUpgrade={openUpgradeModal}
            />
        );
    }

    if (questionsLoading) {
        return (
            <div className="max-w-3xl mx-auto space-y-6 py-8">
                <Skeleton className="h-10 w-64 mx-auto" />
                <Skeleton className="h-[400px] w-full rounded-xl" />
            </div>
        );
    }

    const questions = questionsResponse?.data || [];

    if (questions.length === 0) {
        return (
            <div className="max-w-2xl mx-auto text-center py-12 space-y-4">
                <h2 className="text-2xl font-bold">No Assessment Available</h2>
                <p className="text-muted-foreground">
                    This chapter doesn't have open-ended assessment questions yet.
                </p>
                <Button onClick={() => router.push(`/course/${chapterId}`)}>
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to Chapter
                </Button>
            </div>
        );
    }

    // Use the first question as the primary assessment
    const question = questions[0];

    const handleSubmit = async (answer: string) => {
        try {
            const response = await submitAssessment.mutateAsync({
                chapterId,
                questionId: question.question_id,
                answerText: answer,
                apiKey
            });

            if (response.data) {
                setAssessmentResult(response.data);
                setShowFeedback(true);
            }
        } catch (error) {
            console.error('Failed to submit assessment:', error);
        }
    };

    const handleRetry = () => {
        setShowFeedback(false);
        setAssessmentResult(null);
    };

    return (
        <div className="container mx-auto py-8 px-4">
            {showFeedback && assessmentResult ? (
                <AssessmentFeedback
                    result={assessmentResult}
                    onRetry={handleRetry}
                    chapterId={chapterId}
                />
            ) : (
                <div className="space-y-8">
                    <div className="text-center max-w-2xl mx-auto">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary mb-4">
                            <Sparkles className="h-4 w-4" />
                            <span className="text-xs font-bold uppercase tracking-widest">Hybrid Intelligence</span>
                        </div>
                        <h1 className="text-4xl font-black mb-4">Conceptual Assessment</h1>
                        <p className="text-muted-foreground">
                            Deep-dive into your understanding. Write your thoughts and let our AI mentor provide critical feedback on your reasoning.
                        </p>
                    </div>

                    <AssessmentForm
                        question={question}
                        onSubmit={handleSubmit}
                        isLoading={submitAssessment.isPending}
                        error={submitAssessment.error ? (submitAssessment.error as any).message : null}
                    />
                </div>
            )}
        </div>
    );
}
