import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useGridInputStore } from '@/hooks'
import { useGetMatches } from '@/hooks/useGetMatches'
import type { Match } from '@/types/data'

export const MatchSelect = () => {
  const match = useGridInputStore((state) => state.match)
  const setMatch = useGridInputStore((state) => state.setMatch)

  const { data } = useGetMatches()

  const matches = data?.matches ?? []

  const stringifyMatch = (match: Match): string => {
    return `${match.home_team} vs. ${match.away_team}`
  }

  const matchMap = Object.fromEntries(
    matches.map((match) => [stringifyMatch(match), match]),
  )

  const handleValueChange = (value: string) => {
    return setMatch(matchMap[value])
  }

  return (
    <Select
      value={match !== undefined ? stringifyMatch(match) : ''}
      onValueChange={handleValueChange}
    >
      <SelectTrigger className="w-45">
        <SelectValue placeholder="Select league" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          {matches.map((match) => {
            const matchStr = stringifyMatch(match)
            return (
              <SelectItem key={matchStr} value={matchStr}>
                {matchStr}
              </SelectItem>
            )
          })}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
