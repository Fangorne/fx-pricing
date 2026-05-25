import { PageHeader } from '@/components/layout/PageHeader'
import { SpotPriceTicker } from '@/components/trading/SpotPriceTicker'

export function LivePricesPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Live Prices"
        description="Real-time FX spot prices streamed via WebSocket. Updates every 5 seconds."
        compact
      />
      <div className="max-w-lg">
        <SpotPriceTicker defaultPair="EUR/USD" />
      </div>
    </div>
  )
}
