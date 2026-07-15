import { create } from 'zustand';

export const usePredictionStore = create((set) => ({
  predictions: [],
  loading: false,
  error: null,

  setPredictions: (predictions) => set({ predictions }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  addPrediction: (prediction) =>
    set((state) => ({
      predictions: [...state.predictions, prediction],
    })),

  clearPredictions: () => set({ predictions: [] }),
  clearError: () => set({ error: null }),
}));

export const useMatchStore = create((set) => ({
  currentMatch: null,
  matches: [],
  loading: false,

  setCurrentMatch: (match) => set({ currentMatch: match }),
  setMatches: (matches) => set({ matches }),
  setLoading: (loading) => set({ loading }),

  updateMatch: (matchId, updates) =>
    set((state) => ({
      matches: state.matches.map((m) =>
        m.id === matchId ? { ...m, ...updates } : m
      ),
    })),
}));

export const usePlayerStore = create((set) => ({
  players: [],
  selectedPlayer: null,
  loading: false,

  setPlayers: (players) => set({ players }),
  setSelectedPlayer: (player) => set({ selectedPlayer: player }),
  setLoading: (loading) => set({ loading }),
}));
