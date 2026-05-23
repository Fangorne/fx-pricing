import { Link } from 'react-router-dom'
import type { FXConvention } from '@/types/fx'

interface Props {
  conventions: FXConvention[]
  selectedPair?: string
}

export function ConventionsList({ conventions, selectedPair }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-800">
      <table className="w-full text-sm">
        <thead className="bg-gray-900 text-gray-400">
          <tr>
            <th className="px-4 py-3 text-left font-medium">Pair</th>
            <th className="px-4 py-3 text-left font-medium">Spot Lag</th>
            <th className="px-4 py-3 text-left font-medium">Day Count</th>
            <th className="px-4 py-3 text-left font-medium">Pip Precision</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {conventions.map((c) => {
            const isSelected = c.pair === selectedPair
            return (
              <tr
                key={c.pair}
                className={`cursor-pointer transition-colors hover:bg-gray-800 ${
                  isSelected ? 'bg-gray-800' : ''
                }`}
              >
                <td className="px-4 py-3">
                  <Link
                    to={`/conventions/${encodeURIComponent(c.pair)}`}
                    className="font-mono font-semibold text-blue-400 hover:text-blue-300"
                  >
                    {c.pair}
                  </Link>
                </td>
                <td className="px-4 py-3 text-gray-300">T+{c.spotLag}</td>
                <td className="px-4 py-3 text-gray-300">{c.dayCount}</td>
                <td className="px-4 py-3 text-gray-300">{c.pricingPrecision}</td>
              </tr>
            )
          })}
          {conventions.length === 0 && (
            <tr>
              <td colSpan={4} className="px-4 py-8 text-center text-gray-500">
                Aucune paire trouvée
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
