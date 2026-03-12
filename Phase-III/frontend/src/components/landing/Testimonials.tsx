import { Card, CardContent } from '@/components/ui/card';

const testimonials = [
  {
    name: 'Sarah Khan',
    role: 'Software Developer',
    content: 'This AI tutor helped me understand AI agents in just 2 weeks. The adaptive learning path is incredible!',
    avatar: 'SK',
  },
  {
    name: 'Ahmed Hassan',
    role: 'Computer Science Student',
    content: 'Finally, a platform that explains complex concepts in simple terms. The 24/7 availability is a game-changer.',
    avatar: 'AH',
  },
  {
    name: 'Emily Chen',
    role: 'Data Analyst',
    content: 'The quizzes and instant feedback helped me prepare for my AI certification. Highly recommend!',
    avatar: 'EC',
  },
];

export default function Testimonials() {
  return (
    <section className="py-20 bg-background">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-4">
          Loved by Learners Worldwide
        </h2>
        <p className="text-lg text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
          Join thousands of students mastering AI Agent Development
        </p>
        
        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="bg-bg-surface border-border">
              <CardContent className="pt-6">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary font-semibold">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-semibold">{testimonial.name}</div>
                    <div className="text-sm text-muted-foreground">{testimonial.role}</div>
                  </div>
                </div>
                <p className="text-muted-foreground italic">"{testimonial.content}"</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
