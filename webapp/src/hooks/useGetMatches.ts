import { useQuery } from '@tanstack/react-query'
import { getMatches } from '@/services/data'
import { useGridInputStore } from './useGridInputStore'
import type { GetMatchesInput } from '@/types/data'

export const useGetMatches = () => {
  const league = useGridInputStore((state) => state.league)

  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: ['matches', league],
    queryFn: () =>
      getMatches({
        league,
      } as GetMatchesInput),
    enabled: league !== undefined,
    staleTime: Infinity,
    gcTime: Infinity,
  })

  return {
    data,
    isLoading: isLoading || isFetching,
    error,
  }
}
