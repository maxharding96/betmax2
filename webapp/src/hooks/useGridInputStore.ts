import { create } from 'zustand'
import type { FieldValue, LeagueValue } from '@/types/data'

interface GridInputStore {
  league?: LeagueValue
  setLeague: (league: LeagueValue) => void
  matches?: string[]
  setMatches: (matches: string[]) => void
  field?: FieldValue
  setField: (field: FieldValue) => void
  over?: number
  setOver: (over: number) => void
}

export const useGridInputStore = create<GridInputStore>((set) => ({
  league: undefined,
  setLeague: (league: LeagueValue) => set(() => ({ league })),
  matches: undefined,
  setMatches: (matches: string[]) => set(() => ({ matches })),
  field: undefined,
  setField: (field: FieldValue) => set(() => ({ field })),
  over: 0.5,
  setOver: (over: number) => set(() => ({ over })),
}))
