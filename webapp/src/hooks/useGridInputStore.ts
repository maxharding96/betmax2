import { create } from 'zustand'
import type { FieldValue, LeagueValue } from '@/types/data'

interface GridInputStore {
  field?: FieldValue
  setField: (field: FieldValue) => void
  over?: number
  setOver: (over: number) => void
  league?: LeagueValue
  setLeague: (league: LeagueValue) => void
  date?: Date
  setDate: (date: Date) => void
}

export const useGridInputStore = create<GridInputStore>((set) => ({
  field: undefined,
  setField: (field: FieldValue) => set(() => ({ field })),
  over: 1,
  setOver: (over: number) => set(() => ({ over })),
  league: undefined,
  setLeague: (league: LeagueValue) => set(() => ({ league })),
  date: undefined,
  setDate: (date: Date) => set(() => ({ date })),
}))
