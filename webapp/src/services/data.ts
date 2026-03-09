import type { PredictionInput, PredictionOutput } from '@/types/data'
import { predictionOutputSchema } from '@/types/data'

const BASE_URL = 'http://localhost:8000'

export const getPredictions = async (
  input: PredictionInput,
): Promise<PredictionOutput> => {
  const url = `${BASE_URL}/predict`

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })

  const payload = await response.json()

  return predictionOutputSchema.parse(payload)
}
