import {
  Combobox,
  ComboboxChip,
  ComboboxChips,
  ComboboxChipsInput,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxItem,
  ComboboxList,
  ComboboxValue,
} from '@/components/ui/combobox'

import { useGridInputStore } from '@/hooks'
import { useGetMatches } from '@/hooks/useGetMatches'
import type { Match } from '@/types/data'

export const MatchSelect = () => {
  const selected = useGridInputStore((state) => state.matches)
  const setSelected = useGridInputStore((state) => state.setMatches)

  const { data } = useGetMatches()

  const matches = data?.matches ?? []

  const matchKey = (match: Match): string => {
    return match.home_team
  }

  const stringifyMatch = (match: Match): string => {
    return `${match.home_team} vs. ${match.away_team}`
  }

  const matchMap = Object.fromEntries(
    matches.map((match) => [matchKey(match), match]),
  )

  const handleValueChange = (value: string[]) => {
    console.log(value)
    return setSelected(value)
  }

  return (
    <Combobox
      items={matches.map(matchKey)}
      multiple
      value={selected}
      onValueChange={handleValueChange}
    >
      <ComboboxChips>
        <ComboboxValue>
          {selected?.map((item) => (
            <ComboboxChip key={item}>{item}</ComboboxChip>
          ))}
        </ComboboxValue>
        <ComboboxChipsInput placeholder="Select matches" />
      </ComboboxChips>
      <ComboboxContent className="w-fit m-2">
        <ComboboxEmpty>No items found.</ComboboxEmpty>
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {stringifyMatch(matchMap[item])}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}
