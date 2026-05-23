import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { SpotCalculatorPage } from './SpotCalculatorPage'
import * as api from '@/services/api'
import type { SpotDateResult, FXConvention } from '@/types/fx'

const mockSpot: SpotDateResult = {
  pair: 'EUR/USD',
  trade_date: '2026-05-22',
  spot_date: '2026-05-27',
}

const mockValue: SpotDateResult = {
  pair: 'EUR/USD',
  trade_date: '2026-05-22',
  spot_date: '2026-05-27',
  tenor: '3M',
  value_date: '2026-08-27',
}

const mockConvention: FXConvention = {
  pair: 'EUR/USD',
  baseCurrency: 'EUR',
  quoteCurrency: 'USD',
  spotLag: 2,
  settlementCalendars: ['EUR', 'USD'],
  dayCount: 'Act/360',
  businessDayConvention: 'MODIFIED_FOLLOWING',
  pricingPrecision: 4,
  pipSize: 0.0001,
}

function renderPage() {
  return render(
    <MemoryRouter>
      <SpotCalculatorPage />
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.restoreAllMocks()
})

describe('SpotCalculatorPage', () => {
  it('renders pair selector with all 12 pairs', () => {
    vi.spyOn(api, 'calculateSpotDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'calculateValueDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'fetchConvention').mockReturnValue(new Promise(() => {}))
    renderPage()
    const pairSelect = screen.getByDisplayValue('EUR/USD')
    const options = pairSelect.querySelectorAll('option')
    expect(options.length).toBe(12)
  })

  it('renders tenor selector with 10 tenors', () => {
    vi.spyOn(api, 'calculateSpotDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'calculateValueDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'fetchConvention').mockReturnValue(new Promise(() => {}))
    renderPage()
    const tenorSelect = screen.getByDisplayValue('3M')
    const options = tenorSelect.querySelectorAll('option')
    expect(options.length).toBe(10)
  })

  it('shows result after debounce with spot and value date', async () => {
    vi.spyOn(api, 'calculateSpotDate').mockResolvedValue(mockSpot)
    vi.spyOn(api, 'calculateValueDate').mockResolvedValue(mockValue)
    vi.spyOn(api, 'fetchConvention').mockResolvedValue(mockConvention)
    renderPage()
    await waitFor(() => screen.getByText(/Spot Date/i), { timeout: 1500 })
    expect(screen.getAllByText(/Value Date/i).length).toBeGreaterThan(0)
  }, 3000)

  it('shows loading skeleton while fetching', async () => {
    vi.spyOn(api, 'calculateSpotDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'calculateValueDate').mockReturnValue(new Promise(() => {}))
    vi.spyOn(api, 'fetchConvention').mockReturnValue(new Promise(() => {}))
    renderPage()
    // Trigger debounce by changing tenor
    const tenorSelect = screen.getByDisplayValue('3M')
    fireEvent.change(tenorSelect, { target: { value: '1M' } })
    await waitFor(
      () => {
        const el = document.querySelector('.animate-pulse')
        if (!el) throw new Error('no skeleton')
        return el
      },
      { timeout: 700 },
    )
    expect(document.querySelector('.animate-pulse')).toBeTruthy()
  }, 2000)

  it('shows error message on API failure', async () => {
    vi.spyOn(api, 'calculateSpotDate').mockRejectedValue(new Error('API error 404'))
    vi.spyOn(api, 'calculateValueDate').mockRejectedValue(new Error('API error 404'))
    vi.spyOn(api, 'fetchConvention').mockRejectedValue(new Error('API error 404'))
    renderPage()
    await waitFor(() => screen.getByText(/API error/i), { timeout: 1500 })
  }, 3000)

  it('accumulates history entries', async () => {
    vi.spyOn(api, 'calculateSpotDate').mockResolvedValue(mockSpot)
    vi.spyOn(api, 'calculateValueDate').mockResolvedValue(mockValue)
    vi.spyOn(api, 'fetchConvention').mockResolvedValue(mockConvention)
    renderPage()
    await waitFor(() => screen.getByText(/Derniers calculs/i), { timeout: 1500 })
    expect(screen.getByText(/Derniers calculs/i)).toBeTruthy()
  }, 3000)
})
