/** @type {import('tailwindcss').Config} */
import { fontFamily } from 'tailwindcss/defaultTheme'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          base:     '#0a0e17',
          surface:  '#0f1520',
          elevated: '#141c2b',
          overlay:  '#192234',
        },
        border: {
          subtle:  '#1a2236',
          default: '#1f2d45',
          strong:  '#2a3d5c',
        },
        text: {
          primary:   '#d4e0f5',
          secondary: '#6e88a8',
          muted:     '#354d6a',
          inverse:   '#0a0e17',
        },
        accent: {
          DEFAULT: '#00b4c8',
          subtle:  '#00232a',
          hover:   '#00cce0',
          dim:     '#007f8f',
        },
        positive: {
          DEFAULT: '#00d47a',
          subtle:  '#002e1c',
          dim:     '#009455',
        },
        negative: {
          DEFAULT: '#f0384f',
          subtle:  '#2b0c12',
          dim:     '#b02238',
        },
        warning: {
          DEFAULT: '#f5a623',
          subtle:  '#291a00',
        },
        // Legacy aliases kept for backward compat during migration
        success: {
          DEFAULT: '#00d47a',
          subtle:  '#002e1c',
        },
        danger: {
          DEFAULT: '#f0384f',
          subtle:  '#2b0c12',
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
