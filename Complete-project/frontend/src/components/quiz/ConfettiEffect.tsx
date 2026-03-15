'use client';

import { useEffect, useState } from 'react';
import Confetti from 'react-confetti';

interface ConfettiEffectProps {
  active?: boolean;
  duration?: number;
}

export default function ConfettiEffect({ active = true, duration = 5000 }: ConfettiEffectProps) {
  const [isRunning, setIsRunning] = useState(active);

  useEffect(() => {
    if (active) {
      setIsRunning(true);
      const timer = setTimeout(() => setIsRunning(false), duration);
      return () => clearTimeout(timer);
    }
  }, [active, duration]);

  if (!isRunning) return null;

  return (
    <Confetti
      width={window.innerWidth}
      height={window.innerHeight}
      recycle={false}
      numberOfPieces={200}
      gravity={0.1}
      colors={['#00E5B4', '#0066FF', '#FF6B35', '#22C55E', '#F59E0B']}
    />
  );
}
