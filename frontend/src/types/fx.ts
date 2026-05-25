export type Currency = string

export interface CurrencyPair {
  base: Currency
  quote: Currency
  symbol: string
}

export type DayCountConvention = 'Act/360' | 'Act/365' | 'Act/Act' | '30/360'

export type BusinessDayConvention =
  | 'FOLLOWING'
  | 'MODIFIED_FOLLOWING'
  | 'PRECEDING'
  | 'MODIFIED_PRECEDING'
  | 'END_OF_MONTH'

export type SettlementConvention = 'T+0' | 'T+1' | 'T+2' | 'T+3'

export interface FXConvention {
  pair: string
  baseCurrency: Currency
  quoteCurrency: Currency
  spotLag: number
  settlementCalendars: Currency[]
  dayCount: DayCountConvention
  businessDayConvention: BusinessDayConvention
  pricingPrecision: number
  pipSize: number
}

export interface CalendarHoliday {
  date: string
  currency: Currency
  name: string
  type: 'bank' | 'settlement' | 'both'
}

export interface MarketCalendar {
  currency: Currency
  year: number
  holidays: CalendarHoliday[]
}

export interface SpotDateResult {
  pair: string
  trade_date: string
  spot_date: string
  tenor?: string
  value_date?: string
}

export interface BusinessDayCheckResult {
  date: string
  currency: Currency
  is_business_day: boolean
  reason?: string
}

export interface SpotPrice {
  pair: string
  bid: number
  ask: number
  mid: number
  timestamp: string
  is_stale: boolean
  age_seconds: number
}

export type StreamStatus = 'connecting' | 'live' | 'error' | 'closed'
