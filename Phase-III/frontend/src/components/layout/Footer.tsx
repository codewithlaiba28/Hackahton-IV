export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-24 bg-background relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/5 to-transparent" />

      <div className="max-w-7xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          {/* Brand */}
          <div className="col-span-2">
            <h3 className="text-2xl font-black text-white mb-6 tracking-tighter uppercase">
              Course <span className="text-primary">Companion</span>
            </h3>
            <p className="text-muted-foreground/60 mb-8 max-w-sm leading-relaxed">
              The world's first AI-native educational platform for the next generation of agent builders.
              Available 24/7, optimized for rapid mastery.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-black text-white uppercase tracking-widest mb-6">Platform</h4>
            <ul className="space-y-4 text-sm text-muted-foreground/50">
              <li><a href="/course" className="hover:text-primary transition-colors">Curriculum</a></li>
              <li><a href="/progress" className="hover:text-primary transition-colors">Analytics</a></li>
              <li><a href="/pricing" className="hover:text-primary transition-colors">Premium Plans</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-sm font-black text-white uppercase tracking-widest mb-6">Resources</h4>
            <ul className="space-y-4 text-sm text-muted-foreground/50">
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Cloud</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Terms of Execution</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Auth Protocol</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-xs font-medium text-muted-foreground/30 tracking-wide uppercase">
            © {currentYear} COURSE COMPANION FTE. ALL SYSTEMS OPERATIONAL.
          </p>
          <div className="flex items-center gap-6">
            <span className="text-xs font-bold text-primary opacity-50 uppercase tracking-widest">
              Built for Agent Factory Hackathon IV
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
