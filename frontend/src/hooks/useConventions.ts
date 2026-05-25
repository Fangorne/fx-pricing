import { useEffect, useState } from 'react'
import { fetchConventions, fetchConvention } from '@/services/api'
import type { FXConvention } from '@/types/fx'

interface UseConventionsResult {
  conventions: FXConvention[]
  loading: boolean
  error: string | null
}

export function useConventions(): UseConventionsResult {
  const [conventions, setConventions] = useState<FXConvention[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchConventions()
      .then((data) => {
        if (!cancelled) setConventions(data)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : 'API unavailable')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  return { conventions, loading, error }
}

interface UseConventionDetailResult {
  convention: FXConvention | null
  loading: boolean
  error: string | null
}

export function useConventionDetail(pair: string | undefined): UseConventionDetailResult {
  const [convention, setConvention] = useState<FXConvention | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!pair) {
      setConvention(null)
      return
    }
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchConvention(pair)
      .then((data) => {
        if (!cancelled) setConvention(data)
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          const msg = err instanceof Error ? err.message : 'Not found'
          setError(msg.includes('404') ? 'Convention not found' : msg)
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [pair])

  return { convention, loading, error }
}
