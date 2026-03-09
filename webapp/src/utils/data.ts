import { League, Season, Field } from '@/types/data'

// Helper to get select options from an enum object
export function enumToOptions<T extends Record<string, number>>(
  enumObj: T,
  labels?: Partial<Record<keyof T, string>>,
): { label: string; value: number }[] {
  return Object.entries(enumObj).map(([key, value]) => ({
    label: labels?.[key as keyof T] ?? key,
    value,
  }))
}

// Pre-built options for each select
export const leagueOptions = enumToOptions(League, {
  PREMIER_LEAGUE: 'Premier League',
  CHAMPIONSHIP: 'Championship',
})

export const seasonOptions = enumToOptions(Season, {
  S_23: '2023/24',
  S_24: '2024/25',
  S_25: '2025/26',
})

export const fieldOptions = enumToOptions(Field, {
  SH: 'Shots',
  SOT: 'Shots on Target',
  FLS: 'Fouls Conceded',
  FLD: 'Fouls Drawn',
})
