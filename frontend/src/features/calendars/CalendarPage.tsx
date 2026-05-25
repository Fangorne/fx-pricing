import { useState } from 'react'
import { useCalendar } from '@/hooks/useCalendar'
import { HolidayList } from './HolidayList'
import { BusinessDayChecker } from './BusinessDayChecker'
import { Alert } from '@/components/ui/Alert'
import { Badge } from '@/components/ui/Badge'

const CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD', 'SEK', 'NOK']

const CURRENT_YEAR = new Date().getFullYear()
const YEARS = [-2, -1, 0, 1, 2].map((offset) => CURRENT_YEAR + offset)

export function CalendarPage() {
  const [currency, setCurrency] = useState('USD')
  const [year, setYear] = useState(CURRENT_YEAR)
  const { holidays, loading, error } = useCalendar(currency, year)

  return (
    <div className="space-y-4 px-6 py-6">
      {/* Page header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2">
        <span className="text-label uppercase tracking-wider text-text-muted">Market Calendars</span>
        {!loading && holidays.length > 0 && (
          <Badge variant="neutral">{holidays.length} holidays</Badge>
        )}
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <p className="text-label uppercase tracking-wider text-text-muted mb-1">Currency</p>
          <div className="flex gap-1 flex-wrap">
            {CURRENCIES.map((c) => (
              <button
                key={c}
                onClick={() => setCurrency(c)}
                className={`
                  rounded px-2.5 py-1 font-mono text-xs font-semibold transition-colors duration-[100ms]
                  ${c === currency
                    ? 'bg-accent/15 text-accent border border-accent/30'
                    : 'border border-border-default bg-bg-elevated text-text-secondary hover:border-border-strong hover:text-text-primary'
                  }
                `}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="text-label uppercase tracking-wider text-text-muted mb-1">Year</p>
          <div className="flex gap-1">
            {YEARS.map((y) => (
              <button
                key={y}
                onClick={() => setYear(y)}
                className={`
                  rounded px-2.5 py-1 font-mono text-xs font-semibold transition-colors duration-[100ms]
                  ${y === year
                    ? 'bg-accent/15 text-accent border border-accent/30'
                    : 'border border-border-default bg-bg-elevated text-text-secondary hover:border-border-strong hover:text-text-primary'
                  }
                `}
              >
                {y}
              </button>
            ))}
          </div>
        </div>
      </div>

      {error && <Alert variant="error">API unavailable — {error}</Alert>}

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        {/* Holiday list */}
        <div className="space-y-2">
          <p className="text-label uppercase tracking-wider text-text-muted">
            {currency} holidays {year}
          </p>
          <HolidayList holidays={holidays} loading={loading} />
        </div>

        {/* Business day checker */}
        <BusinessDayChecker currency={currency} />
      </div>
    </div>
  )
}
