import type { CalendarHoliday } from '@/types/fx'

interface Props {
  holidays: CalendarHoliday[]
  loading: boolean
}

function formatDate(iso: string): string {
  return new Date(iso + 'T00:00:00').toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  })
}

export function HolidayList({ holidays, loading }: Props) {
  if (loading) {
    return (
      <div className="animate-pulse space-y-2">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="h-10 rounded bg-gray-800" />
        ))}
      </div>
    )
  }

  if (holidays.length === 0) {
    return <p className="py-8 text-center text-gray-500">Aucun jour férié trouvé.</p>
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-800">
      <table className="w-full text-sm">
        <thead className="bg-gray-900 text-gray-400">
          <tr>
            <th className="px-4 py-3 text-left font-medium">Date</th>
            <th className="px-4 py-3 text-left font-medium">Nom</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {holidays.map((h) => (
            <tr key={h.date} className="hover:bg-gray-800/50">
              <td className="px-4 py-3 font-mono text-gray-300">{formatDate(h.date)}</td>
              <td className="px-4 py-3 text-gray-100">{h.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
