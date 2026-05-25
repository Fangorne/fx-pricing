import { useCallback, useRef, useState } from 'react'
import { Alert, Badge, Button, DataTable, Input, Panel, Select, Skeleton } from '../components/ui'
import { PageHeader } from '../components/layout/PageHeader'
import { TokenName, useTheme } from '../contexts/ThemeContext'

// ---------------------------------------------------------------------------
// Section wrapper
// ---------------------------------------------------------------------------
function Section({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <section className="space-y-4">
      <div className="space-y-1 border-b border-border-subtle pb-3">
        <h2 className="text-sm font-semibold text-text-primary">{title}</h2>
        <p className="text-sm text-text-secondary">{description}</p>
      </div>
      {children}
    </section>
  )
}

// ---------------------------------------------------------------------------
// 0. Theme Editor
// ---------------------------------------------------------------------------
const TOKEN_GROUPS: { label: string; tokens: TokenName[] }[] = [
  { label: 'Backgrounds', tokens: ['bg-base', 'bg-surface', 'bg-elevated', 'bg-overlay'] },
  { label: 'Borders', tokens: ['border-subtle', 'border-default', 'border-strong'] },
  { label: 'Text', tokens: ['text-primary', 'text-secondary', 'text-muted'] },
  { label: 'Accent', tokens: ['accent', 'accent-subtle', 'accent-hover'] },
  { label: 'Semantic', tokens: ['success', 'success-subtle', 'warning', 'warning-subtle', 'danger', 'danger-subtle'] },
]

function TokenRow({ name }: { name: TokenName }) {
  const { tokens, updateToken } = useTheme()
  const [hexInput, setHexInput] = useState(tokens[name])
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const handleColorPicker = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value
    setHexInput(val)
    updateToken(name, val)
  }, [name, updateToken])

  const handleHexInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value
    setHexInput(val)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      if (/^#[0-9a-f]{6}$/i.test(val)) {
        updateToken(name, val)
      }
    }, 300)
  }, [name, updateToken])

  return (
    <div className="flex items-center gap-3">
      <span className="w-40 shrink-0 font-mono text-xs text-text-secondary">{name}</span>
      <input
        type="color"
        value={tokens[name]}
        onChange={handleColorPicker}
        className="h-7 w-10 cursor-pointer rounded border border-border-default bg-transparent p-0.5"
        aria-label={`Color picker for ${name}`}
      />
      <input
        type="text"
        value={hexInput}
        onChange={handleHexInput}
        maxLength={7}
        className="w-24 rounded border border-border-default bg-bg-elevated px-2 py-1 font-mono text-xs text-text-primary focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-1 focus-visible:ring-offset-bg-base"
        aria-label={`Hex value for ${name}`}
      />
      <div
        className="h-5 w-5 rounded border border-border-default"
        style={{ backgroundColor: tokens[name] }}
      />
    </div>
  )
}

