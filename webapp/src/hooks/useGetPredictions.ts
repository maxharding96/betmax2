import { useQuery } from '@tanstack/react-query'
import { getPredictions } from '@/services/data'
import { useGridInputStore } from './useGridInputStore'
import type { PredictionInput } from '@/types/data'

export const useGetPredictions = () => {
  const { field, over, league, date } = useGridInputStore()

  console.log(field, over, league, date)

  const enabled = Boolean(
    field !== undefined && over !== undefined && league !== undefined && date,
  )

  console.log(enabled)

  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: ['predictions'],
    queryFn: () =>
      getPredictions({
        field,
        over,
        league,
        //TODO this should not be done here
        date: date?.toISOString().split('T')[0],
      } as PredictionInput),
    enabled,
  })

  return {
    data,
    isLoading: isLoading || isFetching,
    error,
  }
}
