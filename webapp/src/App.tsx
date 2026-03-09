import { Grid } from '@/features/grid'
import { DatePicker } from '@/features/date-picker'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useGridInputStore } from './hooks'
import { LeagueSelect } from './features/league-select'
import { FieldSelect } from './features/field-select'

function App() {
  const queryClient = new QueryClient()

  const { date, setDate } = useGridInputStore()

  return (
    <QueryClientProvider client={queryClient}>
      <div className="p-8 flex flex-col gap-4">
        <div className="flex gap-4">
          <DatePicker date={date} setDate={setDate} />
          <LeagueSelect />
          <FieldSelect />
        </div>
        <Grid />
      </div>
    </QueryClientProvider>
  )
}

export default App
