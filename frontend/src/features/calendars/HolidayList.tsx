import type { CalendarHoliday } from '@/types/fx'
import { Skeleton } from '@/components/ui/Skeleton'
import { formatIso } from '@/utils/dates'

interface Props {
  holidays: CalendarHoliday[]
  loading: boolean
}

export function HolidayList({ holidays, loading }: Props) {
  if (loading) {
    return <Skeleton lines={10} />
  }

  if (holidays.length === 0) {
    return (
      <div className="flex items-center justify-center rounded-lg border border-border-subtle py-12">
        <p className="text-sm text-text-muted">No holidays found.</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border-default">
      <table className="data-table">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Holiday</th>
          </tr>
        </thead>
        <tbody>
          {holidays.map((h) => (
            <tr key={h.date}>
              <td className="font-mono text-text-secondary w-36">{formatIso(h.date)}</td>
              <td className="text-text-primary">{h.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
