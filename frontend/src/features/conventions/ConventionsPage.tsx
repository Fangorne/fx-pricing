import { useState, useMemo } from 'react'
import { useParams } from 'react-router-dom'
import { useConventions } from '@/hooks/useConventions'
import { ConventionsList } from './ConventionsList'
import { ConventionDetail } from './ConventionDetail'

export function ConventionsPage() {
  const { pair } = useParams<{ pair?: string }>()
  const selectedPair = pair ? decodeURIComponent(pair) : undefined

  const [search, setSearch] = useState('')
  const { conventions, loading, error } = useConventions()

  const filtered = useMemo(() => {
    const q = search.trim().toUpperCase()
    if (!q) return conventions
    return conventions.filter((c) => c.pair.replace('/', '').includes(q))
  }, [conventions, search])

  return (
    <div className="mx-auto max-w-6xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-100">FX Conventions</h1>
        <span className="text-sm text-gray-500">{conventions.length} paires G10</span>
      </div>

      <input
        type="search"
        placeholder="Filtrer par paire (ex: EUR, USD…)"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
      />

      {error && (
        <div className="rounded-lg border border-red-800 bg-red-950 px-4 py-3 text-red-400">
          API inaccessible — {error}
        </div>
      )}

      {loading ? (
        <div className="animate-pulse space-y-2">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-10 rounded bg-gray-800" />
          ))}
        </div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2">
          <ConventionsList conventions={filtered} selectedPair={selectedPair} />
          {selectedPair && <ConventionDetail pair={selectedPair} />}
        </div>
      )}
    </div>
  )
}
