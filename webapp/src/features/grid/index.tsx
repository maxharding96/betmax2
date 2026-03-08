import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export const Grid = () => {
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
        <TableRow>
          <TableCell className="font-medium">Bukayo Saka</TableCell>
          <TableCell>Arsenal</TableCell>
          <TableCell>Tottenham</TableCell>
          <TableCell>Home</TableCell>
          <TableCell>1.50</TableCell>
          <TableCell className="text-right">2.00</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  )
}
