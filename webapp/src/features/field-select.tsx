import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useGridInputStore } from '@/hooks'
import { fieldOptions } from '@/utils/data'

export const FieldSelect = () => {
  const { field, setField } = useGridInputStore()

  return (
    <Select
      value={field !== undefined ? String(field) : ''}
      onValueChange={(v) => setField(Number(v))}
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
