/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        teal: {
          primary: '#0d8e84',
          dark:    '#0b7a71',
          light:   '#e6f7f6',
          lighter: '#f0faf9',
          border:  '#b2e0dd',
          text:    '#0a5e57',
          muted:   '#5ca89f',
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
