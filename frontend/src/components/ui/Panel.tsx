import type { ReactNode } from 'react'

interface PanelProps {
  children: ReactNode
  className?: string
  variant?: 'default' | 'inset' | 'highlight'
}

const variants = {
  default:   'border-border-default bg-bg-surface',
  inset:     'border-border-subtle bg-bg-elevated',
  highlight: 'border-accent/30 bg-accent-subtle',
}

export function Panel({ children, className = '', variant = 'default' }: PanelProps) {
  return (
    <div className={`rounded-lg border p-4 ${variants[variant]} ${className}`}>
      {children}
    </div>
  )
}
