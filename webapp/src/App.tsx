import { Grid } from '@/features/grid'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LeagueSelect } from './features/league-select'
import { FieldSelect } from './features/field-select'
import { MatchSelect } from './features/match-select'

function App() {
  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <div className="p-8 flex flex-col gap-4">
        <div className="flex gap-4">
          <LeagueSelect />
          <MatchSelect />
          <FieldSelect />
        </div>
        <Grid />
      </div>
    </QueryClientProvider>
  )
}

export default App
