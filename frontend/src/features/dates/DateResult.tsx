import type { SpotDateCalcResult } from '@/hooks/useSpotDate'
import { formatIso } from '@/utils/dates'

interface Props {
  result: SpotDateCalcResult
}

interface DataRowProps {
  label: string
  value: string
  highlight?: boolean
}

function DataRow({ label, value, highlight }: DataRowProps) {
  return (
    <div className="flex items-center justify-between border-b border-border-subtle py-2.5">
      <span className="text-xs text-text-secondary">{label}</span>
      <span
        className={`font-mono font-semibold ${
          highlight ? 'text-data text-accent' : 'text-sm text-text-primary'
        }`}
      >
        {value}
      </span>
    </div>
  )
}

export function DateResult({ result }: Props) {
  return (
    <div className="rounded-lg border border-border-default bg-bg-surface">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border-subtle px-4 py-3">
        <span className="font-mono text-data font-bold text-accent">{result.pair}</span>
        <span className="text-xs text-text-muted">
          Trade: {formatIso(result.tradeDate)} &middot; {result.tenor}
        </span>
      </div>

      {/* Primary result — spot / value dates */}
      <div className="grid grid-cols-2 gap-px bg-border-subtle">
        <div className="bg-bg-surface px-4 py-3">
          <p className="text-label uppercase tracking-wider text-text-muted">Spot Date</p>
          <p className="mt-1 font-mono text-data-lg font-bold text-accent">
            {formatIso(result.spotDate)}
          </p>
        </div>
        {result.valueDate && (
          <div className="bg-bg-surface px-4 py-3">
            <p className="text-label uppercase tracking-wider text-text-muted">Value Date</p>
            <p className="mt-1 font-mono text-data-lg font-bold text-accent">
              {formatIso(result.valueDate)}
            </p>
          </div>
        )}
      </div>

      {/* Convention detail */}
      {result.convention && (
        <div className="px-4 py-3 space-y-0">
          <p className="text-label uppercase tracking-wider text-text-muted mb-1">Convention</p>
          <DataRow label="Spot Lag" value={`T+${result.convention.spotLag}`} />
          <DataRow label="Roll Convention" value={result.convention.businessDayConvention} />
          <DataRow label="Day Count" value={result.convention.dayCount} />
        </div>
      )}
    </div>
  )
}
