import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useMemo } from 'react'
import { Spinner } from '@/components/ui/spinner'
import { useGetRows } from '@/hooks'
import {
  expectedValue,
  kellyCriterion,
  scoreBets,
  toPercent,
  fractionalOddsToDecimal,
  percentageToDecimalOdds,
} from '@/utils/stats'

export const Grid = () => {
  const { data, isLoading, error } = useGetRows()

  const rows = useMemo(() => {
    const rows = data?.rows ?? []
    const filteredRows = rows
      .map((row) => ({
        ...row,
        ev: expectedValue(row.odds, row.prediction),
        kelly: kellyCriterion(row.odds, row.prediction),
      }))
      .filter((row) => row.ev > 0 && row.kelly > 0)

    return scoreBets(filteredRows)
  }, [data])

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
            <TableHead className="text-right">Kelly Criterion (%)</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.player}>
              <TableCell className="font-medium">{row.player}</TableCell>
              <TableCell>{row.team}</TableCell>
              <TableCell>{row.opponent}</TableCell>
              <TableCell>{row.venue}</TableCell>
              <TableCell>{fractionalOddsToDecimal(row.odds)}</TableCell>
              <TableCell>{percentageToDecimalOdds(row.prediction)}</TableCell>
              <TableCell>{toPercent(row.ev)}</TableCell>
              <TableCell className="text-right">
                {toPercent(row.kelly)}
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
