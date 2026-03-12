'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { CheckCircle, XCircle, Trophy, RotateCcw, ArrowRight } from 'lucide-react';
import type { QuizResult } from '@/types/api';

interface QuizResultsProps {
  result: QuizResult;
  onRetake: () => void;
  onContinue: () => void;
}

export default function QuizResults({ result, onRetake, onContinue }: QuizResultsProps) {
  const isPass = result.percentage >= 80;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Score Header */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6 text-center space-y-4">
          {isPass ? (
            <Trophy className="h-20 w-20 text-primary mx-auto" />
          ) : (
            <RotateCcw className="h-20 w-20 text-warning mx-auto" />
          )}

          <div>
            <div className="text-5xl font-bold mb-2">
              {result.score}/{result.total}
            </div>
            <div className={`text-2xl font-bold ${
              isPass ? 'text-success' : 'text-warning'
            }`}>
              {result.percentage}%
            </div>
          </div>

          <p className="text-muted-foreground">
            {isPass
              ? "🎉 Congratulations! You've passed the quiz!"
              : "Keep practicing! You can retake this quiz."}
          </p>

          <div className="flex gap-4 justify-center pt-4">
            <Button onClick={onRetake} variant="outline">
              <RotateCcw className="h-4 w-4 mr-2" />
              Retake Quiz
            </Button>
            <Button onClick={onContinue}>
              Back to Chapter
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Results */}
      <Card className="bg-bg-surface border-border">
        <CardContent className="pt-6 space-y-4">
          <h2 className="text-xl font-semibold mb-4">Question Breakdown</h2>
          
          {result.correct_answers.map((questionId, index) => (
            <div
              key={questionId}
              className="p-4 rounded-lg border border-border bg-bg-elevated"
            >
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-success mt-0.5 shrink-0" />
                <div className="flex-1">
                  <p className="text-sm font-medium mb-2">
                    Question {index + 1} - Correct ✓
                  </p>
                  {result.explanations[questionId] && (
                    <p className="text-sm text-muted-foreground">
                      {result.explanations[questionId]}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}

          {result.correct_answers.length < result.total && (
            <>
              <div className="pt-4 border-t border-border">
                <h3 className="font-semibold mb-3">Questions to Review</h3>
              </div>
              {Array.from({ length: result.total }).map((_, index) => {
                const questionId = Object.keys(result.explanations)[index];
                if (result.correct_answers.includes(questionId)) return null;
                
                return (
                  <div
                    key={questionId}
                    className="p-4 rounded-lg border border-border bg-bg-elevated"
                  >
                    <div className="flex items-start gap-3">
                      <XCircle className="h-5 w-5 text-error mt-0.5 shrink-0" />
                      <div className="flex-1">
                        <p className="text-sm font-medium mb-2">
                          Question {index + 1} - Incorrect ✗
                        </p>
                        {result.explanations[questionId] && (
                          <p className="text-sm text-muted-foreground">
                            {result.explanations[questionId]}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
