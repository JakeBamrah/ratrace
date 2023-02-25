/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: "class", // or 'media' or 'class'
  theme: {
    colors: {
      ...colors,
      grey: {...colors.gray}
    },
    extend: {
      screens: {
        xs: '400px',
      }
    },
  },
  plugins: [],
}
