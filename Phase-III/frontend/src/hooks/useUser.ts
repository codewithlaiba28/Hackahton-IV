'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { api } from '@/lib/api';

export function useUserProfile() {
    const { data: session } = useSession();
    const apiKey = (session?.user as any)?.apiKey;

    return useQuery({
        queryKey: ['user-profile', apiKey],
        queryFn: async () => {
            const response = await api.users.me(apiKey);
            return response.data; // Return the User object directly
        },
        enabled: !!apiKey,
    });
}

export function useUpgrade() {
    const { data: session, update } = useSession();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            const apiKey = (session?.user as any)?.apiKey;
            if (!apiKey) throw new Error('Authentication required');
            return api.users.upgrade(apiKey);
        },
        onSuccess: async (data) => {
            // Update the session with new tier
            if (update) {
                await update({
                    user: {
                        ...session?.user,
                        tier: data.data.tier,
                    },
                    trigger: "update"
                } as any);
            }

            // Invalidate queries that depend on user tier
            queryClient.invalidateQueries({ queryKey: ['user-profile'] });
            queryClient.invalidateQueries({ queryKey: ['chapters'] });
            queryClient.invalidateQueries({ queryKey: ['progress'] });
            queryClient.invalidateQueries({ queryKey: ['cost-summary'] });
        },
    });
}
