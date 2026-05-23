import type { SpotDateCalcResult } from '@/hooks/useSpotDate'

interface Props {
  result: SpotDateCalcResult
}

function formatDate(iso: string): string {
  return new Date(iso + 'T00:00:00').toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

interface RowProps {
  label: string
  value: string
  highlight?: boolean
}

function Row({ label, value, highlight }: RowProps) {
  return (
    <div className="flex items-center justify-between border-b border-gray-800 py-3">
      <span className="text-gray-400 text-sm">{label}</span>
      <span
        className={`font-mono font-semibold ${highlight ? 'text-blue-400 text-lg' : 'text-gray-100'}`}
      >
        {value}
      </span>
    </div>
  )
}

export function DateResult({ result }: Props) {
  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-6 space-y-1">
      <div className="flex items-center gap-3 mb-4">
        <span className="font-mono text-lg font-bold text-blue-400">{result.pair}</span>
        <span className="text-gray-500 text-sm">
          Trade: {formatDate(result.tradeDate)} · Ténor: {result.tenor}
        </span>
      </div>

      <Row label="Spot Date" value={formatDate(result.spotDate)} highlight />
      {result.valueDate && (
        <Row label="Value Date" value={formatDate(result.valueDate)} highlight />
      )}

      {result.convention && (
        <>
          <div className="pt-3">
            <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">Convention</p>
          </div>
          <Row label="Spot Lag" value={`T+${result.convention.spotLag}`} />
          <Row label="Roll Convention" value={result.convention.businessDayConvention} />
          <Row label="Day Count" value={result.convention.dayCount} />
        </>
      )}
    </div>
  )
}
