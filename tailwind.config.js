/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',  // เส้นทางไปยังไฟล์ HTML ของคุณ
    './rooms/templates/**/*.html', // เพิ่มเส้นทางที่เหมาะสม
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
