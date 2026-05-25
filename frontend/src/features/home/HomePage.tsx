import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Badge } from '@/components/ui/Badge'
import { ArrowLeftRight, CalendarDays, Calculator } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

interface ApiStatus {
  status: 'online' | 'offline' | 'checking'
}

function useApiHealth(): ApiStatus {
  const [status, setStatus] = useState<ApiStatus['status']>('checking')

  useEffect(() => {
    let cancelled = false
    fetch(`${BASE_URL}/api/v1/conventions`)
      .then((res) => {
        if (!cancelled) setStatus(res.ok ? 'online' : 'offline')
      })
      .catch(() => {
        if (!cancelled) setStatus('offline')
      })
    return () => { cancelled = true }
  }, [])

  return { status }
}

interface FeatureCard {
  title: string
  description: string
  to: string
  label: string
  icon: LucideIcon
}

const FEATURES: FeatureCard[] = [
  {
    title: 'FX Conventions',
    description: 'Spot lag, day count basis, roll convention, and pip precision for all G10 pairs.',
    to: '/conventions',
    label: 'Browse conventions',
    icon: ArrowLeftRight,
  },
  {
    title: 'Market Calendars',
    description: 'Holiday calendars for each G10 currency. Verify business day status for any date.',
    to: '/calendars',
    label: 'View calendars',
    icon: CalendarDays,
  },
  {
    title: 'Date Calculator',
    description: 'Compute spot and value dates for any pair, trade date, and tenor with market conventions.',
    to: '/dates',
    label: 'Open calculator',
    icon: Calculator,
  },
]

const STATS = [
  { value: '45', label: 'currency pairs' },
  { value: '10', label: 'market calendars' },
  { value: 'G10', label: 'coverage' },
]

export function HomePage() {
  const { status } = useApiHealth()

  const statusBadge =
    status === 'checking' ? (
      <Badge variant="neutral" dot>Connecting</Badge>
    ) : status === 'online' ? (
      <Badge variant="positive" dot>API Online</Badge>
    ) : (
      <Badge variant="negative" dot>API Offline</Badge>
    )

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-6 py-6">
      {/* Header */}
      <div className="flex items-start justify-between border-b border-border-subtle pb-4">
        <div>
          <h1 className="font-mono text-data-lg font-bold text-text-primary">FX Pricing Platform</h1>
          <p className="mt-1 text-sm text-text-secondary">
            Institutional-grade reference data · G10 currency pairs
          </p>
        </div>
        {statusBadge}
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-3 gap-px rounded-lg border border-border-subtle bg-border-subtle overflow-hidden">
        {STATS.map((stat) => (
          <div key={stat.label} className="bg-bg-surface px-5 py-4">
            <p className="font-mono text-data-xl font-bold text-text-primary">{stat.value}</p>
            <p className="mt-0.5 text-label uppercase tracking-wider text-text-muted">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Feature cards */}
      <div className="grid gap-3 sm:grid-cols-3">
        {FEATURES.map((feature) => {
          const Icon = feature.icon
          return (
            <div
              key={feature.to}
              className="group rounded-lg border border-border-default bg-bg-surface p-4 transition-colors duration-[150ms] hover:border-border-strong"
            >
              <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-md bg-bg-elevated">
                <Icon size={15} className="text-accent" />
              </div>
              <h2 className="text-sm font-semibold text-text-primary">{feature.title}</h2>
              <p className="mt-1.5 text-xs leading-relaxed text-text-secondary">{feature.description}</p>
              <div className="mt-4">
                <Link
                  to={feature.to}
                  className="text-xs font-semibold text-accent transition-colors duration-[100ms] hover:text-accent-hover"
                >
                  {feature.label} →
                </Link>
              </div>
            </div>
          )
        })}
      </div>

      {/* Quick reference */}
      <div className="rounded-lg border border-border-subtle bg-bg-surface">
        <div className="border-b border-border-subtle px-4 py-2">
          <span className="text-label uppercase tracking-wider text-text-muted">Quick Reference</span>
        </div>
        <div className="grid grid-cols-2 gap-px bg-border-subtle sm:grid-cols-4">
          {[
            { pair: 'EUR/USD', spot: 'T+2', basis: 'Act/360' },
            { pair: 'USD/JPY', spot: 'T+2', basis: 'Act/360' },
            { pair: 'GBP/USD', spot: 'T+2', basis: 'Act/365' },
            { pair: 'USD/CHF', spot: 'T+2', basis: 'Act/360' },
          ].map((row) => (
            <Link
              key={row.pair}
              to="/conventions"
              className="bg-bg-surface px-4 py-3 transition-colors duration-[100ms] hover:bg-bg-elevated"
            >
              <p className="font-mono text-sm font-semibold text-accent">{row.pair}</p>
              <p className="mt-1 text-label text-text-muted">
                {row.spot} &middot; {row.basis}
              </p>
            </Link>
          ))}
        </div>
        <div className="border-t border-border-subtle px-4 py-2">
          <span className="text-label uppercase tracking-wider text-text-muted">
            Press <kbd className="rounded border border-border-default bg-bg-elevated px-1 font-mono text-[10px] text-text-secondary">?</kbd> for keyboard shortcuts
          </span>
        </div>
      </div>
    </div>
  )
}
