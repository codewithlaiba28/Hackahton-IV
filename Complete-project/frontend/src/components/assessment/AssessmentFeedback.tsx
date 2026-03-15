'use client';

import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
    Trophy,
    CheckCircle2,
    XCircle,
    Lightbulb,
    TrendingUp,
    ArrowLeft,
    RotateCcw
} from 'lucide-react';
import { AssessmentResult } from '@/types/api';
import Link from 'next/link';

interface AssessmentFeedbackProps {
    result: AssessmentResult;
    onRetry: () => void;
    chapterId: string;
}

export default function AssessmentFeedback({ result, onRetry, chapterId }: AssessmentFeedbackProps) {
    const getGradeColor = (grade: string) => {
        switch (grade) {
            case 'A': return 'text-success border-success';
            case 'B': return 'text-primary border-primary';
            case 'C': return 'text-warning border-warning';
            default: return 'text-error border-error';
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="flex flex-col md:flex-row gap-6">
                {/* Main Score Card */}
                <Card className="flex-1 bg-bg-surface border-border overflow-hidden">
                    <CardHeader className="bg-primary/5 pb-8">
                        <div className="flex justify-between items-start">
                            <div>
                                <CardTitle className="text-2xl">Assessment Result</CardTitle>
                                <p className="text-sm text-muted-foreground mt-1">Evaluated by Course Companion AI</p>
                            </div>
                            <div className={`text-5xl font-black border-4 rounded-xl p-3 ${getGradeColor(result.grade)}`}>
                                {result.grade}
                            </div>
                        </div>
                        <div className="mt-6 flex items-end gap-3">
                            <span className="text-4xl font-bold">{result.score}</span>
                            <span className="text-muted-foreground text-xl mb-1">/ 100</span>
                            <div className="ml-auto">
                                <Badge variant="outline" className="border-primary/30 text-primary">
                                    {result.word_count} words
                                </Badge>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent className="pt-8 space-y-8">
                        {/* Feedback Section */}
                        <div>
                            <div className="flex items-center gap-2 mb-3">
                                <Trophy className="h-5 w-5 text-warning" />
                                <h3 className="font-bold text-lg">AI Feedback</h3>
                            </div>
                            <p className="text-muted-foreground leading-relaxed italic">
                                "{result.feedback}"
                            </p>
                        </div>

                        {/* Concepts Grid */}
                        <div className="grid md:grid-cols-2 gap-6">
                            <div className="space-y-3">
                                <div className="flex items-center gap-2 text-success">
                                    <CheckCircle2 className="h-4 w-4" />
                                    <h4 className="font-semibold">Concepts Mastered</h4>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {result.correct_concepts.map((concept, i) => (
                                        <Badge key={i} variant="secondary" className="bg-success/10 text-success border-success/20">
                                            {concept}
                                        </Badge>
                                    ))}
                                </div>
                            </div>

                            <div className="space-y-3">
                                <div className="flex items-center gap-2 text-warning">
                                    <TrendingUp className="h-4 w-4" />
                                    <h4 className="font-semibold">Areas for Focus</h4>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {result.missing_concepts.map((concept, i) => (
                                        <Badge key={i} variant="secondary" className="bg-warning/10 text-warning border-warning/20">
                                            {concept}
                                        </Badge>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Improvement Suggestions */}
                        <div className="p-4 rounded-lg bg-primary/5 border border-primary/10">
                            <div className="flex items-center gap-2 mb-2 text-primary">
                                <Lightbulb className="h-5 w-5" />
                                <h4 className="font-bold">How to Improve</h4>
                            </div>
                            <p className="text-sm text-muted-foreground leading-relaxed">
                                {result.improvement_suggestions}
                            </p>
                        </div>
                    </CardContent>
                    <CardFooter className="bg-bg-card/50 border-t border-border p-6 flex flex-wrap gap-4">
                        <Button variant="outline" onClick={onRetry} className="flex-1 sm:flex-none">
                            <RotateCcw className="mr-2 h-4 w-4" />
                            Try Again
                        </Button>
                        <Link href={`/course/${chapterId}`} className="flex-1 sm:flex-none">
                            <Button className="w-full">
                                <ArrowLeft className="mr-2 h-4 w-4" />
                                Back to Chapter
                            </Button>
                        </Link>
                    </CardFooter>
                </Card>
            </div>
        </div>
    );
}
