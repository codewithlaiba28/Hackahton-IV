'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useProgress(userId: string, apiKey?: string) {
  return useQuery({
    queryKey: ['progress', userId],
    queryFn: () => api.progress.get(userId, apiKey),
    enabled: !!userId && !!apiKey,
  });
}

export function useUpdateProgress() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ userId, chapterId, status, apiKey }: {
      userId: string;
      chapterId: string;
      status: string;
      apiKey?: string;
    }) => api.progress.update(userId, chapterId, status, apiKey),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['progress', variables.userId] });
      queryClient.invalidateQueries({ queryKey: ['chapters'] });
    },
  });
}
