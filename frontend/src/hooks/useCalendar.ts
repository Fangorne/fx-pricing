import { useEffect, useState } from 'react'
import { fetchHolidays, checkBusinessDay } from '@/services/api'
import type { CalendarHoliday, BusinessDayCheckResult } from '@/types/fx'

interface UseCalendarResult {
  holidays: CalendarHoliday[]
  loading: boolean
  error: string | null
}

export function useCalendar(currency: string, year: number): UseCalendarResult {
  const [holidays, setHolidays] = useState<CalendarHoliday[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!currency) return
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchHolidays(currency, year)
      .then((data) => {
        if (!cancelled) setHolidays(data)
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
  }, [currency, year])

  return { holidays, loading, error }
}

interface UseBusinessDayResult {
  result: BusinessDayCheckResult | null
  loading: boolean
  error: string | null
}

export function useBusinessDay(currency: string, date: string): UseBusinessDayResult {
  const [result, setResult] = useState<BusinessDayCheckResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!date || !currency) {
      setResult(null)
      return
    }

    // Client-side weekend detection — skip API call
    const d = new Date(date + 'T00:00:00')
    const dow = d.getDay()
    if (dow === 0 || dow === 6) {
      setResult({
        date,
        currency,
        is_business_day: false,
        reason: 'Weekend',
      })
      return
    }

    let cancelled = false
    const timer = setTimeout(() => {
      setLoading(true)
      setError(null)
      checkBusinessDay(currency, date)
        .then((data) => {
          if (!cancelled) setResult(data)
        })
        .catch((err: unknown) => {
          if (!cancelled) setError(err instanceof Error ? err.message : 'API unavailable')
        })
        .finally(() => {
          if (!cancelled) setLoading(false)
        })
    }, 300)

    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [currency, date])

  return { result, loading, error }
}
