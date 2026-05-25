import type { ReactNode } from 'react'

interface AlertProps {
  variant: 'error' | 'warning' | 'info'
  children: ReactNode
}

const variantClasses = {
  error:   'border-negative/30 bg-negative-subtle text-negative',
  warning: 'border-warning/30 bg-warning-subtle text-warning',
  info:    'border-accent/30 bg-accent-subtle text-accent',
}

export function Alert({ variant, children }: AlertProps) {
  return (
    <div role="alert" className={`rounded-md border px-3 py-2.5 text-sm ${variantClasses[variant]}`}>
      {children}
    </div>
  )
}
