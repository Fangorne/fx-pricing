import { useState } from 'react'
import { useCalendar } from '@/hooks/useCalendar'
import { HolidayList } from './HolidayList'
import { BusinessDayChecker } from './BusinessDayChecker'

const CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD', 'SEK', 'NOK']

const CURRENT_YEAR = new Date().getFullYear()
const YEARS = [-2, -1, 0, 1, 2].map((offset) => CURRENT_YEAR + offset)

export function CalendarPage() {
  const [currency, setCurrency] = useState('USD')
  const [year, setYear] = useState(CURRENT_YEAR)
  const { holidays, loading, error } = useCalendar(currency, year)

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-100">Calendriers de Marché</h1>
        <span className="text-sm text-gray-500">{holidays.length} jours fériés</span>
      </div>

      <div className="flex flex-wrap gap-4">
        <div className="space-y-1">
          <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
            Devise
          </label>
          <select
            value={currency}
            onChange={(e) => setCurrency(e.target.value)}
            className="rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 focus:border-blue-500 focus:outline-none"
          >
            {CURRENCIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-1">
          <label className="text-xs font-medium uppercase tracking-wide text-gray-500">Année</label>
          <select
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            className="rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 focus:border-blue-500 focus:outline-none"
          >
            {YEARS.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-800 bg-red-950 px-4 py-3 text-red-400">
          API inaccessible — {error}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-2">
          <h2 className="text-lg font-semibold text-gray-100">
            Jours fériés {currency} {year}
          </h2>
          <HolidayList holidays={holidays} loading={loading} />
        </div>

        <BusinessDayChecker currency={currency} />
      </div>
    </div>
  )
}
