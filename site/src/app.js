/* Production interactions. Content remains fully available when JavaScript is disabled. */
(() => {
  "use strict";

  const config = window.ICS_CONFIG || {};
  const consentKey = "ics-cookie-consent";
  const consentWording = "I agree that ICS may use these details to contact me about my enquiry, in line with the ICS POPIA privacy notice. You can ask us to delete them at any time.";
  const hasValue = (value) => typeof value === "string" && value.trim().length > 0;

  function event(name, detail = {}) {
    if (localStorage.getItem(consentKey) !== "accepted") return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: name, ...detail });
  }

  function loadGtm() {
    if (!hasValue(config.GTM_ID) || document.querySelector("script[data-ics-gtm]")) return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
    const script = document.createElement("script");
    script.async = true;
    script.dataset.icsGtm = "true";
    script.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(config.GTM_ID)}`;
    document.head.appendChild(script);
  }

  function loadChatbot() {
    if (!hasValue(config.CHATBOT_EMBED) || document.querySelector("script[data-ics-chatbot]")) return;
    const launcher = document.querySelector(".chat-launcher");
    if (launcher) launcher.hidden = false;
    const holder = document.createElement("template");
    holder.innerHTML = config.CHATBOT_EMBED.trim();
    const script = holder.content.querySelector("script");
    if (script) {
      const liveScript = document.createElement("script");
      [...script.attributes].forEach((attribute) => liveScript.setAttribute(attribute.name, attribute.value));
      liveScript.dataset.icsChatbot = "true";
      document.body.appendChild(liveScript);
    }
  }

  function applyConsent() {
    const choice = localStorage.getItem(consentKey);
    document.querySelector(".cookie-banner")?.toggleAttribute("hidden", Boolean(choice));
    if (choice === "accepted") {
      loadGtm();
      loadChatbot();
    }
  }

  function initCookieBanner() {
    document.querySelectorAll("[data-consent]").forEach((button) => {
      button.addEventListener("click", () => {
        localStorage.setItem(consentKey, button.dataset.consent);
        applyConsent();
      });
    });
    applyConsent();
  }

  function initMenu() {
    const button = document.querySelector(".menu-btn");
    const nav = document.querySelector("nav.main");
    if (!button || !nav) return;
    button.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      button.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", (eventTarget) => {
      if (eventTarget.target.closest("a")) {
        nav.classList.remove("open");
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function initSizingTool() {
    const range = document.getElementById("headcount");
    const output = document.getElementById("hc-out");
    const result = document.querySelector(".result");
    if (!range || !output || !result) return;
    const stops = [[0, 5], [400, 25], [600, 50], [800, 100], [1000, 250]];
    const peopleForValue = (value) => {
      for (let index = 1; index < stops.length; index += 1) {
        const start = stops[index - 1];
        const end = stops[index];
        if (value <= end[0]) {
          const people = start[1] + ((value - start[0]) * (end[1] - start[1])) / (end[0] - start[0]);
          return people > 100 ? Math.round(people / 5) * 5 : Math.round(people);
        }
      }
      return 250;
    };
    const update = () => {
      const people = peopleForValue(Number(range.value));
      const label = `${people}${people >= 250 ? "+" : ""}`;
      const tier = (window.ICS_TIERS || []).find((item) => people <= item.max);
      output.textContent = label;
      range.setAttribute("aria-valuetext", `${label} people`);
      if (!tier) return;
      document.getElementById("r-title").textContent = tier.title;
      document.getElementById("r-body").textContent = tier.body;
      document.getElementById("r-list").innerHTML = tier.list.map((item) => `<li>${item}</li>`).join("");
      result.classList.remove("bump");
      void result.offsetWidth;
      result.classList.add("bump");
      event("slider_change", { tier: tier.title, page: location.pathname });
    };
    range.addEventListener("input", update);
    update();
  }

  function utmParameters() {
    const search = new URLSearchParams(location.search);
    return Object.fromEntries([...search.entries()].filter(([key]) => key.toLowerCase().startsWith("utm_")));
  }

  function setFormMessage(form, message, state) {
    const messageElement = form.querySelector("[data-form-message]");
    if (!messageElement) return;
    messageElement.hidden = false;
    messageElement.textContent = message;
    messageElement.dataset.state = state;
  }

  async function submitLeadForm(form) {
    const endpoint = form.dataset.endpoint === "checklist" ? config.CRM_CHECKLIST_ENDPOINT : config.CRM_FORM_ENDPOINT;
    const honeypot = form.querySelector("[name=website]");
    if (honeypot?.value) return;
    if (!form.reportValidity()) return;
    const consent = form.querySelector("[name=consent]");
    if (consent && !consent.checked) {
      setFormMessage(form, "Please tick the consent box so we can contact you.", "error");
      return;
    }
    if (!hasValue(endpoint)) {
      setFormMessage(form, "Online submissions are being connected. Please call us on 082 921 9965 or email admin@icsol.co.za.", "error");
      return;
    }
    const data = Object.fromEntries(new FormData(form).entries());
    const payload = {
      ...data,
      form_name: form.dataset.formName || "enquiry",
      page_url: location.href,
      utm_parameters: utmParameters(),
      timestamp: new Date().toISOString(),
      consent_wording: consent ? consentWording : undefined
    };
    const submit = form.querySelector("button[type=submit]");
    submit.disabled = true;
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("CRM request failed");
      setFormMessage(form, form.dataset.endpoint === "checklist" ? "Thanks, you're on the list. We'll send the checklist shortly." : "Thanks, request received. We'll call you back within one business day.", "success");
      form.reset();
      event("form_submit", { form_name: form.dataset.formName || "enquiry", page: location.pathname });
    } catch (error) {
      setFormMessage(form, "We couldn't send that right now. Please call us on 082 921 9965 or email admin@icsol.co.za.", "error");
    } finally {
      submit.disabled = false;
    }
  }

  function initForms() {
    document.querySelectorAll("form[data-lead-form]").forEach((form) => {
      let started = false;
      form.addEventListener("input", () => {
        if (started) return;
        started = true;
        event("form_start", { form_name: form.dataset.formName || "enquiry", page: location.pathname });
      }, { once: true });
      form.addEventListener("submit", (submission) => {
        submission.preventDefault();
        submitLeadForm(form);
      });
    });
  }

  function initInsightFilters() {
    const chips = [...document.querySelectorAll("[data-filter]")];
    const items = [...document.querySelectorAll("[data-category]")];
    const empty = document.querySelector("[data-filter-empty]");
    if (!chips.length || !items.length) return;
    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const filter = chip.dataset.filter;
        let visible = 0;
        chips.forEach((item) => item.classList.toggle("on", item === chip));
        items.forEach((item) => {
          const show = filter === "all" || item.dataset.category === filter;
          item.hidden = !show;
          if (show) visible += 1;
        });
        if (empty) empty.hidden = visible > 0;
      });
    });
  }

  function initVacanciesLink() {
    const link = document.querySelector("[data-vacancies-link]");
    if (!link || !hasValue(config.VACANCIES_URL)) return;
    link.href = config.VACANCIES_URL;
    link.target = "_blank";
    link.rel = "noopener";
  }

  function initAnalyticsEvents() {
    document.querySelectorAll("a.btn, a[href^='tel:'], a[href^='mailto:']").forEach((link) => {
      link.addEventListener("click", () => {
        const href = link.getAttribute("href") || "";
        if (href.startsWith("tel:")) event("phone_click", { page: location.pathname });
        else if (href.startsWith("mailto:")) event("email_click", { page: location.pathname });
        else event("cta_click", { label: link.textContent.trim(), page: location.pathname });
      });
    });
    let articleRead = false;
    addEventListener("scroll", () => {
      if (articleRead || !document.querySelector(".read")) return;
      const height = document.documentElement.scrollHeight - innerHeight;
      if (height > 0 && scrollY / height >= 0.75) {
        articleRead = true;
        event("article_read", { page: location.pathname });
      }
    }, { passive: true });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initCookieBanner();
    initMenu();
    initSizingTool();
    initForms();
    initInsightFilters();
    initVacanciesLink();
    initAnalyticsEvents();
    document.querySelector(".chat-launcher")?.addEventListener("click", () => event("chat_open", { page: location.pathname }));
  });
})();
