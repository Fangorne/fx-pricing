import { NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import {
  LayoutDashboard,
  ArrowLeftRight,
  CalendarDays,
  Calculator,
  TrendingUp,
  Palette,
  type LucideIcon,
} from 'lucide-react'

interface NavItem {
  to: string
  label: string
  icon: LucideIcon
  end?: boolean
  dev?: boolean
}

const NAV_ITEMS: NavItem[] = [
  { to: '/',              label: 'Overview',        icon: LayoutDashboard, end: true },
  { to: '/conventions',   label: 'Conventions',     icon: ArrowLeftRight },
  { to: '/calendars',     label: 'Calendars',       icon: CalendarDays },
  { to: '/dates',         label: 'Date Calculator', icon: Calculator },
  { to: '/prices',        label: 'Live Prices',     icon: TrendingUp },
  { to: '/design-system', label: 'Design System',   icon: Palette, dev: true },
]

function useUtcClock() {
  const [time, setTime] = useState(() => new Date().toUTCString().slice(17, 22))
  useEffect(() => {
    const id = setInterval(() => setTime(new Date().toUTCString().slice(17, 22)), 1000)
    return () => clearInterval(id)
  }, [])
  return time
}

export function Sidebar() {
  const utcTime = useUtcClock()
  return (
    <aside className="flex h-screen w-[224px] shrink-0 flex-col border-r border-border-subtle bg-bg-surface">
      {/* Logo bar */}
      <div className="flex h-12 items-center gap-2 border-b border-border-subtle px-4">
        <div className="flex h-5 w-5 items-center justify-center rounded-sm bg-accent/10">
          <span className="font-mono text-[10px] font-bold leading-none text-accent">FX</span>
        </div>
        <span className="font-mono text-sm font-semibold tracking-tight text-text-primary">
          Pricing
          <span className="text-text-muted font-normal"> / G10</span>
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-2 py-3">
        <p className="mb-1.5 px-2 text-label uppercase tracking-wider text-text-muted">Navigation</p>
        <ul className="space-y-px" role="list">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            return (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    `group flex items-center gap-2.5 rounded-md px-2.5 py-2 text-sm transition-colors duration-[100ms] ${
                      isActive
                        ? 'bg-accent/10 text-accent'
                        : 'text-text-secondary hover:bg-bg-elevated hover:text-text-primary'
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      <Icon
                        size={14}
                        strokeWidth={isActive ? 2.5 : 2}
                        className={`shrink-0 transition-colors duration-[100ms] ${
                          isActive ? 'text-accent' : 'text-text-muted group-hover:text-text-secondary'
                        }`}
                      />
                      <span className={`font-medium ${isActive ? '' : 'group-hover:text-text-primary'}`}>
                        {item.label}
                      </span>
                      {item.dev && !isActive && (
                        <span className="ml-auto rounded px-1 py-px font-mono text-[9px] font-bold uppercase tracking-wider text-text-muted border border-border-default">
                          DEV
                        </span>
                      )}
                      {isActive && (
                        <span className="ml-auto h-1 w-1 rounded-full bg-accent" />
                      )}
                    </>
                  )}
                </NavLink>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="border-t border-border-subtle px-3 py-3">
        <div className="flex items-center gap-2 px-2 py-1">
          <span className="h-1.5 w-1.5 rounded-full bg-positive animate-pulse" />
          <span className="text-label uppercase tracking-wider text-text-muted">G10 Coverage</span>
        </div>
        <div className="mt-1 px-2 flex items-center justify-between">
          <span className="text-label uppercase tracking-wider text-text-muted">
            45 pairs · 10 cal
          </span>
          <span className="font-mono text-[10px] text-text-muted tabular-nums">
            {utcTime} UTC
          </span>
        </div>
      </div>
    </aside>
  )
}
