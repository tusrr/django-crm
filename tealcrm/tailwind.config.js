/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "client/templates/clients/*.html",
    "core/templates/core/*.html",
    "core/templates/core/partials/*.html",
    "dashboard/templates/dashboard/*.html",
    "leads/templates/leads/*.html",
    "team/templates/team/*.html",
    "userprofile/templates/userprofile/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
