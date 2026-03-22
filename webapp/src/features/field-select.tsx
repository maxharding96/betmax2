import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useGridInputStore } from '@/hooks'
import type { FieldValue } from '@/types/data'
import { fieldOptions } from '@/utils/data'

export const FieldSelect = () => {
  const field = useGridInputStore((state) => state.field)
  const setField = useGridInputStore((state) => state.setField)

  return (
    <Select
      value={field !== undefined ? String(field) : ''}
      onValueChange={(v) => setField(Number(v) as FieldValue)}
    >
      <SelectTrigger className="w-45">
        <SelectValue placeholder="Select field" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          {fieldOptions.map(({ label, value }) => (
            <SelectItem key={value} value={String(value)}>
              {label}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
