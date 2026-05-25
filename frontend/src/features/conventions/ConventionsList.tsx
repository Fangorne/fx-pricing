import type { FXConvention } from '@/types/fx'

interface Props {
  conventions: FXConvention[]
}

export function ConventionsList({ conventions }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border-default">
      <table className="data-table">
        <thead>
          <tr>
            <th scope="col">Pair</th>
            <th scope="col" className="text-center">Spot Lag</th>
            <th scope="col">Day Count</th>
            <th scope="col">Roll Convention</th>
            <th scope="col" className="text-right">Pip Size</th>
            <th scope="col" className="text-center">Precision</th>
            <th scope="col">Calendars</th>
          </tr>
        </thead>
        <tbody>
          {conventions.map((c) => (
            <tr key={c.pair}>
              <td className="font-mono font-semibold text-text-primary">{c.pair}</td>
              <td className="text-center font-mono text-text-secondary">T+{c.spotLag}</td>
              <td className="font-mono text-text-secondary">{c.dayCount}</td>
              <td className="font-mono text-text-secondary">{c.businessDayConvention}</td>
              <td className="text-right font-mono text-text-secondary">{c.pipSize}</td>
              <td className="text-center font-mono text-text-secondary">{c.pricingPrecision}</td>
              <td className="font-mono text-text-muted">{c.settlementCalendars.join(', ')}</td>
            </tr>
          ))}
          {conventions.length === 0 && (
            <tr>
              <td colSpan={7} className="px-3 py-10 text-center text-text-muted">
                No pairs found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
