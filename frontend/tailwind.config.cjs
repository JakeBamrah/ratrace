/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: "class", // or 'media' or 'class'
  theme: {
    colors: {
      ...colors,
      grey: {
      350: "#b0b0b0",
        ...colors.gray
      }
    },
    extend: {
      screens: {
        xs: '400px',
      }
    },
  },
  plugins: [],
}
