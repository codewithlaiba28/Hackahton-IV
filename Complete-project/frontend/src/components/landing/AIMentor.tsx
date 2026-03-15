'use client';

import { motion } from 'framer-motion';
import { MessageSquare, Mic, Brain, Sparkles } from 'lucide-react';

export default function AIMentor() {
    const features = [
        {
            title: 'Voice-First Interaction',
            description: 'Interact with your tutor using Whisper-powered speech recognition.',
            icon: Mic,
        },
        {
            title: 'Intelligent Note-taking',
            description: 'Your mentor automatically organizes your thoughts and creates study guides.',
            icon: MessageSquare,
        },
        {
            title: 'Cognitive Scaffolding',
            description: 'Advanced reasoning models adapt to your knowledge gaps in real-time.',
            icon: Brain,
        },
    ];

    return (
        <section className="py-24 bg-background relative" id="ai-mentor">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex flex-col items-center text-center mb-16">
                    <Badge variant="outline" className="mb-4 border-primary/20 text-primary bg-primary/5 px-4 py-1">
                        <Sparkles className="w-3 h-3 mr-2" />
                        AI-Native Learning
                    </Badge>
                    <h2 className="text-4xl md:text-6xl font-black text-white mb-6">
                        Learning with an <span className="text-primary">AI Mentor</span>
                    </h2>
                    <p className="text-xl text-muted-foreground/70 max-w-2xl">
                        Refined with GPT-4o and Cerebras-fast inference to improve your learning,
                        organize your thoughts, and act as your intellectual thought partner.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    {/* Visual Mockup */}
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8 }}
                        className="relative"
                    >
                        <div className="absolute -inset-4 bg-primary/20 rounded-3xl blur-3xl opacity-20 pointer-events-none" />
                        <div className="relative rounded-3xl border border-white/10 bg-bg-surface p-6 shadow-2xl overflow-hidden aspect-video flex flex-col">
                            <div className="flex items-center gap-2 mb-6 border-b border-white/5 pb-4">
                                <div className="w-3 h-3 rounded-full bg-destructive/50" />
                                <div className="w-3 h-3 rounded-full bg-warning/50" />
                                <div className="w-3 h-3 rounded-full bg-success/50" />
                                <div className="ml-4 text-xs font-mono text-white/40">mentor-terminal --v2.0</div>
                            </div>

                            <div className="flex-1 space-y-4 font-mono text-sm">
                                <div className="text-primary opacity-80">{">"} Initializing educational context...</div>
                                <div className="text-white/60 leading-relaxed pl-4 border-l border-primary/20">
                                    Concept identified: "Agentic Workflows". <br />
                                    Would you like a Socratic breakdown or a technical deep-dive?
                                </div>
                                <div className="text-white/40 italic">{">"} User: Give me the high-level intuition.</div>
                                <div className="p-4 rounded-lg bg-primary/5 border border-primary/10 text-white/80">
                                    Think of it as a relay race where each AI agent holds a baton of specific logic...
                                </div>
                            </div>

                            {/* Decorative elements */}
                            <div className="absolute bottom-0 right-0 w-32 h-32 bg-primary/10 blur-2xl rounded-full" />
                        </div>
                    </motion.div>

                    {/* Features */}
                    <div className="space-y-8">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                className="flex gap-6 group"
                            >
                                <div className="w-14 h-14 shrink-0 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center group-hover:border-primary/50 transition-colors">
                                    <feature.icon className="w-6 h-6 text-primary" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary transition-colors">
                                        {feature.title}
                                    </h3>
                                    <p className="text-muted-foreground/60 leading-relaxed">
                                        {feature.description}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}

function Badge({ children, className, variant }: any) {
    return (
        <div className={`text-xs font-bold uppercase tracking-[0.2em] inline-flex items-center rounded-full px-4 py-1.5 ${className}`}>
            {children}
        </div>
    );
}
