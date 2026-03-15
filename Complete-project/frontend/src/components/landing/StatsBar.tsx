import { Clock, CheckCircle2, Globe, DollarSign } from 'lucide-react';

export default function StatsBar() {
  const stats = [
    { label: 'Availability', value: '168 hrs/week', icon: Clock, desc: 'Always online, ready to tutor whenever you are.' },
    { label: 'Consistency', value: '99%+', icon: CheckCircle2, desc: 'Unwavering educational quality across all sessions.' },
    { label: 'Languages', value: '50+', icon: Globe, desc: 'Tutor in your native language for better clarity.' },
    { label: 'Cost per Session', value: '$0.25', icon: DollarSign, desc: 'Enterprise-grade education at consumer-grade prices.' },
  ];

  return (
    <section className="py-24 bg-background relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/5 to-transparent" />

      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="group p-8 rounded-2xl bg-bg-surface/50 border border-white/5 hover:border-primary/30 transition-all hover:bg-bg-surface"
            >
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-colors">
                <stat.icon className="w-6 h-6 text-primary" />
              </div>
              <div className="text-3xl font-bold text-white mb-2">
                {stat.value}
              </div>
              <div className="text-sm font-semibold text-primary uppercase tracking-wider mb-4">
                {stat.label}
              </div>
              <p className="text-sm text-muted-foreground/60 leading-relaxed">
                {stat.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
