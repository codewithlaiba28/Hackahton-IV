'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useChapters(apiKey?: string) {
  return useQuery({
    queryKey: ['chapters'],
    queryFn: () => api.chapters.list(apiKey),
    enabled: !!apiKey,
  });
}

export function useChapter(id: string, apiKey?: string) {
  return useQuery({
    queryKey: ['chapters', id],
    queryFn: () => api.chapters.get(id, apiKey),
    enabled: !!id && !!apiKey,
  });
}
