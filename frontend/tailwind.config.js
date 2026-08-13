/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#effbff',
          500: '#38bdf8',
          600: '#0ea5e9',
          700: '#0369a1',
        },
      },
    },
  },
  plugins: [],
};
