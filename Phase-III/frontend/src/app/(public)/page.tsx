'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import Hero from '@/components/landing/Hero';
import StatsBar from '@/components/landing/StatsBar';
import FeaturesGrid from '@/components/landing/FeaturesGrid';
import HowItWorks from '@/components/landing/HowItWorks';
import PricingPreview from '@/components/landing/PricingPreview';
import Testimonials from '@/components/landing/Testimonials';
import Footer from '@/components/layout/Footer';

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <Hero />
      <StatsBar />
      <FeaturesGrid />
      <HowItWorks />
      <PricingPreview />
      <Testimonials />
      <Footer />
    </main>
  );
}
