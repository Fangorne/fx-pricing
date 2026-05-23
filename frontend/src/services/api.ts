import type {
  FXConvention,
  CalendarHoliday,
  SpotDateResult,
  BusinessDayCheckResult,
} from '@/types/fx'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`)
  return res.json() as Promise<T>
}

// Backend returns snake_case — map to camelCase FXConvention
interface RawConvention {
  pair: string
  spot_lag: number
  day_count: string
  roll_convention: string
  pip_precision: number
  quotation_side: string
}

function mapConvention(raw: RawConvention): FXConvention {
  return {
    pair: raw.pair,
    baseCurrency: raw.pair.split('/')[0] ?? raw.pair.slice(0, 3),
    quoteCurrency: raw.pair.split('/')[1] ?? raw.pair.slice(3),
    spotLag: raw.spot_lag,
    settlementCalendars: [raw.pair.split('/')[0] ?? '', raw.pair.split('/')[1] ?? ''].filter(
      Boolean,
    ),
    dayCount: raw.day_count as FXConvention['dayCount'],
    businessDayConvention: raw.roll_convention as FXConvention['businessDayConvention'],
    pricingPrecision: raw.pip_precision,
    pipSize: Math.pow(10, -raw.pip_precision),
  }
}

export function fetchConventions(): Promise<FXConvention[]> {
  return get<RawConvention[]>('/api/v1/conventions').then((data) => data.map(mapConvention))
}

export function fetchConvention(pair: string): Promise<FXConvention> {
  return get<RawConvention>(`/api/v1/conventions/${encodeURIComponent(pair)}`).then(mapConvention)
}

export function fetchHolidays(currency: string, year: number): Promise<CalendarHoliday[]> {
  return get(`/api/v1/calendars/${currency}/holidays?year=${year}`)
}

export function checkBusinessDay(currency: string, date: string): Promise<BusinessDayCheckResult> {
  return get(`/api/v1/calendars/${currency}/business-day?date=${date}`)
}

export function calculateSpotDate(pair: string, tradeDate: string): Promise<SpotDateResult> {
  return get(`/api/v1/spot-dates?pair=${encodeURIComponent(pair)}&trade_date=${tradeDate}`)
}

export function calculateValueDate(
  pair: string,
  tradeDate: string,
  tenor: string,
): Promise<SpotDateResult> {
  return get(
    `/api/v1/spot-dates/value?pair=${encodeURIComponent(pair)}&trade_date=${tradeDate}&tenor=${tenor}`,
  )
}
