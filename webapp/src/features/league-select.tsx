import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useGridInputStore } from '@/hooks'
import type { LeagueValue } from '@/types/data'
import { leagueOptions } from '@/utils/data'

export const LeagueSelect = () => {
  const league = useGridInputStore((state) => state.league)
  const setLeague = useGridInputStore((state) => state.setLeague)

  return (
    <Select
      value={league !== undefined ? String(league) : ''}
      onValueChange={(v) => setLeague(Number(v) as LeagueValue)}
    >
      <SelectTrigger className="w-45">
        <SelectValue placeholder="Select league" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          {leagueOptions.map(({ label, value }) => (
            <SelectItem key={value} value={String(value)}>
              {label}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
