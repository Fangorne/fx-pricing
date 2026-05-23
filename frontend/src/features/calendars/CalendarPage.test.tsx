import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { CalendarPage } from './CalendarPage'
import * as api from '@/services/api'
import type { CalendarHoliday, BusinessDayCheckResult } from '@/types/fx'

const mockHolidays: CalendarHoliday[] = [
  { date: '2026-01-01', currency: 'USD', name: 'USD holiday', type: 'bank' },
  { date: '2026-07-04', currency: 'USD', name: 'USD holiday', type: 'bank' },
  { date: '2026-12-25', currency: 'USD', name: 'USD holiday', type: 'bank' },
]

const mockBusinessDay: BusinessDayCheckResult = {
  date: '2026-05-26',
  currency: 'USD',
  is_business_day: true,
}

function renderPage() {
  return render(
    <MemoryRouter>
      <CalendarPage />
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.restoreAllMocks()
})

describe('CalendarPage', () => {
  it('renders currency selector with all 10 currencies', () => {
    vi.spyOn(api, 'fetchHolidays').mockReturnValue(new Promise(() => {}))
    renderPage()
    const select = screen.getByDisplayValue('USD')
    expect(select).toBeTruthy()
    const options = select.querySelectorAll('option')
    expect(options.length).toBe(10)
  })

  it('renders year selector with 5 options', () => {
    vi.spyOn(api, 'fetchHolidays').mockReturnValue(new Promise(() => {}))
    renderPage()
    const selects = screen.getAllByRole('combobox')
    const yearSelect = selects[1]
    expect(yearSelect).toBeTruthy()
    const options = (yearSelect as HTMLSelectElement).querySelectorAll('option')
    expect(options.length).toBe(5)
  })

  it('shows loading skeleton initially', () => {
    vi.spyOn(api, 'fetchHolidays').mockReturnValue(new Promise(() => {}))
    renderPage()
    const skeletons = document.querySelectorAll('.animate-pulse')
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('renders holiday list after fetch', async () => {
    vi.spyOn(api, 'fetchHolidays').mockResolvedValue(mockHolidays)
    renderPage()
    await waitFor(() => expect(screen.getAllByRole('row').length).toBeGreaterThan(1))
  })

  it('detects weekend client-side without calling API', async () => {
    vi.spyOn(api, 'fetchHolidays').mockResolvedValue([])
    const spy = vi.spyOn(api, 'checkBusinessDay')
    renderPage()
    await waitFor(() => screen.getByText(/Vérifier une date/i))

    const input = screen.getByDisplayValue('')
    // 2026-05-23 is a Saturday
    fireEvent.change(input, { target: { value: '2026-05-23' } })

    await waitFor(() => screen.getByText(/Non ouvré/i))
    expect(spy).not.toHaveBeenCalled()
    expect(screen.getByText(/Weekend/i)).toBeTruthy()
  })

  it('calls API for non-weekend date and shows result', async () => {
    vi.spyOn(api, 'fetchHolidays').mockResolvedValue([])
    vi.spyOn(api, 'checkBusinessDay').mockResolvedValue(mockBusinessDay)
    renderPage()
    await waitFor(() => screen.getByText(/Vérifier une date/i))

    const input = screen.getByDisplayValue('')
    // 2026-05-26 is Tuesday
    fireEvent.change(input, { target: { value: '2026-05-26' } })

    // Wait for debounce (300ms) + API response
    await waitFor(() => screen.getByText(/Business Day/i), { timeout: 1500 })
  }, 3000)
})
