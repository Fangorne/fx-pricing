import type { ReactNode } from 'react'

interface Column<T> {
  key: keyof T | string
  header: string
  render?: (value: unknown, row: T) => ReactNode
  mono?: boolean
  align?: 'left' | 'right' | 'center'
  width?: string
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  onRowClick?: (row: T) => void
  selectedId?: string | number
  getRowId?: (row: T) => string | number
  emptyMessage?: string
}

const alignClass = {
  left:   'text-left',
  right:  'text-right',
  center: 'text-center',
}

export function DataTable<T>({
  columns,
  data,
  onRowClick,
  selectedId,
  getRowId,
  emptyMessage = 'No results found',
}: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border-default">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={String(col.key)}
                scope="col"
                className={`${alignClass[col.align ?? 'left']} ${col.width ? `w-[${col.width}]` : ''}`}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => {
            const rowId = getRowId ? getRowId(row) : rowIndex
            const isSelected = selectedId !== undefined && rowId === selectedId
            return (
              <tr
                key={rowId}
                onClick={() => onRowClick?.(row)}
                className={`
                  ${onRowClick ? 'cursor-pointer' : ''}
                  ${isSelected ? '!bg-bg-overlay' : ''}
                `}
              >
                {columns.map((col) => {
                  const value = (row as Record<string, unknown>)[String(col.key)]
                  return (
                    <td
                      key={String(col.key)}
                      className={`
                        text-text-secondary
                        ${col.mono ? 'font-mono' : ''}
                        ${alignClass[col.align ?? 'left']}
                      `}
                    >
                      {col.render ? col.render(value, row) : String(value ?? '')}
                    </td>
                  )
                })}
              </tr>
            )
          })}
          {data.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="px-3 py-10 text-center text-text-muted">
                {emptyMessage}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
