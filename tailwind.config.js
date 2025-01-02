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
        nyxNavBlackTop: '#0D0D0D',
        nyxNavBlackBottom: '#18001C',
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
      boxShadow: {
        pinkGlow: '0 8px 40px 0 rgba(158, 4, 172, 0.25)'
      },
    },
  },
  plugins: [],
}

