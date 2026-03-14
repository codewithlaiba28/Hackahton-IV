'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Search, BookOpen, Clock, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function SearchPage() {
    const { data: session } = useSession();
    const apiKey = (session?.user as any)?.apiKey;
    const [query, setQuery] = useState('');

    const { data: results, isLoading, isError, refetch } = useQuery({
        queryKey: ['search', query],
        queryFn: () => api.search ? (api as any).search.query(query, apiKey) : Promise.reject('Search API not defined'),
        enabled: false,
    });

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            refetch();
        }
    };

    const searchResults = (results as any)?.data || [];

    return (
        <div className="max-w-4xl mx-auto space-y-8 py-6">
            <div>
                <h1 className="text-4xl font-black text-white uppercase tracking-tighter mb-2">
                    Knowledge <span className="text-primary">Retrieval</span>
                </h1>
                <p className="text-xs font-medium text-white/40 uppercase tracking-widest leading-loose">
                    Access the deep archives of collective intelligence.
                </p>
            </div>

            <Card className="bg-white/5 border-white/5 rounded-2xl p-2 transition-all hover:border-primary/20">
                <form onSubmit={handleSearch} className="flex gap-2">
                    <div className="relative flex-1">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-white/20" />
                        <Input
                            placeholder="Query the system archives..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            className="pl-12 h-14 bg-transparent border-none text-white placeholder:text-white/20 focus-visible:ring-0 focus-visible:ring-offset-0 text-lg font-medium"
                        />
                    </div>
                    <Button type="submit" size="lg" className="h-14 px-8 rounded-xl bg-primary text-primary-foreground font-black uppercase tracking-widest text-[10px] shadow-[0_0_20px_var(--color-primary)]">
                        Execute Search
                    </Button>
                </form>
            </Card>

            <div className="space-y-4">
                {isLoading && (
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <Skeleton key={i} className="h-32 rounded-2xl bg-white/5 border border-white/5" />
                        ))}
                    </div>
                )}

                {isError && (
                    <div className="text-center py-12">
                        <p className="text-error font-black uppercase tracking-widest text-[10px]">Error: Search Subsystem Offline</p>
                    </div>
                )}

                {searchResults.length > 0 && (
                    <div className="space-y-4">
                        {searchResults.map((result: any, index: number) => (
                            <Card key={index} className="bg-white/5 border-white/5 rounded-2xl overflow-hidden hover:border-primary/30 transition-all group">
                                <CardContent className="p-6">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1 space-y-2">
                                            <div className="flex items-center gap-2">
                                                <BookOpen className="h-4 w-4 text-primary" />
                                                <h3 className="text-lg font-black text-white uppercase tracking-tighter">{result.title}</h3>
                                            </div>
                                            <p className="text-sm text-white/40 leading-relaxed line-clamp-2">
                                                {result.snippet}...
                                            </p>
                                            <div className="flex items-center gap-4 text-[10px] font-black uppercase tracking-widest text-white/20">
                                                <div className="flex items-center gap-1">
                                                    <Clock className="h-3 w-3" />
                                                    {result.estimated_read_min || 5} min read
                                                </div>
                                                <div className="text-primary/60">Relevance: {Math.round(result.score * 100)}%</div>
                                            </div>
                                        </div>
                                        <Link href={`/course/${result.id}`}>
                                            <Button variant="ghost" className="h-12 w-12 rounded-xl group-hover:bg-primary/10 group-hover:text-primary">
                                                <ArrowRight className="h-5 w-5" />
                                            </Button>
                                        </Link>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}

                {!isLoading && query && searchResults.length === 0 && (
                    <div className="text-center py-24">
                        <Search className="h-16 w-16 text-white/10 mx-auto mb-6" />
                        <h3 className="text-xl font-black text-white uppercase tracking-tighter mb-2">No Matches Found</h3>
                        <p className="text-white/40 text-[10px] font-black uppercase tracking-widest">The archives contain no data matching your query.</p>
                    </div>
                )}

                {!query && (
                    <div className="text-center py-24 opacity-20">
                        <Search className="h-24 w-24 text-white mx-auto mb-6" />
                        <p className="text-white/40 text-[10px] font-black uppercase tracking-widest">Subsystem Waiting for Input</p>
                    </div>
                )}
            </div>
        </div>
    );
}
