import { useState } from 'react'
import { useBusinessDay } from '@/hooks/useCalendar'
import { Panel } from '@/components/ui/Panel'
import { FieldLabel } from '@/components/ui/FieldLabel'
import { Badge } from '@/components/ui/Badge'

interface Props {
  currency: string
}

export function BusinessDayChecker({ currency }: Props) {
  const [date, setDate] = useState('')
  const { result, loading, error } = useBusinessDay(currency, date)

  return (
    <Panel className="space-y-4 self-start">
      <p className="text-label uppercase tracking-wider text-text-muted">Business Day Check</p>
      <p className="font-mono text-sm font-semibold text-accent">{currency}</p>

      <div>
        <FieldLabel htmlFor="check-date">Select date</FieldLabel>
        <input
          id="check-date"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="form-control font-mono"
        />
      </div>

      {loading && (
        <div className="h-6 w-32 animate-pulse rounded bg-bg-overlay" />
      )}

      {error && !loading && (
        <p className="text-xs text-negative">Error — {error}</p>
      )}

      {result && !loading && (
        <div className="space-y-1">
          <Badge variant={result.is_business_day ? 'positive' : 'negative'} dot>
            {result.is_business_day ? 'Business Day' : 'Non-business Day'}
          </Badge>
          {result.reason && (
            <p className="text-xs text-text-muted mt-1.5">{result.reason}</p>
          )}
        </div>
      )}

      {!date && !result && (
        <p className="text-xs text-text-muted">Select a date above to check.</p>
      )}
    </Panel>
  )
}
