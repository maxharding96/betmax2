import { z } from 'zod'

export const League = {
  PREMIER_LEAGUE: 0,
  CHAMPIONSHIP: 1,
} as const

export const Season = {
  S_23: 0,
  S_24: 1,
  S_25: 2,
} as const

export const Field = {
  SH: 0,
  SOT: 1,
  FLS: 2,
  FLD: 3,
} as const

export const matchSchema = z.object({
  league: z.enum(League),
  season: z.enum(Season),
  home_team: z.string(),
  away_team: z.string(),
  date: z.string(),
})

export const getMatchesInputSchema = z.object({
  league: z.enum(League),
})

export type GetMatchesInput = z.infer<typeof getMatchesInputSchema>

export const getMatchesOutputSchema = z.object({
  matches: z.array(matchSchema),
})

export type GetMatchesOutput = z.infer<typeof getMatchesOutputSchema>

export type Match = z.infer<typeof matchSchema>

export const getRowsInputSchema = z.object({
  match: matchSchema,
  field: z.enum(Field),
  over: z.float32(),
})

export type GetRowsInput = z.infer<typeof getRowsInputSchema>

const rowSchema = z.object({
  player: z.string(),
  team: z.string(),
  opponent: z.string(),
  venue: z.enum(['home', 'away']),
  odds: z.string(),
  prediction: z.float32(),
})

export const getRowOutputSchema = z.object({
  rows: z.array(rowSchema),
})

export type GetRowsOutput = z.infer<typeof getRowOutputSchema>

type EnumValues<T extends Record<string, number>> = T[keyof T]

export type LeagueValue = EnumValues<typeof League>
export type SeasonValue = EnumValues<typeof Season>
export type FieldValue = EnumValues<typeof Field>
