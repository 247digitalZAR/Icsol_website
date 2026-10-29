/* Replace only these values when the live integrations are ready. */
window.ICS_CONFIG = Object.freeze({
  CRM_FORM_ENDPOINT: "",
  CRM_CHECKLIST_ENDPOINT: "",
  CHATBOT_EMBED: "",
  GTM_ID: "",
  VACANCIES_URL: "",
  SHOW_TESTIMONIALS: false
});

/* Kept as editable data so ICS can amend the sizing guide without changing UI logic. */
window.ICS_TIERS = [
  {
    max: 9,
    title: "A few hours a week",
    body: "Mostly on call: a sounding board for the owner, with a short monthly check-in.",
    list: ["Contracts and policies set up once, then kept current", "Advice on warnings and difficult conversations", "Help with your next hire"]
  },
  {
    max: 30,
    title: "One to two days a week",
    body: "Enough time to run performance reviews, keep contracts current and handle issues as they come up.",
    list: ["A regular on-site day", "Performance reviews and probation management", "Discipline and grievances handled with you", "Job descriptions as roles are added"]
  },
  {
    max: 50,
    title: "Two days a week",
    body: "A standing HR function: structure, performance and employee relations run properly as the team grows.",
    list: ["Org structure and role design", "Performance and incentive framework", "Manager coaching and training", "Recruitment for growth roles"]
  },
  {
    max: 100,
    title: "Three days a week",
    body: "Your HR function, run for you: a senior HR executive on site most of the week, with the wider ICS team behind them.",
    list: ["Regular on-site days, plus same-day cover", "HR policies, procedures and compliance audits", "Employment equity and skills development reporting", "Workforce planning and recruitment for growth roles"]
  },
  {
    max: 249,
    title: "A full outsourced HR function",
    body: "A dedicated HR lead on site most days, backed by labour law, IR and recruitment specialists. The capability of an HR department, without building one.",
    list: ["A dedicated HR lead, four to five days a week", "Industrial relations and union engagement", "Training, facilitation and leadership development", "Monthly HR reporting to management"]
  },
  {
    max: 9999,
    title: "Talk to us",
    body: "At 250 people or more you likely have an HR team already. We add senior depth where it's needed.",
    list: ["Project support for your HR team", "Interim cover during a vacancy", "Recruit your next HR manager"]
  }
]);
