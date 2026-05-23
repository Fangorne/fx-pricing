import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { ConventionsPage } from './ConventionsPage'
import * as api from '@/services/api'
import type { FXConvention } from '@/types/fx'

const mockConventions: FXConvention[] = [
  {
    pair: 'EUR/USD',
    baseCurrency: 'EUR',
    quoteCurrency: 'USD',
    spotLag: 2,
    settlementCalendars: ['EUR', 'USD'],
    dayCount: 'Act/360',
    businessDayConvention: 'MODIFIED_FOLLOWING',
    pricingPrecision: 4,
    pipSize: 0.0001,
  },
  {
    pair: 'GBP/USD',
    baseCurrency: 'GBP',
    quoteCurrency: 'USD',
    spotLag: 2,
    settlementCalendars: ['GBP', 'USD'],
    dayCount: 'Act/365',
    businessDayConvention: 'MODIFIED_FOLLOWING',
    pricingPrecision: 4,
    pipSize: 0.0001,
  },
  {
    pair: 'USD/JPY',
    baseCurrency: 'USD',
    quoteCurrency: 'JPY',
    spotLag: 2,
    settlementCalendars: ['USD', 'JPY'],
    dayCount: 'Act/360',
    businessDayConvention: 'MODIFIED_FOLLOWING',
    pricingPrecision: 2,
    pipSize: 0.01,
  },
]

function renderPage(path = '/conventions') {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <ConventionsPage />
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.restoreAllMocks()
})

describe('ConventionsPage', () => {
  it('shows loading skeletons initially', () => {
    vi.spyOn(api, 'fetchConventions').mockReturnValue(new Promise(() => {}))
    renderPage()
    const skeletons = document.querySelectorAll('.animate-pulse')
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('renders list of pairs after fetch', async () => {
    vi.spyOn(api, 'fetchConventions').mockResolvedValue(mockConventions)
    renderPage()
    await waitFor(() => expect(screen.getByText('EUR/USD')).toBeTruthy())
    expect(screen.getByText('GBP/USD')).toBeTruthy()
    expect(screen.getByText('USD/JPY')).toBeTruthy()
  })

  it('filters pairs by search query', async () => {
    vi.spyOn(api, 'fetchConventions').mockResolvedValue(mockConventions)
    renderPage()
    await waitFor(() => screen.getByText('EUR/USD'))
    const input = screen.getByPlaceholderText(/filtrer/i)
    fireEvent.change(input, { target: { value: 'EUR' } })
    expect(screen.getByText('EUR/USD')).toBeTruthy()
    expect(screen.queryByText('GBP/USD')).toBeNull()
    expect(screen.queryByText('USD/JPY')).toBeNull()
  })

  it('shows error message when API is unavailable', async () => {
    vi.spyOn(api, 'fetchConventions').mockRejectedValue(new Error('API error 500'))
    renderPage()
    await waitFor(() => screen.getByText(/API inaccessible/i))
  })

  it('shows "aucune paire trouvée" when filter matches nothing', async () => {
    vi.spyOn(api, 'fetchConventions').mockResolvedValue(mockConventions)
    renderPage()
    await waitFor(() => screen.getByText('EUR/USD'))
    const input = screen.getByPlaceholderText(/filtrer/i)
    fireEvent.change(input, { target: { value: 'XXXYYY' } })
    expect(screen.getByText(/aucune paire/i)).toBeTruthy()
  })
})