function ThemeEditor() {
  const { resetToDefaults } = useTheme()
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <p className="text-xs text-text-muted">
          Changes apply globally across the app and persist in localStorage.
        </p>
        <Button variant="ghost" size="sm" onClick={resetToDefaults}>
          Reset to defaults
        </Button>
      </div>
      <div className="grid gap-6 sm:grid-cols-2">
        {TOKEN_GROUPS.map((group) => (
          <div key={group.label} className="space-y-2">
            <p className="text-label uppercase tracking-wide text-text-muted">{group.label}</p>
            <div className="space-y-2">
              {group.tokens.map((token) => (
                <TokenRow key={token} name={token} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// 1. Color Palette (reactive)
// ---------------------------------------------------------------------------
const swatchNames: TokenName[] = [
  'bg-base', 'bg-surface', 'bg-elevated', 'bg-overlay',
  'border-subtle', 'border-default', 'border-strong',
  'text-primary', 'text-secondary', 'text-muted',
  'accent', 'accent-subtle', 'accent-hover',
  'success', 'success-subtle',
  'warning', 'warning-subtle',
  'danger', 'danger-subtle',
]

function ColorPalette() {
  const { tokens } = useTheme()
  return (
    <div className="grid grid-cols-[repeat(auto-fill,minmax(100px,1fr))] gap-3">
      {swatchNames.map((name) => (
        <div key={name} className="space-y-1.5">
          <div
            className="h-12 w-full rounded-lg border border-border-default"
            style={{ backgroundColor: tokens[name] }}
            aria-label={name}
          />
          <div>
            <p className="text-xs font-medium text-text-primary">{name}</p>
            <p className="font-mono text-xs text-text-muted">{tokens[name]}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// 2. Typography
// ---------------------------------------------------------------------------
type TypographyRow = {
  name: string
  className: string
  meta: string
  sample: string
}

const typographyRows: TypographyRow[] = [
  {
    name: 'display',
    className: 'text-2xl font-bold',
    meta: '24px / 700',
    sample: 'EUR/USD Spot Rate',
  },
  {
    name: 'heading',
    className: 'text-lg font-semibold',
    meta: '18px / 600',
    sample: 'FX Market Conventions',
  },
  {
    name: 'subheading',
    className: 'text-sm font-medium',
    meta: '14px / 500',
    sample: 'Settlement: T+2',
  },
  {
    name: 'body',
    className: 'text-sm font-normal',
    meta: '14px / 400',
    sample: 'Day count basis determines how interest accrues between value dates.',
  },
  {
    name: 'small',
    className: 'text-xs font-normal',
    meta: '12px / 400',
    sample: 'Effective 2026-05-25 — Act/360 basis',
  },
  {
    name: 'label',
    className: 'text-label uppercase tracking-wide',
    meta: '11px / 500 / uppercase',
    sample: 'Spot Lag',
  },
  {
    name: 'data',
    className: 'text-data font-mono',
    meta: '14px / 600 / mono',
    sample: '1.08432',
  },
  {
    name: 'data-lg',
    className: 'text-data-lg font-mono font-bold',
    meta: '18px / 700 / mono',
    sample: 'EUR/USD 1.08432',
  },
]

function Typography() {
  return (
    <div className="space-y-2">
      {typographyRows.map((row) => (
        <div
          key={row.name}
          className="flex items-baseline gap-6 rounded-lg border border-border-subtle px-4 py-3"
        >
          <div className="w-28 shrink-0">
            <span className="text-label uppercase tracking-wide text-text-muted">{row.name}</span>
            <p className="mt-0.5 font-mono text-xs text-text-muted">{row.meta}</p>
          </div>
          <span className={`text-text-primary ${row.className}`}>{row.sample}</span>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// 3. Buttons
// ---------------------------------------------------------------------------
const buttonVariants = ['primary', 'secondary', 'ghost', 'danger'] as const
const buttonSizes = ['sm', 'md'] as const

function Buttons() {
  return (
    <div className="space-y-4">
      {buttonSizes.map((size) => (
        <div key={size} className="space-y-2">
          <p className="text-label uppercase tracking-wide text-text-muted">size: {size}</p>
          <div className="flex flex-wrap items-center gap-3">
            {buttonVariants.map((variant) => (
              <Button key={variant} variant={variant} size={size}>
                {variant.charAt(0).toUpperCase() + variant.slice(1)}
              </Button>
            ))}
            <Button variant="primary" size={size} disabled>
              Disabled
            </Button>
          </div>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// 4. Badges
// ---------------------------------------------------------------------------
const badgeItems = [
  { variant: 'positive', label: 'Settled' },
  { variant: 'warning', label: 'Pending' },
  { variant: 'negative', label: 'Failed' },
  { variant: 'neutral', label: 'Draft' },
  { variant: 'accent', label: 'Active' },
] as const

function Badges() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      {badgeItems.map((item) => (
        <Badge key={item.variant} variant={item.variant}>
          {item.label}
        </Badge>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// 5. Alerts
// ---------------------------------------------------------------------------
function Alerts() {
  return (
    <div className="space-y-3">
      <Alert variant="error">
        Settlement failed: EUR/USD value date 2026-05-27 falls on a non-business day.
      </Alert>
      <Alert variant="warning">
        Spot lag override applied — holiday calendar for USD has not been refreshed since 2026-04-01.
      </Alert>
      <Alert variant="info">
        GBP/USD convention updated: day count basis changed from Act/365 to Act/Act effective T+0.
      </Alert>
    </div>
  )
}

// ---------------------------------------------------------------------------
// 6. Inputs & Selects
// ---------------------------------------------------------------------------
function Inputs() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <Input placeholder="1.08432" />
      <Input label="Spot Rate" placeholder="1.08432" />
      <Input label="Value Date" placeholder="2026-05-27" error="Date falls on a holiday." />
      <Select
        label="Day Count"
        options={[
          { value: 'act360', label: 'Act/360' },
          { value: 'act365', label: 'Act/365' },
          { value: 'actact', label: 'Act/Act' },
          { value: '30360', label: '30/360' },
        ]}
      />
    </div>
  )
}

// ---------------------------------------------------------------------------
// 7. Panels
// ---------------------------------------------------------------------------
function Panels() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <Panel variant="default">
        <p className="text-label uppercase tracking-wide text-text-muted">variant: default</p>
        <p className="mt-2 text-sm text-text-primary">
          EUR/USD — Settlement T+2, Act/360, London business days.
        </p>
      </Panel>
      <Panel variant="inset">
        <p className="text-label uppercase tracking-wide text-text-muted">variant: inset</p>
        <p className="mt-2 text-sm text-text-primary">
          GBP/USD — Settlement T+2, Act/365, New York + London calendars.
        </p>
      </Panel>
    </div>
  )
}

// ---------------------------------------------------------------------------
// 8. Skeleton
// ---------------------------------------------------------------------------
function Skeletons() {
  return (
    <div className="grid gap-6 sm:grid-cols-2">
      <div className="space-y-2">
        <p className="text-label uppercase tracking-wide text-text-muted">1 line</p>
        <Skeleton lines={1} />
      </div>
      <div className="space-y-2">
        <p className="text-label uppercase tracking-wide text-text-muted">3 lines</p>
        <Skeleton lines={3} />
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// 9. DataTable
// ---------------------------------------------------------------------------
type FxRow = {
  pair: string
  spotLag: string
  dayCount: string
  convention: string
}

const fxData: FxRow[] = [
  { pair: 'EUR/USD', spotLag: 'T+2', dayCount: 'Act/360', convention: 'Modified Following' },
  { pair: 'GBP/USD', spotLag: 'T+2', dayCount: 'Act/365', convention: 'Modified Following' },
  { pair: 'USD/JPY', spotLag: 'T+2', dayCount: 'Act/360', convention: 'Following' },
  { pair: 'USD/CAD', spotLag: 'T+1', dayCount: 'Act/365', convention: 'Modified Following' },
]

const fxColumns = [
  { key: 'pair' as keyof FxRow, header: 'Pair', mono: true },
  { key: 'spotLag' as keyof FxRow, header: 'Spot Lag', align: 'center' as const },
  { key: 'dayCount' as keyof FxRow, header: 'Day Count' },
  { key: 'convention' as keyof FxRow, header: 'Convention' },
]

function FxTable() {
  return <DataTable columns={fxColumns} data={fxData} getRowId={(r) => r.pair} />
}

// ---------------------------------------------------------------------------
// 10. Borders & Spacing
// ---------------------------------------------------------------------------
const spacingScale = [1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24] as const
const borderColors = [
  { label: 'border-subtle', cls: 'border-border-subtle', hex: '#1e1e2e' },
  { label: 'border-default', cls: 'border-border-default', hex: '#2a2a3a' },
  { label: 'border-strong', cls: 'border-border-strong', hex: '#3d3d52' },
]

function BordersAndSpacing() {
  return (
    <div className="space-y-8">
      {/* Border colors */}
      <div className="space-y-3">
        <p className="text-label uppercase tracking-wide text-text-muted">Border tokens</p>
        <div className="space-y-3">
          {borderColors.map((b) => (
            <div key={b.label} className="flex items-center gap-4">
              <div className={`h-8 w-48 rounded border-2 bg-bg-elevated ${b.cls}`} />
              <span className="text-sm text-text-primary">{b.label}</span>
              <span className="font-mono text-xs text-text-muted">{b.hex}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Spacing scale */}
      <div className="space-y-3">
        <p className="text-label uppercase tracking-wide text-text-muted">
          Spacing scale (8px base)
        </p>
        <div className="flex flex-wrap items-end gap-4">
          {spacingScale.map((step) => (
            <div key={step} className="flex flex-col items-center gap-1.5">
              <div
                className="bg-accent-subtle border border-accent/30 rounded"
                style={{ width: `${step * 4}px`, height: `${step * 4}px` }}
              />
              <span className="font-mono text-xs text-text-muted">{step * 4}px</span>
              <span className="text-label text-text-muted">× {step}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export function DesignSystemPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-12 px-6 py-8">
      <PageHeader
        title="Design System"
        subtitle="Visual reference for all semantic tokens, typography, and UI components used in FXPricing."
        badge={
          <Badge variant="accent">Dev Tool</Badge>
        }
      />

      <Section
        title="Theme Editor"
        description="Edit any color token live — changes apply instantly to every component in the app."
      >
        <ThemeEditor />
      </Section>

      <Section
        title="Color Palette"
        description="All semantic color tokens — backgrounds, borders, text, accent, and status colors. Every class uses the design system token, not a raw Tailwind value."
      >
        <ColorPalette />
      </Section>

      <Section
        title="Typography"
        description="Type scale with realistic FX content. Mono variants are used for numeric data to prevent layout shift."
      >
        <Typography />
      </Section>

      <Section
        title="Buttons"
        description="Four variants × two sizes. The danger variant transitions to a filled state on hover to communicate destructive intent."
      >
        <Buttons />
      </Section>

      <Section
        title="Badges"
        description="Inline status indicators using subtle background + border treatment. Always uppercase via the label text style."
      >
        <Badges />
      </Section>

      <Section
        title="Alerts"
        description="Full-width contextual messages for errors, warnings, and informational feedback."
      >
        <Alerts />
      </Section>

      <Section
        title="Inputs & Selects"
        description="Form controls with optional label and error state. Error state overrides the border and focus ring to danger tokens."
      >
        <Inputs />
      </Section>

      <Section
        title="Panel"
        description="Surface containers. Default uses bg-surface with a visible border; inset uses bg-elevated for a recessed appearance."
      >
        <Panels />
      </Section>

      <Section
        title="Skeleton"
        description="Animated loading placeholder. Uses bg-overlay fill with pulse animation."
      >
        <Skeletons />
      </Section>

      <Section
        title="DataTable"
        description="Responsive table with mono rendering for pair codes, sticky header on bg-elevated, and divided rows on border-subtle."
      >
        <FxTable />
      </Section>

      <Section
        title="Borders & Spacing"
        description="Three border token weights and the 4px-step spacing scale derived from the 8px base unit."
      >
        <BordersAndSpacing />
      </Section>
    </div>
  )
}
