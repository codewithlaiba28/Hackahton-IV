'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Send, Info } from 'lucide-react';
import { AssessmentQuestion } from '@/types/api';

interface AssessmentFormProps {
    question: AssessmentQuestion;
    onSubmit: (answer: string) => void;
    isLoading: boolean;
    error: string | null;
}

export default function AssessmentForm({ question, onSubmit, isLoading, error }: AssessmentFormProps) {
    const [answer, setAnswer] = useState('');
    const [wordCount, setWordCount] = useState(0);

    useEffect(() => {
        const words = answer.trim().split(/\s+/).filter(w => w.length > 0);
        setWordCount(words.length);
    }, [answer]);

    const isValid = wordCount >= 20 && wordCount <= 500;

    const handleSubmit = () => {
        if (isValid && !isLoading) {
            onSubmit(answer);
        }
    };

    return (
        <Card className="w-full max-w-3xl mx-auto bg-bg-surface border-border shadow-xl">
            <CardHeader>
                <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold px-2 py-1 rounded bg-secondary/20 text-secondary uppercase tracking-wider">
                        {question.difficulty}
                    </span>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Info className="h-3 w-3" />
                        <span>20-500 words required</span>
                    </div>
                </div>
                <CardTitle className="text-xl md:text-2xl leading-tight">
                    {question.question_text}
                </CardTitle>
                <CardDescription>
                    Write a detailed response based on the chapter content. Your answer will be evaluated by an AI mentor.
                </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
                <div className="relative">
                    <Textarea
                        placeholder="Type your answer here..."
                        className="min-h-[300px] resize-none bg-bg-card border-border focus:ring-primary p-4 text-base leading-relaxed"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        disabled={isLoading}
                    />
                    <div className={`absolute bottom-3 right-3 text-xs font-medium px-2 py-1 rounded ${wordCount < 20 || wordCount > 500 ? 'bg-error/10 text-error' : 'bg-success/10 text-success'
                        }`}>
                        {wordCount} words
                    </div>
                </div>

                {error && (
                    <Alert variant="destructive" className="bg-error/10 border-error/20 text-error">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
                    <p className="text-xs text-muted-foreground italic">
                        * Ensure your answer is grounded in the chapter's key concepts.
                    </p>
                    <Button
                        onClick={handleSubmit}
                        disabled={!isValid || isLoading}
                        className="w-full sm:w-auto min-w-[150px]"
                    >
                        {isLoading ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Evaluating...
                            </>
                        ) : (
                            <>
                                <Send className="mr-2 h-4 w-4" />
                                Submit Answer
                            </>
                        )}
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
