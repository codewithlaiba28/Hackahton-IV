'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { QuizSubmission } from '@/types/api';

export function useQuiz(chapterId: string, apiKey?: string) {
  return useQuery({
    queryKey: ['quiz', chapterId],
    queryFn: () => api.quizzes.get(chapterId, apiKey),
    enabled: !!chapterId && !!apiKey,
  });
}

export function useSubmitQuiz() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ chapterId, answers, apiKey }: {
      chapterId: string;
      answers: QuizSubmission;
      apiKey?: string;
    }) => api.quizzes.submit(chapterId, answers, apiKey),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['quiz', variables.chapterId] });
      queryClient.invalidateQueries({ queryKey: ['progress'] });
    },
  });
}
