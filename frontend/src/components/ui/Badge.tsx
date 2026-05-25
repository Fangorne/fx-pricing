import type { ReactNode } from 'react'

interface BadgeProps {
  variant: 'success' | 'positive' | 'warning' | 'danger' | 'negative' | 'neutral' | 'accent'
  children: ReactNode
  dot?: boolean
}

const variantClasses: Record<BadgeProps['variant'], string> = {
  positive: 'bg-positive-subtle text-positive border border-positive/20',
  success:  'bg-positive-subtle text-positive border border-positive/20',
  negative: 'bg-negative-subtle text-negative border border-negative/20',
  danger:   'bg-negative-subtle text-negative border border-negative/20',
  warning:  'bg-warning-subtle text-warning border border-warning/20',
  neutral:  'bg-bg-elevated text-text-secondary border border-border-default',
  accent:   'bg-accent-subtle text-accent border border-accent/20',
}

const dotClasses: Record<BadgeProps['variant'], string> = {
  positive: 'bg-positive',
  success:  'bg-positive',
  negative: 'bg-negative',
  danger:   'bg-negative',
  warning:  'bg-warning',
  neutral:  'bg-text-muted',
  accent:   'bg-accent',
}

export function Badge({ variant, children, dot = false }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-label font-semibold uppercase tracking-wider ${variantClasses[variant]}`}
    >
      {dot && <span className={`h-1.5 w-1.5 rounded-full ${dotClasses[variant]}`} />}
      {children}
    </span>
  )
}
