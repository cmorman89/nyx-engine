/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './index_2.html',
  ],
  theme: {
    extend: {
      colors: {
        nyx: '#00002B',
        nyxDarkPurpleBlue: '#1a0751',
        nyxDarkPurple: '#19021B',
        // header_purple: '#190432',
        nyxTerminalGreen: '#45CD45'
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        pixelify: ['Pixelify Sans', 'sans-serif'],
        ptSansNarrow: ['PT Sans Narrow', 'sans-serif'],
      },
      lineHeight: {
        hero: '1.40',
      },
    },
  },
  plugins: [],
}

