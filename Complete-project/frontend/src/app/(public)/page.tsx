'use client';

import Hero from '@/components/landing/Hero';
import StatsBar from '@/components/landing/StatsBar';
import FeaturesGrid from '@/components/landing/FeaturesGrid';
import AIMentor from '@/components/landing/AIMentor';
import HowItWorks from '@/components/landing/HowItWorks';
import LearningAnalytics from '@/components/landing/LearningAnalytics';
import PricingPreview from '@/components/landing/PricingPreview';
import Testimonials from '@/components/landing/Testimonials';
import Footer from '@/components/layout/Footer';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-background">
      <Hero />
      <StatsBar />
      <FeaturesGrid />
      <AIMentor />
      <HowItWorks />
      <LearningAnalytics />
      <PricingPreview />
      <Testimonials />
      <Footer />
    </main>
  );
}
