import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { format } from 'date-fns'
import { ChevronDownIcon } from 'lucide-react'

interface DatePickProps {
  date?: Date
  setDate: (date: Date) => void
}

export function DatePicker(props: DatePickProps) {
  const { date, setDate } = props

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          data-empty={!date}
          className="w-53 justify-between text-left font-normal"
        >
          {date ? format(date, 'PPP') : <span>Pick a date</span>}
          <ChevronDownIcon />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <Calendar mode="single" required selected={date} onSelect={setDate} />
      </PopoverContent>
    </Popover>
  )
}
