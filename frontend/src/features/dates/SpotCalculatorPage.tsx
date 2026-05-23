import { useState, useEffect } from 'react'
import { useSpotDate } from '@/hooks/useSpotDate'
import { DateResult } from './DateResult'
import type { SpotDateCalcResult } from '@/hooks/useSpotDate'

const PAIRS = [
  'EUR/USD',
  'USD/JPY',
  'GBP/USD',
  'USD/CHF',
  'USD/CAD',
  'AUD/USD',
  'NZD/USD',
  'EUR/GBP',
  'EUR/JPY',
  'EUR/CHF',
  'GBP/JPY',
  'AUD/JPY',
]

const TENORS = ['ON', 'TN', '1W', '2W', '1M', '2M', '3M', '6M', '9M', '1Y']

const TODAY = new Date().toISOString().slice(0, 10)

function formatDate(iso: string): string {
  return new Date(iso + 'T00:00:00').toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

export function SpotCalculatorPage() {
  const [pair, setPair] = useState('EUR/USD')
  const [tradeDate, setTradeDate] = useState(TODAY)
  const [tenor, setTenor] = useState('3M')
  const [history, setHistory] = useState<SpotDateCalcResult[]>([])

  const { result, loading, error } = useSpotDate(pair, tradeDate, tenor)

  useEffect(() => {
    if (!result) return
    setHistory((prev) => {
      const key = `${result.pair}|${result.tradeDate}|${result.tenor}`
      const prevKey = prev[0] ? `${prev[0].pair}|${prev[0].tradeDate}|${prev[0].tenor}` : null
      if (key === prevKey) return prev
      return [result, ...prev].slice(0, 5)
    })
  }, [result])

  const selectClass =
    'rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 focus:border-blue-500 focus:outline-none w-full'

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <h1 className="text-2xl font-bold text-gray-100">Calculateur Spot / Value Date</h1>

      {/* Form */}
      <div className="rounded-lg border border-gray-800 bg-gray-900 p-6">
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-1">
            <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
              Paire FX
            </label>
            <select value={pair} onChange={(e) => setPair(e.target.value)} className={selectClass}>
              {PAIRS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
              Trade Date
            </label>
            <input
              type="date"
              value={tradeDate}
              onChange={(e) => setTradeDate(e.target.value)}
              className={selectClass}
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
              Ténor
            </label>
            <select
              value={tenor}
              onChange={(e) => setTenor(e.target.value)}
              className={selectClass}
            >
              {TENORS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Result */}
      {loading && (
        <div className="animate-pulse rounded-lg border border-gray-800 bg-gray-900 p-6 space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-8 rounded bg-gray-800" />
          ))}
        </div>
      )}

      {error && !loading && (
        <div className="rounded-lg border border-red-800 bg-red-950 px-4 py-3 text-red-400">
          {error}
        </div>
      )}

      {result && !loading && <DateResult result={result} />}

      {/* History */}
      {history.length > 0 && (
        <div className="space-y-2">
          <h2 className="text-sm font-medium uppercase tracking-wide text-gray-500">
            Derniers calculs
          </h2>
          <div className="divide-y divide-gray-800 rounded-lg border border-gray-800">
            {history.map((h, i) => (
              <div
                key={i}
                className="flex items-center justify-between px-4 py-3 text-sm hover:bg-gray-800/50"
              >
                <div className="flex items-center gap-3">
                  <span className="font-mono font-semibold text-blue-400">{h.pair}</span>
                  <span className="text-gray-500">
                    {formatDate(h.tradeDate)} · {h.tenor}
                  </span>
                </div>
                <div className="flex gap-4 text-gray-300">
                  <span>Spot: {formatDate(h.spotDate)}</span>
                  {h.valueDate && <span>Value: {formatDate(h.valueDate)}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
