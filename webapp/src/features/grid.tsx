import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Spinner } from '@/components/ui/spinner'
import { useGetRows } from '@/hooks'
import { expectedValue, kellyCriterion, toPercent } from '@/utils/stats'

export const Grid = () => {
  const { data, isLoading, error } = useGetRows()

  const rows = (data?.rows ?? [])
    .filter((row) => {
      const ev = expectedValue(row.odds, row.prediction)
      const kc = kellyCriterion(row.odds, row.prediction)
      return ev > 0 && kc > 0
    })
    .sort(
      (a, b) =>
        expectedValue(b.odds, b.prediction) -
        expectedValue(a.odds, a.prediction),
    )

  return (
    <div className="h-200 overflow-auto">
      <Table>
        <TableHeader className="sticky top-0 z-10 bg-background">
          <TableRow>
            <TableHead>Player</TableHead>
            <TableHead>Team</TableHead>
            <TableHead>Opponent</TableHead>
            <TableHead>Venue</TableHead>
            <TableHead>Best Odds</TableHead>
            <TableHead>Prediction</TableHead>
            <TableHead>EV (%)</TableHead>
            <TableHead>Kelly Criterion (%)</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.player}>
              <TableCell className="font-medium">{row.player}</TableCell>
              <TableCell>{row.team}</TableCell>
              <TableCell>{row.opponent}</TableCell>
              <TableCell>{row.venue}</TableCell>
              <TableCell>{row.odds}</TableCell>
              <TableCell>{toPercent(row.prediction)}</TableCell>
              <TableCell>
                {toPercent(expectedValue(row.odds, row.prediction))}
              </TableCell>
              <TableCell className="text-right">
                {toPercent(kellyCriterion(row.odds, row.prediction))}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="p-8 flex justify-center">
        <GridState
          hasData={!!data?.rows}
          rowCount={rows.length}
          isLoading={isLoading}
          error={error}
        />
      </div>
    </div>
  )
}

interface GridStateProps {
  hasData: boolean
  rowCount: number
  isLoading: boolean
  error: Error | null
}

const GridState = (props: GridStateProps) => {
  const { hasData, rowCount, isLoading, error } = props

  if (isLoading) return <Spinner className="size-6" />

  if (error) return <p className="text-red-600">{error.message}</p>

  if (hasData) {
    if (rowCount === 0) {
      return <p className="text-muted-foreground">No good value odds found.</p>
    }
    return null
  }

  return <p className="text-muted-foreground">What odds do you want to find?</p>
}
