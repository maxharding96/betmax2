import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useGetPredictions } from '@/hooks'

export const Grid = () => {
  const { data } = useGetPredictions()

  if (!data) {
    return null
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-25">Player</TableHead>
          <TableHead>Team</TableHead>
          <TableHead>Opponent</TableHead>
          <TableHead>Venue</TableHead>
          <TableHead>Best Odds</TableHead>
          <TableHead className="text-right">Prediction</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.predictions.map((p) => (
          <TableRow key={p.player}>
            <TableCell className="font-medium">{p.player}</TableCell>
            <TableCell>Arsenal</TableCell>
            <TableCell>Tottenham</TableCell>
            <TableCell>Home</TableCell>
            <TableCell>1.50</TableCell>
            <TableCell className="text-right">{p.prediction}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
