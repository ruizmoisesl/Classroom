/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage:{
        "student": "url(../app/static/img/student.svg)",
        "teacher": "url(../app/static/img/teacher.svg)"

      }
    },
  },
  plugins: [],
}