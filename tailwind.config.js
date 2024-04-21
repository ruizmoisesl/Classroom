/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage:{
        "profile": "{{url_for('static', filename= 'img/profile.png')}}"
      }
    },
  },
  plugins: [],
}