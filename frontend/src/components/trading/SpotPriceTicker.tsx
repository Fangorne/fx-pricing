import { useEffect, useRef, useState } from 'react'
import { useSpotStream } from '@/hooks/useSpotStream'
import { Badge } from '@/components/ui/Badge'
import { Select } from '@/components/ui/Select'
import type { StreamStatus } from '@/types/fx'

const G10_PAIRS = [
  'EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'USD/CAD',
  'AUD/USD', 'NZD/USD', 'EUR/GBP', 'EUR/JPY', 'GBP/JPY',
  'EUR/CHF', 'EUR/CAD', 'EUR/AUD', 'EUR/NZD', 'GBP/CHF',
  'AUD/JPY', 'AUD/NZD', 'USD/SEK', 'USD/NOK',
]

const PIP_PRECISION: Record<string, number> = {
  'USD/JPY': 3, 'EUR/JPY': 3, 'GBP/JPY': 3, 'AUD/JPY': 3,
  'USD/SEK': 4, 'USD/NOK': 4,
}
function getPipPrecision(pair: string): number {
  return PIP_PRECISION[pair] ?? 5
}

function formatPrice(value: number, pair: string): string {
  return value.toFixed(getPipPrecision(pair))
}

const STATUS_BADGE: Record<StreamStatus, { variant: 'positive' | 'warning' | 'danger' | 'neutral'; label: string }> = {
  live:        { variant: 'positive', label: 'LIVE' },
  connecting:  { variant: 'warning',  label: 'CONNECTING' },
  error:       { variant: 'danger',   label: 'ERROR' },
  closed:      { variant: 'neutral',  label: 'RECONNECTING' },
}

interface SpotPriceTickerProps {
  defaultPair?: string
}

export function SpotPriceTicker({ defaultPair = 'EUR/USD' }: SpotPriceTickerProps) {
  const [pair, setPair] = useState(defaultPair)
  const { price, status } = useSpotStream(pair)

  const prevMidRef = useRef<number | null>(null)
  const [flashClass, setFlashClass] = useState('')
  const flashTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (price === null) return
    const prev = prevMidRef.current
    if (prev !== null && prev !== price.mid) {
      const cls = price.mid > prev ? 'price-flash-up' : 'price-flash-down'
      if (flashTimeoutRef.current) clearTimeout(flashTimeoutRef.current)
      setFlashClass('')
      // Force a reflow so the animation restarts
      requestAnimationFrame(() => {
        setFlashClass(cls)
        flashTimeoutRef.current = setTimeout(() => setFlashClass(''), 500)
      })
    }
    prevMidRef.current = price.mid
  }, [price?.mid])

  const badge = STATUS_BADGE[status]
  const prec = getPipPrecision(pair)

  return (
    <div className="rounded-lg border border-border-default bg-bg-surface p-6 space-y-6">
      {/* Header row */}
      <div className="flex items-center justify-between">
        <Select
          options={G10_PAIRS.map((p) => ({ value: p, label: p }))}
          value={pair}
          onChange={(e) => setPair(e.target.value)}
          className="w-36 text-base font-mono font-bold"
        />
        <Badge variant={badge.variant} dot>
          {badge.label}
        </Badge>
      </div>

      {/* Price display */}
      {status === 'connecting' && price === null ? (
        <div className="space-y-3 animate-pulse">
          <div className="h-12 w-48 rounded-md bg-bg-elevated" />
          <div className="flex gap-8">
            <div className="h-6 w-24 rounded-md bg-bg-elevated" />
            <div className="h-6 w-24 rounded-md bg-bg-elevated" />
            <div className="h-6 w-24 rounded-md bg-bg-elevated" />
          </div>
        </div>
      ) : price ? (
        <div className={`rounded-md p-3 transition-colors ${flashClass}`}>
          {/* Mid — large */}
          <div className="font-mono text-5xl font-bold tracking-tight text-text-primary leading-none">
            {formatPrice(price.mid, pair)}
          </div>

          {/* Bid / Ask row */}
          <div className="mt-3 flex gap-8">
            <div>
              <div className="text-label uppercase tracking-wider text-text-muted mb-1">Bid</div>
              <div className="font-mono text-lg font-semibold text-negative">
                {formatPrice(price.bid, pair)}
              </div>
            </div>
            <div>
              <div className="text-label uppercase tracking-wider text-text-muted mb-1">Ask</div>
              <div className="font-mono text-lg font-semibold text-positive">
                {formatPrice(price.ask, pair)}
              </div>
            </div>
            <div>
              <div className="text-label uppercase tracking-wider text-text-muted mb-1">Spread</div>
              <div className="font-mono text-lg font-semibold text-text-secondary">
                {((price.ask - price.bid) * 10 ** prec).toFixed(1)} pips
              </div>
            </div>
          </div>

          {/* Metadata row */}
          <div className="mt-3 flex items-center gap-3 text-xs text-text-muted font-mono">
            <span>{new Date(price.timestamp).toLocaleTimeString()} UTC</span>
            <span>·</span>
            <span>{price.age_seconds.toFixed(1)}s ago</span>
            {price.is_stale && (
              <>
                <span>·</span>
                <span className="text-warning">⚠ stale</span>
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="text-text-muted text-sm font-mono">Waiting for data…</div>
      )}
    </div>
  )
}
