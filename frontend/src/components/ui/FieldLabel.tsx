import type { ReactNode } from 'react'

interface FieldLabelProps {
  htmlFor?: string
  children: ReactNode
}

export function FieldLabel({ htmlFor, children }: FieldLabelProps) {
  return (
    <label
      htmlFor={htmlFor}
      className="block text-label uppercase tracking-wider text-text-muted mb-1"
    >
      {children}
    </label>
  )
}
