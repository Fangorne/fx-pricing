import { useConventionDetail } from '@/hooks/useConventions'

interface Props {
  pair: string
}

interface RowProps {
  label: string
  value: string | number
}

function Row({ label, value }: RowProps) {
  return (
    <div className="flex justify-between border-b border-gray-800 py-3">
      <span className="text-gray-400">{label}</span>
      <span className="font-mono text-gray-100">{value}</span>
    </div>
  )
}

export function ConventionDetail({ pair }: Props) {
  const { convention, loading, error } = useConventionDetail(pair)

  if (loading) {
    return (
      <div className="animate-pulse space-y-3 rounded-lg border border-gray-800 bg-gray-900 p-6">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-8 rounded bg-gray-800" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-800 bg-red-950 p-6 text-red-400">{error}</div>
    )
  }

  if (!convention) return null

  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-6">
      <h2 className="mb-4 font-mono text-xl font-bold text-blue-400">{convention.pair}</h2>
      <div className="space-y-1">
        <Row label="Spot Lag" value={`T+${convention.spotLag}`} />
        <Row label="Day Count Basis" value={convention.dayCount} />
        <Row label="Roll Convention" value={convention.businessDayConvention} />
        <Row label="Pip Precision" value={convention.pricingPrecision} />
        <Row label="Pip Size" value={convention.pipSize} />
      </div>
    </div>
  )
}
