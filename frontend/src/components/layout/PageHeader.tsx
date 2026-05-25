import type { ReactNode } from 'react'

interface PageHeaderProps {
  title: string
  subtitle?: string
  badge?: ReactNode
  actions?: ReactNode
  /** When true, renders the compact terminal-style header used by most pages */
  compact?: boolean
}

export function PageHeader({ title, subtitle, badge, actions, compact = false }: PageHeaderProps) {
  if (compact) {
    return (
      <div className="flex items-center justify-between border-b border-border-subtle pb-2">
        <div className="flex items-center gap-3">
          <span className="text-label uppercase tracking-wider text-text-muted">{title}</span>
          {badge}
        </div>
        {actions && <div className="flex items-center gap-2">{actions}</div>}
      </div>
    )
  }

  return (
    <div className="flex items-start justify-between">
      <div className="space-y-1">
        <div className="flex items-center gap-3">
          <h1 className="font-mono text-data-lg font-bold text-text-primary">{title}</h1>
          {badge}
        </div>
        {subtitle && <p className="text-sm text-text-secondary">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  )
}
