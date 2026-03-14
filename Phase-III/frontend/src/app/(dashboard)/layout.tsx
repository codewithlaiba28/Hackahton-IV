'use client';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useUIStore } from '@/store/useUIStore';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';
import UpgradeModal from '@/components/premium/UpgradeModal';
import { useUpgrade } from '@/hooks/useUser';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { isSidebarOpen, isUpgradeModalOpen, closeUpgradeModal } = useUIStore();
  const [mounted, setMounted] = useState(false);
  const upgradeMutation = useUpgrade();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (status === 'loading') return;
    if (status === 'unauthenticated') {
      router.push('/login');
    }
  }, [status, router]);

  if (status === 'loading' || !mounted) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main
          className={`flex-1 transition-all duration-300 ${isSidebarOpen ? 'ml-64' : 'ml-0'
            }`}
        >
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
      <UpgradeModal
        isOpen={isUpgradeModalOpen}
        onClose={closeUpgradeModal}
        isLoading={upgradeMutation.isPending}
        onUpgrade={() => {
          upgradeMutation.mutate(undefined, {
            onSuccess: () => {
              closeUpgradeModal();
            }
          });
        }}
      />
    </div>
  );
}
