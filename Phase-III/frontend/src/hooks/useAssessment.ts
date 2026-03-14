import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useAssessmentQuestions(chapterId: string, apiKey?: string) {
    return useQuery({
        queryKey: ['assessments', chapterId],
        queryFn: () => api.assessments.questions(chapterId, apiKey),
        enabled: !!chapterId,
    });
}

export function useSubmitAssessment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({
            chapterId,
            questionId,
            answerText,
            apiKey,
        }: {
            chapterId: string;
            questionId: string;
            answerText: string;
            apiKey?: string;
        }) => api.assessments.submit(chapterId, questionId, answerText, apiKey),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({
                queryKey: ['assessments', variables.chapterId, 'results']
            });
            // Also invalidate progress to reflect participation
            queryClient.invalidateQueries({
                queryKey: ['progress']
            });
        },
    });
}

export function useAssessmentResults(chapterId: string, apiKey?: string) {
    return useQuery({
        queryKey: ['assessments', chapterId, 'results'],
        queryFn: () => (api as any).assessments.results ? (api as any).assessments.results(chapterId, apiKey) : Promise.resolve({ data: [] }),
        enabled: !!chapterId,
    });
}
