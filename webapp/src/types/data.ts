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

export const predictInputSchema = z.object({
  field: z.enum(Field),
  over: z.int(),
  league: z.enum(League),
  date: z.string(),
})

export type PredictionInput = z.infer<typeof predictInputSchema>

const predictionSchema = z.object({
  player: z.string(),
  prediction: z.float32(),
})

export const predictionOutputSchema = z.object({
  predictions: z.array(predictionSchema),
})

export type PredictionOutput = z.infer<typeof predictionOutputSchema>

type EnumValues<T extends Record<string, number>> = T[keyof T]

export type LeagueValue = EnumValues<typeof League>
export type SeasonValue = EnumValues<typeof Season>
export type FieldValue = EnumValues<typeof Field>
