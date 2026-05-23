import { useEffect, useState } from 'react'
import { calculateSpotDate, calculateValueDate, fetchConvention } from '@/services/api'
import type { FXConvention, SpotDateResult } from '@/types/fx'

export interface SpotDateCalcResult {
  pair: string
  tradeDate: string
  tenor: string
  spotDate: string
  valueDate: string | null
  convention: FXConvention | null
}

interface UseSpotDateResult {
  result: SpotDateCalcResult | null
  loading: boolean
  error: string | null
}

export function useSpotDate(pair: string, tradeDate: string, tenor: string): UseSpotDateResult {
  const [result, setResult] = useState<SpotDateCalcResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!pair || !tradeDate || !tenor) {
      setResult(null)
      setError(null)
      return
    }

    let cancelled = false
    const timer = setTimeout(() => {
      setLoading(true)
      setError(null)

      const spotPromise = calculateSpotDate(pair, tradeDate)
      const valuePromise = calculateValueDate(pair, tradeDate, tenor)
      const convPromise = fetchConvention(pair)

      Promise.allSettled([spotPromise, valuePromise, convPromise]).then(
        ([spotRes, valueRes, convRes]) => {
          if (cancelled) return

          if (spotRes.status === 'rejected') {
            const msg =
              spotRes.reason instanceof Error ? spotRes.reason.message : 'Calcul impossible'
            setError(msg)
            setLoading(false)
            return
          }

          const spotData = spotRes.value as SpotDateResult
          const valueDate =
            valueRes.status === 'fulfilled'
              ? ((valueRes.value as SpotDateResult).value_date ?? null)
              : null
          const convention = convRes.status === 'fulfilled' ? convRes.value : null

          setResult({
            pair,
            tradeDate,
            tenor,
            spotDate: spotData.spot_date,
            valueDate,
            convention,
          })
          setLoading(false)
        },
      )
    }, 300)

    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [pair, tradeDate, tenor])

  return { result, loading, error }
}
