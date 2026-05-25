import { createContext, useCallback, useContext, useEffect, useState } from 'react'

export type TokenName =
  | 'bg-base' | 'bg-surface' | 'bg-elevated' | 'bg-overlay'
  | 'border-subtle' | 'border-default' | 'border-strong'
  | 'text-primary' | 'text-secondary' | 'text-muted' | 'text-inverse'
  | 'accent' | 'accent-subtle' | 'accent-hover' | 'accent-dim'
  | 'positive' | 'positive-subtle'
  | 'negative' | 'negative-subtle'
  | 'warning' | 'warning-subtle'

export type TokenMap = Record<TokenName, string>

export const TOKEN_DEFAULTS: TokenMap = {
  'bg-base':        '#0a0e17',
  'bg-surface':     '#0f1520',
  'bg-elevated':    '#141c2b',
  'bg-overlay':     '#192234',
  'border-subtle':  '#1a2236',
  'border-default': '#1f2d45',
  'border-strong':  '#2a3d5c',
  'text-primary':   '#d4e0f5',
  'text-secondary': '#6e88a8',
  'text-muted':     '#354d6a',
  'text-inverse':   '#0a0e17',
  'accent':         '#00b4c8',
  'accent-subtle':  '#00232a',
  'accent-hover':   '#00cce0',
  'accent-dim':     '#007f8f',
  'positive':        '#00d47a',
  'positive-subtle': '#002e1c',
  'negative':        '#f0384f',
  'negative-subtle': '#2b0c12',
  'warning':         '#f5a623',
  'warning-subtle':  '#291a00',
}

const STORAGE_KEY = 'fx-pricing-theme'

function applyTokens(tokens: TokenMap) {
  const root = document.documentElement
  for (const [name, value] of Object.entries(tokens)) {
    root.style.setProperty(`--${name}`, value)
  }
}

function loadSaved(): Partial<TokenMap> {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}')
  } catch {
    return {}
  }
}

interface ThemeContextValue {
  tokens: TokenMap
  updateToken: (name: TokenName, value: string) => void
  resetToDefaults: () => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [tokens, setTokens] = useState<TokenMap>(() => {
    const saved = loadSaved()
    return { ...TOKEN_DEFAULTS, ...saved }
  })

  useEffect(() => {
    applyTokens(tokens)
  }, [])

  const updateToken = useCallback((name: TokenName, value: string) => {
    document.documentElement.style.setProperty(`--${name}`, value)
    setTokens((prev) => {
      const next = { ...prev, [name]: value }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      return next
    })
  }, [])

  const resetToDefaults = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    applyTokens(TOKEN_DEFAULTS)
    setTokens(TOKEN_DEFAULTS)
  }, [])

  return (
    <ThemeContext.Provider value={{ tokens, updateToken, resetToDefaults }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used inside ThemeProvider')
  return ctx
}
