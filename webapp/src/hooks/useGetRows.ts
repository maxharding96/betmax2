import { useQuery } from '@tanstack/react-query'
import { getRows } from '@/services/data'
import { useGridInputStore } from './useGridInputStore'
import type { GetRowsInput } from '@/types/data'
import { useShallow } from 'zustand/react/shallow'

export const useGetRows = () => {
  const { match, field, over } = useGridInputStore(
    useShallow((state) => ({
      match: state.match,
      field: state.field,
      over: state.over,
    })),
  )

  const enabled = Boolean(!!match && field !== undefined && !!over)

  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: ['rows', match, field, over],
    queryFn: () =>
      getRows({
        match,
        field,
        over,
      } as GetRowsInput),
    enabled,
  })

  return {
    data,
    isLoading: isLoading || isFetching,
    error,
  }
}
