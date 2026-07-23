/* ============================================================
   main.js — interactions, animations, easter eggs
   ============================================================ */
(function () {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- year ---------- */
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- theme ---------- */
  const root = document.documentElement;
  const savedTheme = (() => { try { return localStorage.getItem("pico-theme"); } catch (e) { return null; } })();
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.setAttribute("data-theme", savedTheme || (prefersDark ? "dark" : "light"));
  $("#themeToggle")?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("pico-theme", next); } catch (e) {}
  });

  /* ---------- language ---------- */
  const savedLang = (() => { try { return localStorage.getItem("pico-lang"); } catch (e) { return null; } })();
  window.PICO_I18N.applyLang(savedLang || "en");
  $("#langToggle")?.addEventListener("click", () => {
    const next = root.lang === "ar" ? "en" : "ar";
    window.PICO_I18N.applyLang(next);
  });

  /* ---------- nav: scroll state + mobile menu ---------- */
  const nav = $("#nav");
  const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 10);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const burger = $("#burger"), navMobile = $("#navMobile");
  burger?.addEventListener("click", () => {
    const open = navMobile.classList.toggle("is-open");
    burger.setAttribute("aria-expanded", String(open));
  });
  $$("#navMobile a").forEach((a) => a.addEventListener("click", () => {
    navMobile.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
  }));

  /* ---------- scroll reveal ---------- */
  const revealTargets = [
    ".section-head", ".stats__inner", ".grow__layout", ".grow__more",
    ".heritage__media", ".heritage__copy", ".cert", ".f2f__step", ".reach__copy", ".reach__map", ".reach__list li", ".contact__panel"
  ];
  const revealEls = [];
  revealTargets.forEach((sel) => $$(sel).forEach((el) => { el.classList.add("reveal"); revealEls.push(el); }));
  if (REDUCED) {
    revealEls.forEach((el) => el.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          e.target.style.transitionDelay = (Math.min(i, 4) * 60) + "ms";
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  }

  /* ---------- animated counters ---------- */
  const counters = $$(".stat__num");
  const fmt = (n) => n >= 1000 ? n.toLocaleString(root.lang === "ar" ? "ar-EG" : "en-US") : String(n);
  const runCount = (el) => {
    const target = parseInt(el.dataset.count, 10);
    if (REDUCED) { el.textContent = fmt(target); return; }
    const dur = 1400, start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { runCount(e.target); countIO.unobserve(e.target); } });
  }, { threshold: 0.5 });
  counters.forEach((c) => countIO.observe(c));
  // re-render numbers on language change (locale digits)
  window.addEventListener("langchange", () => counters.forEach((c) => { if (c.textContent !== "0") c.textContent = fmt(parseInt(c.dataset.count, 10)); }));

  /* ---------- 3D fruit viewers ---------- */
  let heroViewer = null, fruitViewer = null;
  if (window.THREE && window.THREE.OrbitControls && window.PICO_FRUITS) {
    const heroCanvas = $("#heroCanvas");
    if (heroCanvas) heroViewer = window.PICO_FRUITS.makeViewer(heroCanvas, { fruit: "strawberry", autoRotateSpeed: 1.4 });

    const fruitCanvas = $("#fruitCanvas");
    if (fruitCanvas) {
      fruitViewer = window.PICO_FRUITS.makeViewer(fruitCanvas, { fruit: "strawberry", autoRotateSpeed: 1.8 });
      $$(".fruit-tab").forEach((tab) => {
        tab.addEventListener("click", () => {
          const fruit = tab.dataset.fruit;
          fruitViewer.setFruit(fruit);
          $$(".fruit-tab").forEach((t) => { t.classList.remove("is-active"); t.setAttribute("aria-selected", "false"); });
          tab.classList.add("is-active"); tab.setAttribute("aria-selected", "true");
          $$(".fruit-card").forEach((c) => { c.hidden = c.dataset.panel !== fruit; });
        });
      });
    }

    /* Easter egg #1: click the hero strawberry 5x → it spins wildly */
    let clicks = 0, clickTimer = null;
    heroCanvas?.addEventListener("pointerdown", () => {
      clicks++;
      clearTimeout(clickTimer);
      clickTimer = setTimeout(() => (clicks = 0), 1200);
      if (clicks >= 5) { clicks = 0; heroViewer?.kickSpin(); dropFruit(14); }
    });
  } else {
    // graceful fallback if WebGL/CDN unavailable
    $$("#heroCanvas, #fruitCanvas").forEach((c) => {
      const wrap = document.createElement("div");
      wrap.textContent = "🍓";
      wrap.style.cssText = "font-size:8rem;display:grid;place-items:center;height:100%;";
      c.replaceWith(wrap);
    });
  }

  /* ---------- global-reach trade-routes diagram ---------- */
  (function buildRoutes() {
    const svg = $(".routes");
    if (!svg) return;
    const SVGNS = "http://www.w3.org/2000/svg";
    const hub = { x: 300, y: 215 };
    const dests = [
      { x: 110, y: 80, label: "UK" },
      { x: 300, y: 52, label: "Europe" },
      { x: 488, y: 84, label: "Russia" },
      { x: 548, y: 222, label: "Far East" },
      { x: 450, y: 332, label: "Gulf" },
      { x: 236, y: 356, label: "S. Africa" }
    ];
    const lines = $(".routes__lines", svg);
    const nodes = $(".routes__nodes", svg);

    dests.forEach((d, i) => {
      const mx = (hub.x + d.x) / 2, my = (hub.y + d.y) / 2;
      // perpendicular bow for a gentle arc
      const dx = d.x - hub.x, dy = d.y - hub.y;
      const cx = mx - dy * 0.18, cy = my + dx * 0.18;
      const path = document.createElementNS(SVGNS, "path");
      path.setAttribute("d", `M${hub.x},${hub.y} Q${cx},${cy} ${d.x},${d.y}`);
      path.setAttribute("class", "route-line");
      path.style.animationDelay = (i * 0.35) + "s";
      lines.appendChild(path);

      const pulse = document.createElementNS(SVGNS, "circle");
      pulse.setAttribute("cx", d.x); pulse.setAttribute("cy", d.y); pulse.setAttribute("r", 4.5);
      pulse.setAttribute("class", "route-node");
      pulse.style.animationDelay = (i * 0.35) + "s";
      nodes.appendChild(pulse);

      const label = document.createElementNS(SVGNS, "text");
      const left = d.x < hub.x;
      label.setAttribute("x", d.x + (left ? -10 : 10));
      label.setAttribute("y", d.y - 9);
      label.setAttribute("text-anchor", left ? "end" : "start");
      label.setAttribute("class", "route-label");
      label.textContent = d.label;
      nodes.appendChild(label);
    });

    // hub (Egypt / PICO)
    const ring = document.createElementNS(SVGNS, "circle");
    ring.setAttribute("cx", hub.x); ring.setAttribute("cy", hub.y); ring.setAttribute("r", 9);
    ring.setAttribute("class", "route-hub-ring");
    nodes.appendChild(ring);
    const hubDot = document.createElementNS(SVGNS, "circle");
    hubDot.setAttribute("cx", hub.x); hubDot.setAttribute("cy", hub.y); hubDot.setAttribute("r", 7);
    hubDot.setAttribute("fill", "url(#hub)");
    nodes.appendChild(hubDot);
    const hubLabel = document.createElementNS(SVGNS, "text");
    hubLabel.setAttribute("x", hub.x); hubLabel.setAttribute("y", hub.y + 26);
    hubLabel.setAttribute("text-anchor", "middle");
    hubLabel.setAttribute("class", "route-hub-label");
    hubLabel.textContent = "Egypt · PICO";
    nodes.appendChild(hubLabel);
  })();

  /* ---------- contact form (demo validation) ---------- */
  const form = $("#contactForm");
  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const dict = window.PICO_I18N.dict();
    const name = $("#cName"), email = $("#cEmail");
    let ok = true;
    const setValid = (input, valid) => input.closest(".field").classList.toggle("is-invalid", !valid);
    const nameOk = name.value.trim().length > 1; setValid(name, nameOk); ok = ok && nameOk;
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim()); setValid(email, emailOk); ok = ok && emailOk;
    const note = $("#formNote");
    if (ok) {
      note.textContent = dict.formSuccess;
      form.reset();
    } else {
      note.textContent = "";
    }
  });

  /* =========================================================
     EASTER EGGS
     ========================================================= */

  /* helper: rain fruit from the top */
  const FRUIT_EMOJI = ["🍓", "🥭", "🍊", "🍇", "🍑", "🥑", "🍌"];
  function dropFruit(count) {
    if (REDUCED) return;
    const layer = $("#fruitRain");
    for (let i = 0; i < count; i++) {
      const s = document.createElement("span");
      s.textContent = FRUIT_EMOJI[(Math.random() * FRUIT_EMOJI.length) | 0];
      s.style.left = Math.random() * 100 + "vw";
      s.style.fontSize = (1.4 + Math.random() * 1.8) + "rem";
      const dur = 2.4 + Math.random() * 2.2;
      s.style.animationDuration = dur + "s";
      s.style.animationDelay = (Math.random() * 0.4) + "s";
      layer.appendChild(s);
      setTimeout(() => s.remove(), (dur + 0.6) * 1000);
    }
  }

  /* Easter egg #2: Konami code → fruit storm */
  const KONAMI = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  let ki = 0;
  window.addEventListener("keydown", (e) => {
    const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    ki = (key === KONAMI[ki]) ? ki + 1 : (key === KONAMI[0] ? 1 : 0);
    if (ki === KONAMI.length) {
      ki = 0;
      dropFruit(60);
      document.body.animate(
        [{ filter: "hue-rotate(0deg)" }, { filter: "hue-rotate(28deg)" }, { filter: "hue-rotate(0deg)" }],
        { duration: 900 }
      );
    }
  });

  /* Easter egg #3: the footer tractor drives off, dropping fruit */
  $("#tractor")?.addEventListener("click", (e) => {
    const t = e.currentTarget;
    if (t.classList.contains("is-driving")) return;
    t.classList.add("is-driving");
    dropFruit(8);
    setTimeout(() => t.classList.remove("is-driving"), 2600);
  });

  /* Easter egg #4: console message */
  const style1 = "color:#6fbf2f;font-size:15px;font-weight:bold;font-family:sans-serif";
  const style2 = "color:#5c6c60;font-size:12px;font-family:sans-serif";
  console.log("%c🍓 PICO Modern Agriculture", style1);
  console.log("%cThird-generation growers, now leaving footprints in the console too.\nTry the Konami code (↑ ↑ ↓ ↓ ← → ← → b a), tap the hero strawberry five times, or honk the tractor in the footer.", style2);
})();
