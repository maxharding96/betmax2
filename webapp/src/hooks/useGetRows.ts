import { useQuery } from '@tanstack/react-query'
import { getRows } from '@/services/data'
import { useGridInputStore } from './useGridInputStore'
import type { GetRowsInput } from '@/types/data'
import { useShallow } from 'zustand/react/shallow'

export const useGetRows = () => {
  const { league, matches, field, over } = useGridInputStore(
    useShallow((state) => ({
      league: state.league,
      matches: state.matches,
      field: state.field,
      over: state.over,
    })),
  )

  const enabled = Boolean(!!matches && field !== undefined && !!over)

  const homeTeams = matches?.sort((a, b) => (b > a ? 1 : 0))

  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: ['rows', homeTeams, field, over],
    queryFn: () =>
      getRows({
        league,
        home_teams: homeTeams,
        field,
        over,
      } as GetRowsInput),
    enabled,
    staleTime: Infinity,
    gcTime: Infinity,
  })

  return {
    data,
    isLoading: isLoading || isFetching,
    error,
  }
}
