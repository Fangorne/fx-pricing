import type { InputHTMLAttributes } from 'react'
import { FieldLabel } from './FieldLabel'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  mono?: boolean
}

export function Input({ label, error, id, mono = false, className = '', ...props }: InputProps) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-')
  return (
    <div className="space-y-1">
      {label && <FieldLabel htmlFor={inputId}>{label}</FieldLabel>}
      <input
        id={inputId}
        className={`
          form-control
          ${mono ? 'font-mono' : 'font-sans'}
          ${error ? 'border-negative focus:border-negative focus:ring-negative/40' : ''}
          ${className}
        `}
        {...props}
      />
      {error && <p className="text-xs text-negative mt-1">{error}</p>}
    </div>
  )
}
