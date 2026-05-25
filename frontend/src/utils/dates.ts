const BLOOMBERG_MONTHS = [
  'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
]

/** Parse an ISO date string safely, treating it as local midnight to avoid UTC shift. */
export function parseIso(iso: string): Date {
  return new Date(iso + 'T00:00:00')
}

/** Format a date as ISO 8601: 2026-05-27 */
export function formatIso(date: Date | string): string {
  const d = typeof date === 'string' ? parseIso(date) : date
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

/** Format a date as Bloomberg style: 27-MAY-26 */
export function formatBloomberg(date: Date | string): string {
  const d = typeof date === 'string' ? parseIso(date) : date
  const day = String(d.getDate()).padStart(2, '0')
  const mon = BLOOMBERG_MONTHS[d.getMonth()]
  const yr = String(d.getFullYear()).slice(-2)
  return `${day}-${mon}-${yr}`
}
