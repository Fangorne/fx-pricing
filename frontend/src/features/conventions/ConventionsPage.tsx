import { useState, useMemo } from 'react'
import { useConventions } from '@/hooks/useConventions'
import { ConventionsList } from './ConventionsList'
import { Alert } from '@/components/ui/Alert'
import { Skeleton } from '@/components/ui/Skeleton'
import { Badge } from '@/components/ui/Badge'

export function ConventionsPage() {
  const [search, setSearch] = useState('')
  const { conventions, loading, error } = useConventions()

  const filtered = useMemo(() => {
    const q = search.trim().toUpperCase()
    if (!q) return conventions
    return conventions.filter((c) => c.pair.replace('/', '').includes(q))
  }, [conventions, search])

  return (
    <div className="space-y-4 px-6 py-6">
      {/* Page header */}
      <div className="flex items-center justify-between border-b border-border-subtle pb-2">
        <span className="text-label uppercase tracking-wider text-text-muted">FX Conventions</span>
        {conventions.length > 0 && (
          <Badge variant="neutral">{filtered.length} pairs</Badge>
        )}
      </div>

      {/* Search */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <input
            type="search"
            placeholder="Filter pair — EUR, USD, JPY…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Filter currency pairs"
            className="form-control font-mono"
          />
        </div>
        {search && (
          <button
            onClick={() => setSearch('')}
            className="text-xs text-text-muted hover:text-text-secondary transition-colors"
          >
            Clear
          </button>
        )}
      </div>

      {error && <Alert variant="error">API unavailable — {error}</Alert>}

      {loading ? <Skeleton lines={10} /> : <ConventionsList conventions={filtered} />}
    </div>
  )
}
