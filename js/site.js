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
  const viewToggle = document.querySelector("[data-view-toggle]");

  const applyFilter = (filter) => {
    if (!grid) return;
    let visible = 0;
    grid.querySelectorAll(".card").forEach((card) => {
      const cats = (card.dataset.categories || "").split(/\s+/).filter(Boolean);
      const show = filter === "ALL" || cats.includes(filter);
      card.classList.toggle("is-hidden", !show);
      if (show) visible += 1;
    });
    if (countEl) countEl.textContent = String(visible);
  };

  if (filters && grid) {
    filters.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      filters.querySelectorAll("button").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      applyFilter(btn.dataset.filter || "ALL");
    });
  }

  const setView = (view) => {
    if (!grid) return;
    const mode = view === "list" ? "list" : "grid";
    grid.dataset.view = mode;
    grid.classList.toggle("work-view--grid", mode === "grid");
    grid.classList.toggle("work-view--list", mode === "list");
    if (viewToggle) {
      viewToggle.querySelectorAll("button[data-view]").forEach((b) => {
        const on = b.dataset.view === mode;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }
    try {
      localStorage.setItem("work-view", mode);
    } catch (_) {}
  };

  if (viewToggle && grid) {
    viewToggle.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-view]");
      if (!btn) return;
      setView(btn.dataset.view);
    });
    let saved = "grid";
    try {
      saved = localStorage.getItem("work-view") || "grid";
    } catch (_) {}
    setView(saved);
  }

  const carousel = document.querySelector("[data-hero-carousel]");
  if (carousel) {
    const root = carousel.closest(".hero-identity--carousel") || document;
    const slides = [...carousel.querySelectorAll(".hero-carousel__slide")];
    const dots = [...root.querySelectorAll(".hero-carousel__dot")];
    const titleEl = root.querySelector("[data-hero-title]");
    const metaEl = root.querySelector("[data-hero-meta]");
    const linkEl = root.querySelector("[data-hero-link]");
    const prevBtn = root.querySelector("[data-hero-prev]");
    const nextBtn = root.querySelector("[data-hero-next]");
    let index = Math.max(0, slides.findIndex((s) => s.classList.contains("is-active")));
    let timer;
    let pointerId = null;
    let startX = 0;
    let startY = 0;
    let tracking = false;
    let swiped = false;

    const syncText = (slide) => {
      if (!slide) return;
      if (titleEl) titleEl.textContent = slide.dataset.title || "";
      if (metaEl) metaEl.textContent = slide.dataset.meta || "";
      if (linkEl && slide.dataset.href) linkEl.setAttribute("href", slide.dataset.href);
    };

    const go = (next) => {
      if (!slides.length) return;
      index = ((next % slides.length) + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle("is-active", i === index));
      dots.forEach((d, i) => d.classList.toggle("is-active", i === index));
      syncText(slides[index]);
    };

    const stop = () => {
      if (timer) clearInterval(timer);
      timer = null;
    };
    const start = () => {
      stop();
      if (slides.length > 1) timer = setInterval(() => go(index + 1), 5000);
    };

    prevBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      go(index - 1);
      start();
    });
    nextBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      go(index + 1);
      start();
    });
    dots.forEach((dot) => {
      dot.addEventListener("click", (e) => {
        e.preventDefault();
        go(Number(dot.dataset.go) || 0);
        start();
      });
    });

    const onPointerDown = (e) => {
      if (e.target.closest("a, button")) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      pointerId = e.pointerId;
      startX = e.clientX;
      startY = e.clientY;
      tracking = true;
      swiped = false;
      root.classList.add("is-dragging");
      stop();
      try {
        root.setPointerCapture(pointerId);
      } catch (_) {}
    };

    const onPointerMove = (e) => {
      if (!tracking || e.pointerId !== pointerId) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      if (!swiped && Math.abs(dx) > 28 && Math.abs(dx) > Math.abs(dy) * 1.15) {
        swiped = true;
        go(dx < 0 ? index + 1 : index - 1);
      }
    };

    const onPointerUp = (e) => {
      if (e.pointerId !== pointerId) return;
      tracking = false;
      pointerId = null;
      root.classList.remove("is-dragging");
      start();
    };

    root.addEventListener("pointerdown", onPointerDown);
    root.addEventListener("pointermove", onPointerMove);
    root.addEventListener("pointerup", onPointerUp);
    root.addEventListener("pointercancel", onPointerUp);
    root.addEventListener("pointerleave", (e) => {
      if (tracking && e.pointerType === "mouse") onPointerUp(e);
    });

    // Prevent accidental link navigation after a swipe
    linkEl?.addEventListener("click", (e) => {
      if (swiped) {
        e.preventDefault();
        swiped = false;
      }
    });

    root.addEventListener("mouseenter", stop);
    root.addEventListener("mouseleave", start);
    syncText(slides[index]);
    start();
  }
})();
