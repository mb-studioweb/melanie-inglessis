(() => {
  const toggle = document.querySelector(".site-nav__toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  document.querySelectorAll(".site-menu a[href]").forEach((a) => {
    a.addEventListener("click", () => document.body.classList.remove("nav-open"));
  });

  const clock = document.querySelector("[data-live-clock]");
  if (clock) {
    const tick = () => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, "0");
      const mm = String(now.getMinutes()).padStart(2, "0");
      const offset = -now.getTimezoneOffset() / 60;
      const sign = offset >= 0 ? "+" : "";
      clock.textContent = `${hh}:${mm} (GMT${sign}${offset})`;
    };
    tick();
    setInterval(tick, 30000);
  }

  const filters = document.querySelector("[data-work-filters]");
  const grid = document.querySelector("[data-work-grid]");
  const countEl = document.querySelector("[data-work-count]");
  if (filters && grid) {
    filters.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      filters.querySelectorAll("button").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      const filter = btn.dataset.filter;
      let visible = 0;
      grid.querySelectorAll(".card").forEach((card) => {
        const cats = (card.dataset.categories || "").split(/\s+/);
        const show = filter === "ALL" || cats.includes(filter);
        card.classList.toggle("is-hidden", !show);
        if (show) visible += 1;
      });
      if (countEl) countEl.textContent = String(visible);
    });
  }

  const carousel = document.querySelector("[data-hero-carousel]");
  if (carousel) {
    const slides = [...carousel.querySelectorAll(".hero-carousel__slide")];
    const dots = [...carousel.querySelectorAll(".hero-carousel__dot")];
    let index = Math.max(0, slides.findIndex((s) => s.classList.contains("is-active")));
    let timer;

    const go = (next) => {
      index = (next + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle("is-active", i === index));
      dots.forEach((d, i) => d.classList.toggle("is-active", i === index));
    };
    const stop = () => { if (timer) clearInterval(timer); };
    const start = () => {
      stop();
      timer = setInterval(() => go(index + 1), 5500);
    };

    carousel.querySelector("[data-hero-prev]")?.addEventListener("click", () => { go(index - 1); start(); });
    carousel.querySelector("[data-hero-next]")?.addEventListener("click", () => { go(index + 1); start(); });
    dots.forEach((dot) => dot.addEventListener("click", () => { go(Number(dot.dataset.go)); start(); }));
    carousel.addEventListener("mouseenter", stop);
    carousel.addEventListener("mouseleave", start);
    start();
  }
})();
