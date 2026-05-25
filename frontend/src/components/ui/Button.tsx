import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  children: ReactNode
}

const variantClasses: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary:
    'bg-accent text-text-inverse font-semibold hover:bg-accent-hover ' +
    'focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg-base',
  secondary:
    'bg-bg-elevated border border-border-default text-text-primary ' +
    'hover:border-border-strong hover:bg-bg-overlay ' +
    'focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg-base',
  ghost:
    'text-text-secondary hover:text-text-primary hover:bg-bg-elevated ' +
    'focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg-base',
  danger:
    'bg-negative-subtle border border-negative/30 text-negative ' +
    'hover:bg-negative hover:text-text-inverse ' +
    'focus-visible:ring-2 focus-visible:ring-negative focus-visible:ring-offset-2 focus-visible:ring-offset-bg-base',
}

const sizeClasses: Record<NonNullable<ButtonProps['size']>, string> = {
  sm: 'h-7 px-3 text-xs rounded-md gap-1.5',
  md: 'h-8 px-4 text-sm rounded-md gap-2',
  lg: 'h-10 px-5 text-sm rounded-lg gap-2',
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      className={`
        inline-flex items-center justify-center font-medium
        transition-colors duration-[150ms]
        disabled:pointer-events-none disabled:opacity-40
        ${variantClasses[variant]} ${sizeClasses[size]} ${className}
      `}
      {...props}
    >
      {children}
    </button>
  )
}
