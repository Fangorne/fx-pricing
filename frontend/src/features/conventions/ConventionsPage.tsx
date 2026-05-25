import { useState, useMemo } from 'react'
import { useConventions } from '@/hooks/useConventions'
import { ConventionsList } from './ConventionsList'
import { ConventionDetail } from './ConventionDetail'
import { Alert } from '@/components/ui/Alert'
import { Skeleton } from '@/components/ui/Skeleton'
import { Badge } from '@/components/ui/Badge'
import { PageHeader } from '@/components/layout/PageHeader'

export function ConventionsPage() {
  const [search, setSearch] = useState('')
  const [selectedPair, setSelectedPair] = useState<string | null>(null)
  const { conventions, loading, error } = useConventions()

  const filtered = useMemo(() => {
    const q = search.trim().toUpperCase()
    if (!q) return conventions
    return conventions.filter((c) => c.pair.replace('/', '').includes(q))
  }, [conventions, search])

  return (
    <div className="space-y-4 px-6 py-6">
      <PageHeader
        title="FX Conventions"
        compact
        badge={conventions.length > 0 ? <Badge variant="neutral">{filtered.length} pairs</Badge> : undefined}
      />

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
            className="text-xs text-text-muted hover:text-text-secondary transition-colors duration-[100ms]"
          >
            Clear
          </button>
        )}
        {selectedPair && (
          <button
            onClick={() => setSelectedPair(null)}
            className="ml-auto text-xs text-text-muted hover:text-text-secondary transition-colors duration-[100ms]"
          >
            Close detail ×
          </button>
        )}
      </div>

      {error && <Alert variant="error">API unavailable — {error}</Alert>}

      {loading ? (
        <Skeleton lines={10} />
      ) : (
        <div className={`grid gap-4 ${selectedPair ? 'lg:grid-cols-[1fr_320px]' : ''}`}>
          <ConventionsList
            conventions={filtered}
            selectedPair={selectedPair}
            onSelectPair={setSelectedPair}
          />
          {selectedPair && (
            <div className="self-start">
              <ConventionDetail pair={selectedPair} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
