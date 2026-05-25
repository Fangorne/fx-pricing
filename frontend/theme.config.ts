/**
 * THEME CONFIG — Single source of truth for the FX Pricing design system.
 *
 * Philosophy: Bloomberg Terminal meets Linear. Every pixel is intentional.
 * Dense, readable, no decorative noise. Data is the hero.
 *
 * Rules for all frontend agents:
 *  - Never hardcode a color, spacing value, or font name outside this file.
 *  - All Tailwind classes must map to tokens defined here.
 *  - Motion must be subtle: 150ms ease-out max for micro-interactions.
 *  - Tables: sticky headers, alternating-row or divider only, no zebra stripes.
 *  - Forms: every input needs a visible focus ring using --accent.
 */

export const theme = {
  // ─── Palette ────────────────────────────────────────────────────────────────
  colors: {
    // Backgrounds — layered from darkest (base) to lightest (overlay)
    bg: {
      base:     '#0a0e17', // terminal black — the page canvas
      surface:  '#0f1520', // sidebar, cards
      elevated: '#141c2b', // hover states, inset panels
      overlay:  '#192234', // modals, dropdowns, selected rows
    },

    // Borders — from invisible (subtle) to visible (strong)
    border: {
      subtle:  '#1a2236',
      default: '#1f2d45',
      strong:  '#2a3d5c',
      focus:   '#00b4c8', // accent — always used for focus rings
    },

    // Text — high contrast hierarchy
    text: {
      primary:   '#d4e0f5', // body text, data values
      secondary: '#6e88a8', // labels, descriptions
      muted:     '#354d6a', // column headers, placeholders
      inverse:   '#0a0e17', // text on bright accent backgrounds
    },

    // Accent — cyan/teal interactive color
    accent: {
      DEFAULT: '#00b4c8',
      subtle:  '#00232a',
      hover:   '#00cce0',
      dim:     '#007f8f',
    },

    // Semantic — trading signals
    positive: {
      DEFAULT: '#00d47a', // bid / gain / success
      subtle:  '#002e1c',
      dim:     '#009455',
    },
    negative: {
      DEFAULT: '#f0384f', // ask / loss / danger
      subtle:  '#2b0c12',
      dim:     '#b02238',
    },
    warning: {
      DEFAULT: '#f5a623',
      subtle:  '#291a00',
    },
    neutral: {
      DEFAULT: '#6e88a8',
      subtle:  '#0f1520',
    },
  },

  // ─── Typography ─────────────────────────────────────────────────────────────
  fonts: {
    sans:  ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
    mono:  ['JetBrains Mono', 'ui-monospace', 'monospace'],
  },

  fontSize: {
    // Numeric / market data — always mono
    'data-xs': ['11px', { lineHeight: '16px', fontWeight: '500' }],
    'data-sm': ['13px', { lineHeight: '18px', fontWeight: '600' }],
    'data':    ['15px', { lineHeight: '22px', fontWeight: '600' }],
    'data-lg': ['20px', { lineHeight: '28px', fontWeight: '700' }],
    'data-xl': ['28px', { lineHeight: '36px', fontWeight: '700' }],

    // UI labels — uppercase, tracked out
    'label':   ['10px', { lineHeight: '14px', fontWeight: '600', letterSpacing: '0.08em' }],
    'label-sm':['9px',  { lineHeight: '12px', fontWeight: '600', letterSpacing: '0.10em' }],
  },

  // ─── Spacing (8-pt grid) ────────────────────────────────────────────────────
  // Base unit = 4px. Use multiples of 2 (8px, 16px, 24px…).
  // Never use arbitrary values outside this scale in components.
  spacing: {
    px:   '1px',
    0.5:  '2px',
    1:    '4px',
    1.5:  '6px',
    2:    '8px',
    2.5:  '10px',
    3:    '12px',
    4:    '16px',
    5:    '20px',
    6:    '24px',
    8:    '32px',
    10:   '40px',
    12:   '48px',
    16:   '64px',
  },

  // ─── Border radius ──────────────────────────────────────────────────────────
  // Keep it tight — this is a terminal, not a consumer app.
  radius: {
    sm:  '3px',
    md:  '6px',
    lg:  '8px',
    xl:  '12px',
    full:'9999px',
  },

  // ─── Shadows ────────────────────────────────────────────────────────────────
  shadows: {
    sm:  '0 1px 2px 0 rgb(0 0 0 / 0.4)',
    md:  '0 2px 8px 0 rgb(0 0 0 / 0.5)',
    lg:  '0 4px 20px 0 rgb(0 0 0 / 0.6)',
    glow:'0 0 12px 0 rgb(0 180 200 / 0.25)',
  },

  // ─── Motion ─────────────────────────────────────────────────────────────────
  // All transitions must be fast and functional, never decorative.
  motion: {
    fast:   '100ms ease-out',
    normal: '150ms ease-out',
    slow:   '250ms ease-out',
  },

  // ─── Layout ─────────────────────────────────────────────────────────────────
  layout: {
    sidebarWidth: '224px',
    pageMaxWidth:  '1280px',
    pagePadding:   '24px',
    headerHeight:  '48px',
  },
} as const

// ─── Design Rules (for all agents) ────────────────────────────────────────────
//
// SPACING
//   - Page content: px-6 py-6 (24px)
//   - Cards/panels: p-4 (16px)
//   - Table cells:  px-3 py-2 (compact), never px-6 in tables
//   - Section gaps: space-y-4 or space-y-6, never space-y-10+
//
// TYPOGRAPHY
//   - All numeric/market data: font-mono
//   - Column headers: text-label uppercase tracking-wider text-text-muted
//   - Page section headers: text-label uppercase text-text-muted (not h2 styles)
//   - Primary values: text-text-primary font-semibold
//   - Secondary values: text-text-secondary
//
// TABLES
//   - Always: sticky thead with bg-bg-elevated, divide-y divide-border-subtle
//   - Hover: hover:bg-bg-overlay on tbody rows
//   - No zebra striping
//   - Numeric columns: text-right font-mono
//
// COLOR SEMANTICS
//   - Positive numbers / success states: text-positive
//   - Negative numbers / error states: text-negative
//   - Interactive / links / active: text-accent
//   - Never use raw hex values in components
//
// ANTI-PATTERNS (never do these)
//   - No white/light backgrounds anywhere
//   - No rounded-2xl or larger radius
//   - No text-white (use text-text-primary)
//   - No shadow-xl decorative shadows
//   - No gradient backgrounds (gradients only for micro-details)
//   - No font-size below 10px
//   - No margin-auto centering of sidebar/nav elements
//   - No px-8 or larger in table cells
