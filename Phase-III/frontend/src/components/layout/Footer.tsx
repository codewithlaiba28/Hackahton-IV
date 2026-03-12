export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-12 bg-bg-elevated border-t border-border">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="col-span-2">
            <h3 className="text-xl font-bold mb-4">Course Companion FTE</h3>
            <p className="text-muted-foreground mb-4 max-w-sm">
              Your 24/7 AI-powered tutor for AI Agent Development. Learn at your own pace with personalized guidance.
            </p>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="/course" className="hover:text-foreground transition-colors">Course</a></li>
              <li><a href="/progress" className="hover:text-foreground transition-colors">Progress</a></li>
              <li><a href="/pricing" className="hover:text-foreground transition-colors">Pricing</a></li>
            </ul>
          </div>
          
          {/* Legal */}
          <div>
            <h4 className="font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-foreground transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-foreground transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
        
        {/* Bottom Bar */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-muted-foreground">
            © {currentYear} Course Companion FTE. All rights reserved.
          </p>
          <p className="text-sm text-muted-foreground">
            Built with ❤️ for Panaversity Agent Factory Hackathon IV
          </p>
        </div>
      </div>
    </footer>
  );
}
