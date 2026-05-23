import { useState } from 'react'
import { useBusinessDay } from '@/hooks/useCalendar'

interface Props {
  currency: string
}

export function BusinessDayChecker({ currency }: Props) {
  const [date, setDate] = useState('')
  const { result, loading, error } = useBusinessDay(currency, date)

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-6 space-y-4">
      <h2 className="text-lg font-semibold text-gray-100">Vérifier une date</h2>

      <input
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-2 text-gray-100 focus:border-blue-500 focus:outline-none"
      />

      {loading && <div className="h-8 w-40 animate-pulse rounded bg-gray-800" />}

      {error && !loading && <p className="text-sm text-red-400">Erreur — {error}</p>}

      {result && !loading && (
        <div
          className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium ${
            result.is_business_day
              ? 'bg-green-900/50 text-green-400 border border-green-800'
              : 'bg-red-900/50 text-red-400 border border-red-800'
          }`}
        >
          <span
            className={`h-2 w-2 rounded-full ${result.is_business_day ? 'bg-green-400' : 'bg-red-400'}`}
          />
          {result.is_business_day
            ? 'Business Day'
            : `Non ouvré${result.reason ? ` — ${result.reason}` : ''}`}
        </div>
      )}
    </div>
  )
}
