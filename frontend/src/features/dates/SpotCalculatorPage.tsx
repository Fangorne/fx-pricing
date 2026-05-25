import { useState, useEffect, useRef } from 'react'
import { useSpotDate } from '@/hooks/useSpotDate'
import { DateResult } from './DateResult'
import type { SpotDateCalcResult } from '@/hooks/useSpotDate'
import { Alert } from '@/components/ui/Alert'
import { Skeleton } from '@/components/ui/Skeleton'
import { FieldLabel } from '@/components/ui/FieldLabel'
import { formatIso } from '@/utils/dates'

const PAIRS = [
  'EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD',
  'AUD/USD', 'NZD/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CHF',
  'GBP/JPY', 'AUD/JPY',
]

const TENORS = ['ON', 'TN', '1W', '2W', '1M', '2M', '3M', '6M', '9M', '1Y']

const TODAY = new Date().toISOString().slice(0, 10)

const selectClass =
  'form-control font-mono cursor-pointer'

function parseCommand(input: string): { pair?: string; date?: string; tenor?: string } {
  const clean = input.trim().toUpperCase().replace('/', '')
  const pairMatch = clean.match(/^([A-Z]{6})/)
  const dateMatch = clean.match(/(\d{4}-\d{2}-\d{2})/)
  const tenorMatch = clean.match(/\b(\d+[DWMY])\b/)
  return {
    pair: pairMatch?.[1] ? pairMatch[1].slice(0, 3) + '/' + pairMatch[1].slice(3) : undefined,
    date: dateMatch?.[1],
    tenor: tenorMatch?.[1],
  }
}

export function SpotCalculatorPage() {
  const [pair, setPair] = useState('EUR/USD')
  const [tradeDate, setTradeDate] = useState(TODAY)
  const [tenor, setTenor] = useState('3M')
  const [history, setHistory] = useState<SpotDateCalcResult[]>([])
  const [commandInput, setCommandInput] = useState('')
  const [commandError, setCommandError] = useState<string | null>(null)
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)

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

  function applyCommand(raw: string) {
    const parsed = parseCommand(raw)
    if (!parsed.pair || !parsed.tenor) {
      setCommandError('Pair and tenor required — e.g. EURUSD 3M')
      return
    }
    if (!PAIRS.includes(parsed.pair)) {
      setCommandError(`Unknown pair: ${parsed.pair}`)
      return
    }
    if (!TENORS.includes(parsed.tenor)) {
      setCommandError(`Unknown tenor: ${parsed.tenor} — valid: ${TENORS.join(', ')}`)
      return
    }
    setCommandError(null)
    setPair(parsed.pair)
    if (parsed.date) setTradeDate(parsed.date)
    setTenor(parsed.tenor)
  }

  function handleCommandChange(value: string) {
    setCommandInput(value)
    setCommandError(null)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      if (value.trim()) applyCommand(value)
    }, 400)
  }

  function handleCommandKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') {
      if (debounceRef.current) clearTimeout(debounceRef.current)
      applyCommand(commandInput)
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-4 px-6 py-6">
      {/* Page header */}
      <div className="border-b border-border-subtle pb-2">
        <span className="text-label uppercase tracking-wider text-text-muted">
          Spot / Value Date Calculator
        </span>
      </div>

      {/* Command input */}
      <div className="rounded-lg border border-border-default bg-bg-surface">
        <div className="border-b border-border-subtle px-4 py-2">
          <span className="text-label uppercase tracking-wider text-text-muted">Quick Input</span>
        </div>
        <div className="px-4 py-3 space-y-2">
          <input
            type="text"
            value={commandInput}
            onChange={(e) => handleCommandChange(e.target.value)}
            onKeyDown={handleCommandKeyDown}
            placeholder="EURUSD 3M  or  GBPUSD 2026-06-01 1M"
            className="form-control font-mono text-sm"
            aria-label="Quick command input"
          />
          {commandError ? (
            <p className="text-xs text-negative">{commandError}</p>
          ) : (
            <p className="text-xs text-text-muted">
              Pair + tenor required · date optional (defaults to today) · press Enter or wait
            </p>
          )}
        </div>
      </div>

      {/* Manual form */}
      <div className="rounded-lg border border-border-default bg-bg-surface">
        <div className="border-b border-border-subtle px-4 py-2">
          <span className="text-label uppercase tracking-wider text-text-muted">Manual Selection</span>
        </div>
        <div className="grid gap-4 px-4 py-3 sm:grid-cols-3">
          <div>
            <FieldLabel htmlFor="calc-pair">FX Pair</FieldLabel>
            <select
              id="calc-pair"
              value={pair}
              onChange={(e) => setPair(e.target.value)}
              className={selectClass}
            >
              {PAIRS.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <div>
            <FieldLabel htmlFor="calc-trade-date">Trade Date</FieldLabel>
            <input
              id="calc-trade-date"
              type="date"
              value={tradeDate}
              onChange={(e) => setTradeDate(e.target.value)}
              className={selectClass}
            />
          </div>

          <div>
            <FieldLabel htmlFor="calc-tenor">Tenor</FieldLabel>
            <select
              id="calc-tenor"
              value={tenor}
              onChange={(e) => setTenor(e.target.value)}
              className={selectClass}
            >
              {TENORS.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading && (
        <Skeleton lines={4} className="rounded-lg border border-border-default bg-bg-surface p-4" />
      )}

      {error && !loading && <Alert variant="error">{error}</Alert>}

      {result && !loading && <DateResult result={result} />}

      {/* History */}
      {history.length > 0 && (
        <div className="rounded-lg border border-border-subtle bg-bg-surface overflow-hidden">
          <div className="border-b border-border-subtle px-4 py-2">
            <span className="text-label uppercase tracking-wider text-text-muted">Recent Calculations</span>
          </div>
          <div className="divide-y divide-border-subtle">
            {history.map((h, i) => (
              <div
                key={i}
                className="flex items-center justify-between px-4 py-2.5 text-sm transition-colors duration-[100ms] hover:bg-bg-elevated"
              >
                <div className="flex items-center gap-3">
                  <span className="font-mono font-semibold text-accent">{h.pair}</span>
                  <span className="font-mono text-xs text-text-muted">
                    {formatIso(h.tradeDate)} &middot; {h.tenor}
                  </span>
                </div>
                <div className="flex gap-4 font-mono text-xs text-text-secondary">
                  <span>Spot {formatIso(h.spotDate)}</span>
                  {h.valueDate && <span>Val {formatIso(h.valueDate)}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
