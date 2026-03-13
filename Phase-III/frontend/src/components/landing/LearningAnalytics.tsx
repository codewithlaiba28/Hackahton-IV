'use client';

import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, BarChart3, Target, Activity } from 'lucide-react';

const data = [
    { name: 'Week 1', score: 45 },
    { name: 'Week 2', score: 52 },
    { name: 'Week 3', score: 48 },
    { name: 'Week 4', score: 61 },
    { name: 'Week 5', score: 75 },
    { name: 'Week 6', score: 82 },
    { name: 'Week 7', score: 91 },
];

export default function LearningAnalytics() {
    return (
        <section className="py-24 bg-background relative" id="analytics">
            <div className="max-w-7xl mx-auto px-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

                    <div className="order-2 lg:order-1">
                        <h2 className="text-4xl md:text-5xl font-black text-white mb-8">
                            Performance & <span className="text-primary">Analytics</span>
                        </h2>
                        <p className="text-xl text-muted-foreground/60 mb-12">
                            Transform your learning data into actionable insights.
                            Monitor your growth across all chapters and identify knowledge gaps automatically.
                        </p>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            {[
                                { label: 'Avg. Score', value: '88%', icon: Target },
                                { label: 'Retention', value: '94%', icon: Activity },
                                { label: 'Focus Time', value: '42h', icon: BarChart3 },
                                { label: 'Growth', value: '+24%', icon: TrendingUp },
                            ].map((item, i) => (
                                <div key={i} className="p-6 rounded-2xl bg-bg-surface/50 border border-white/5 flex items-center gap-4 hover:bg-bg-surface transition-colors">
                                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                                        <item.icon className="w-5 h-5 text-primary" />
                                    </div>
                                    <div>
                                        <div className="text-xs font-bold text-white/40 uppercase tracking-widest">{item.label}</div>
                                        <div className="text-xl font-bold text-white">{item.value}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.8 }}
                        className="order-1 lg:order-2 relative"
                    >
                        <div className="absolute -inset-4 bg-primary/10 rounded-[2.5rem] blur-3xl opacity-20 pointer-events-none" />

                        <div className="relative p-8 rounded-[2rem] border border-white/10 bg-bg-surface shadow-2xl">
                            <div className="flex items-center justify-between mb-8">
                                <div>
                                    <h3 className="text-lg font-bold text-white">Course Progress</h3>
                                    <p className="text-sm text-muted-foreground/50">Engagement over time</p>
                                </div>
                                <div className="px-3 py-1 rounded-md bg-white/5 text-primary text-xs font-mono font-bold">
                                    LIVE DATA
                                </div>
                            </div>

                            <div className="h-[300px] w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={data}>
                                        <defs>
                                            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#00f5d4" stopOpacity={0.3} />
                                                <stop offset="95%" stopColor="#00f5d4" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                                        <XAxis
                                            dataKey="name"
                                            axisLine={false}
                                            tickLine={false}
                                            tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 12 }}
                                            dy={10}
                                        />
                                        <YAxis hide />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#121212', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                                            itemStyle={{ color: '#00f5d4' }}
                                        />
                                        <Area
                                            type="monotone"
                                            dataKey="score"
                                            stroke="#00f5d4"
                                            strokeWidth={3}
                                            fillOpacity={1}
                                            fill="url(#colorScore)"
                                            animationDuration={2000}
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Float Card Mockup */}
                        <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                            className="absolute -bottom-6 -left-6 p-6 rounded-2xl bg-bg-elevated border border-primary/20 shadow-2xl backdrop-blur-xl"
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-12 h-12 rounded-full border-2 border-primary border-t-transparent animate-spin" />
                                <div>
                                    <div className="text-xs text-muted-foreground/50 font-bold uppercase">Synthesis</div>
                                    <div className="text-sm text-white font-bold tracking-tight">AI Agent Mastery: 82%</div>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>

                </div>
            </div>
        </section>
    );
}
