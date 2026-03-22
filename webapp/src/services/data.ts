import * as io from '@/types/data'

const BASE_URL = 'http://localhost:8000'

export const getRows = async (
  input: io.GetRowsInput,
): Promise<io.GetRowsOutput> => {
  const url = `${BASE_URL}/get-rows`

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })

  const payload = await response.json()

  return io.getRowOutputSchema.parse(payload)
}

export const getMatches = async (
  input: io.GetMatchesInput,
): Promise<io.GetMatchesOutput> => {
  const url = `${BASE_URL}/get-matches`

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })

  const payload = await response.json()

  console.log(payload)

  return io.getMatchesOutputSchema.parse(payload)
}
