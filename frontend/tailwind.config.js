/** @type {import('tailwindcss').Config} */
import { fontFamily } from 'tailwindcss/defaultTheme'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          base:     'var(--bg-base)',
          surface:  'var(--bg-surface)',
          elevated: 'var(--bg-elevated)',
          overlay:  'var(--bg-overlay)',
        },
        border: {
          subtle:  'var(--border-subtle)',
          default: 'var(--border-default)',
          strong:  'var(--border-strong)',
        },
        text: {
          primary:   'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted:     'var(--text-muted)',
          inverse:   'var(--text-inverse)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          subtle:  'var(--accent-subtle)',
          hover:   'var(--accent-hover)',
          dim:     'var(--accent-dim)',
        },
        positive: {
          DEFAULT: 'var(--positive)',
          subtle:  'var(--positive-subtle)',
        },
        negative: {
          DEFAULT: 'var(--negative)',
          subtle:  'var(--negative-subtle)',
        },
        warning: {
          DEFAULT: 'var(--warning)',
          subtle:  'var(--warning-subtle)',
        },
        success: {
          DEFAULT: 'var(--positive)',
          subtle:  'var(--positive-subtle)',
        },
        danger: {
          DEFAULT: 'var(--negative)',
          subtle:  'var(--negative-subtle)',
        },
      },
      fontFamily: {
        sans: ['Inter', ...fontFamily.sans],
        mono: ['JetBrains Mono', ...fontFamily.mono],
      },
      fontSize: {
        'data-xs': ['11px', { lineHeight: '16px', fontWeight: '500' }],
        'data-sm': ['13px', { lineHeight: '18px', fontWeight: '600' }],
        'data':    ['15px', { lineHeight: '22px', fontWeight: '600' }],
        'data-lg': ['20px', { lineHeight: '28px', fontWeight: '700' }],
        'data-xl': ['28px', { lineHeight: '36px', fontWeight: '700' }],
        'label':   ['10px', { lineHeight: '14px', fontWeight: '600', letterSpacing: '0.08em' }],
        'label-sm':['9px',  { lineHeight: '12px', fontWeight: '600', letterSpacing: '0.10em' }],
      },
      borderRadius: {
        sm:  '3px',
        md:  '6px',
        lg:  '8px',
        xl:  '12px',
      },
      boxShadow: {
        sm:   '0 1px 2px 0 rgb(0 0 0 / 0.4)',
        md:   '0 2px 8px 0 rgb(0 0 0 / 0.5)',
        lg:   '0 4px 20px 0 rgb(0 0 0 / 0.6)',
        glow: '0 0 12px 0 rgb(0 180 200 / 0.25)',
      },
      transitionDuration: {
        fast: '100ms',
        DEFAULT: '150ms',
      },
    },
  },
  plugins: [],
}
