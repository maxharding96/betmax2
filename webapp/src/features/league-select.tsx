import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useGridInputStore } from '@/hooks'
import { leagueOptions } from '@/utils/data'

export const LeagueSelect = () => {
  const { league, setLeague } = useGridInputStore()

  return (
    <Select
      value={league !== undefined ? String(league) : ''}
      onValueChange={(v) => setLeague(Number(v))}
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
