import { create } from 'zustand'
import type { FieldValue, LeagueValue, Match } from '@/types/data'

interface GridInputStore {
  league?: LeagueValue
  setLeague: (league: LeagueValue) => void
  match?: Match
  setMatch: (match: Match) => void
  field?: FieldValue
  setField: (field: FieldValue) => void
  over?: number
  setOver: (over: number) => void
}

export const useGridInputStore = create<GridInputStore>((set) => ({
  league: undefined,
  setLeague: (league: LeagueValue) => set(() => ({ league })),
  match: undefined,
  setMatch: (match: Match) => set(() => ({ match })),
  field: undefined,
  setField: (field: FieldValue) => set(() => ({ field })),
  over: 0.5,
  setOver: (over: number) => set(() => ({ over })),
}))
