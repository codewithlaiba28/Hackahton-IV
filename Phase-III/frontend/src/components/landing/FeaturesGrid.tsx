import { BookOpen, Route, MessageSquare, Award, TrendingUp, Lock } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const features = [
  {
    icon: BookOpen,
    title: 'Content Delivery',
    description: 'Access comprehensive AI Agent Development course content with clear explanations.',
  },
  {
    icon: Route,
    title: 'Smart Navigation',
    description: 'Navigate through chapters with intelligent sequencing and progress tracking.',
  },
  {
    icon: MessageSquare,
    title: 'Grounded Q&A',
    description: 'Get answers based on course content with AI-powered explanations.',
  },
  {
    icon: Award,
    title: 'Interactive Quizzes',
    description: 'Test your knowledge with instant feedback and detailed explanations.',
  },
  {
    icon: TrendingUp,
    title: 'Progress Tracking',
    description: 'Monitor your learning journey with detailed analytics and streaks.',
  },
  {
    icon: Lock,
    title: 'Freemium Access',
    description: 'Start free with chapters 1-3, upgrade for full course access.',
  },
];

export default function FeaturesGrid() {
  return (
    <section className="py-20 bg-background">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-4">
          Everything You Need to Succeed
        </h2>
        <p className="text-lg text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          Comprehensive learning platform designed for modern students
        </p>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="bg-bg-surface border-border hover:border-primary/50 transition-colors">
              <CardContent className="pt-6">
                <feature.icon className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
