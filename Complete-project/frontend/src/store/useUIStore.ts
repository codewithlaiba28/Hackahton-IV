import { create } from 'zustand';

interface UIState {
  // Sidebar
  isSidebarOpen: boolean;
  openSidebar: () => void;
  closeSidebar: () => void;
  toggleSidebar: () => void;
  
  // Modals
  isUpgradeModalOpen: boolean;
  openUpgradeModal: () => void;
  closeUpgradeModal: () => void;
  
  // Theme (for future light mode)
  theme: 'dark' | 'light';
  setTheme: (theme: 'dark' | 'light') => void;
}

export const useUIStore = create<UIState>((set) => ({
  // Sidebar
  isSidebarOpen: true,
  openSidebar: () => set({ isSidebarOpen: true }),
  closeSidebar: () => set({ isSidebarOpen: false }),
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  
  // Modals
  isUpgradeModalOpen: false,
  openUpgradeModal: () => set({ isUpgradeModalOpen: true }),
  closeUpgradeModal: () => set({ isUpgradeModalOpen: false }),
  
  // Theme
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
}));
