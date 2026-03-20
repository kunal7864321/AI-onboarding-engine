import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AnalysisResponse, RoadmapResponse } from '../utils/api';

interface AppState {
  sessionId: string | null;
  analysis: AnalysisResponse | null;
  roadmap: RoadmapResponse | null;
  isLoading: boolean;
  error: string | null;
  
  setSessionId: (id: string | null) => void;
  setAnalysis: (analysis: AnalysisResponse | null) => void;
  setRoadmap: (roadmap: RoadmapResponse | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      sessionId: null,
      analysis: null,
      roadmap: null,
      isLoading: false,
      error: null,
      
      setSessionId: (id) => set({ sessionId: id }),
      setAnalysis: (analysis) => set({ analysis }),
      setRoadmap: (roadmap) => set({ roadmap }),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      reset: () => set({
        sessionId: null,
        analysis: null,
        roadmap: null,
        isLoading: false,
        error: null,
      }),
    }),
    {
      name: 'ai-onboarding-storage',
    }
  )
);
