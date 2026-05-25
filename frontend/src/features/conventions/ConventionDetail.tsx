import { useConventionDetail } from '@/hooks/useConventions'
import { Panel } from '@/components/ui/Panel'
import { Skeleton } from '@/components/ui/Skeleton'
import { Alert } from '@/components/ui/Alert'

interface Props {
  pair: string
}

interface RowProps {
  label: string
  value: string | number
}

function Row({ label, value }: RowProps) {
  return (
    <div className="flex items-center justify-between border-b border-border-subtle py-2.5">
      <span className="text-xs text-text-secondary">{label}</span>
      <span className="font-mono text-sm font-semibold text-text-primary">{value}</span>
    </div>
  )
}

export function ConventionDetail({ pair }: Props) {
  const { convention, loading, error } = useConventionDetail(pair)

  if (loading) {
    return (
      <Panel>
        <Skeleton lines={5} />
      </Panel>
    )
  }

  if (error) {
    return <Alert variant="error">{error}</Alert>
  }

  if (!convention) return null

  return (
    <Panel>
      <p className="text-label uppercase tracking-wider text-text-muted mb-3">Convention detail</p>
      <p className="font-mono text-data-lg font-bold text-accent mb-4">{convention.pair}</p>
      <div>
        <Row label="Spot Lag" value={`T+${convention.spotLag}`} />
        <Row label="Day Count Basis" value={convention.dayCount} />
        <Row label="Roll Convention" value={convention.businessDayConvention} />
        <Row label="Pip Precision" value={convention.pricingPrecision} />
        <Row label="Pip Size" value={convention.pipSize} />
      </div>
    </Panel>
  )
}
