interface SkeletonProps {
  lines?: number
  className?: string
}

export function Skeleton({ lines = 4, className = '' }: SkeletonProps) {
  return (
    <div className={`animate-pulse space-y-1.5 ${className}`} aria-busy="true" aria-label="Loading">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-7 rounded-md bg-bg-elevated"
          style={{ width: i % 3 === 2 ? '60%' : '100%' }}
        />
      ))}
    </div>
  )
}
