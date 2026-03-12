export default function StatsBar() {
  const stats = [
    { label: 'Availability', value: '168 hrs/week' },
    { label: 'Consistency', value: '99%+' },
    { label: 'Languages', value: '50+' },
    { label: 'Cost per Session', value: '$0.25' },
  ];

  return (
    <section className="py-12 bg-bg-surface border-y border-border">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary mb-2">
                {stat.value}
              </div>
              <div className="text-sm md:text-base text-muted-foreground">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
