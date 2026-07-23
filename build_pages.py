#!/usr/bin/env python3
"""Generate PICO's multi-page static site from shared parts.
Run:  python3 build_pages.py   (outputs index.html, about.html, etc.)
Edit content here, not in the generated HTML."""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
 '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
 '  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,600&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet" />\n'
 '  <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />')

NAV_ITEMS = [
    ("home",   "index.html",         "navHome",     "Home"),
    ("about",  "about.html",         "navAbout",    "About"),
    ("crop",   "crop-calendar.html", "navCrop",     "Crop Calendar"),
    ("value",  "value-add.html",     "navValue",    "Value-Add"),
    ("std",    "standards.html",     "navStandards","Standards"),
    ("contact","contact.html",       "navContact",  "Contact"),
]

LOGO_SVG = ('<svg class="pico-logo" viewBox="0 0 172 66" width="104" height="40" role="img" aria-label="PICO">\n'
 '          <defs>\n'
 '            <linearGradient id="picoRed" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c4052e"/><stop offset="1" stop-color="#ea6288"/></linearGradient>\n'
 '            <linearGradient id="picoLeaf" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#5fa828"/><stop offset="1" stop-color="#9bd34a"/></linearGradient>\n'
 '          </defs>\n'
 '          <path d="M40 31 C42 15 55 4 66 2 C61 17 52 27 46 29 Z" fill="url(#picoLeaf)"/>\n'
 '          <path d="M62 6 C54 13 48 21 44 28" fill="none" stroke="#ffffff" stroke-opacity=".45" stroke-width="1.4" stroke-linecap="round"/>\n'
 '          <text x="0" y="55" font-family="Montserrat, sans-serif" font-weight="800" font-size="56" letter-spacing="-2" fill="url(#picoRed)">PICO</text>\n'
 '        </svg>')

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#d60633" />
  <meta property="og:title" content="PICO Modern Agriculture" />
  <meta property="og:description" content="As fresh as it gets. Family-grown Egyptian fruit since 1974." />
  <meta property="og:type" content="website" />
  {FONTS}
  <link rel="stylesheet" href="css/styles.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍓</text></svg>" />
</head>
<body>
  <div class="grain" aria-hidden="true"></div>
  <a href="#main" class="skip-link" data-i18n="skip">Skip to content</a>'''

def nav(active):
    links = "\n".join(
        f'        <a href="{url}" class="{"is-current" if key==active else ""}" data-i18n="{i18n}">{label}</a>'
        for key,url,i18n,label in NAV_ITEMS)
    mlinks = "\n".join(
        f'      <a href="{url}" data-i18n="{i18n}">{label}</a>'
        for key,url,i18n,label in NAV_ITEMS)
    return f'''
  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="brand" aria-label="PICO Modern Agriculture home">
        {LOGO_SVG}
        <span class="brand__sub" data-i18n="brandSub">Modern Agriculture</span>
      </a>
      <nav class="nav__links" aria-label="Primary">
{links}
      </nav>
      <div class="nav__actions">
        <button class="chip" id="langToggle" aria-label="Switch language"><span id="langLabel">العربية</span></button>
        <button class="chip chip--icon" id="themeToggle" aria-label="Toggle dark mode">
          <svg class="ico-sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
          <svg class="ico-moon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
        </button>
        <a href="contact.html" class="btn btn--sm" data-i18n="navCta">Talk to sales</a>
        <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
    <div class="nav__mobile" id="navMobile">
{mlinks}
    </div>
  </header>
'''

def page_hero(tkey, skey):
    return f'''
    <section class="page-hero">
      <div class="page-hero__inner">
        <h1 data-i18n="{tkey}">Page</h1>
        <p data-i18n="{skey}">Subtitle</p>
      </div>
    </section>'''

CTA_BAND = '''
    <section class="cta-band">
      <div class="cta-band__inner">
        <h2 data-i18n="ctaBandT">Let's get your shelves stocked.</h2>
        <a href="contact.html" class="btn" data-i18n="ctaBandBtn">Talk to sales</a>
      </div>
    </section>'''

FOOTER = '''
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <svg class="pico-logo pico-logo--footer" viewBox="0 0 172 66" width="120" height="46" role="img" aria-label="PICO">
          <defs><linearGradient id="picoRedF" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c4052e"/><stop offset="1" stop-color="#ea6288"/></linearGradient></defs>
          <path d="M40 31 C42 15 55 4 66 2 C61 17 52 27 46 29 Z" fill="#7ac143"/>
          <text x="0" y="55" font-family="Montserrat, sans-serif" font-weight="800" font-size="56" letter-spacing="-2" fill="url(#picoRedF)">PICO</text>
        </svg>
        <p data-i18n="footerTag">As fresh as it gets. From our farms straight to your home.</p>
        <div class="footer__social">
          <a href="https://facebook.com/PicoEg" target="_blank" rel="noopener" aria-label="Facebook"><i class="ph ph-facebook-logo"></i></a>
          <a href="https://instagram.com/pico.eg" target="_blank" rel="noopener" aria-label="Instagram"><i class="ph ph-instagram-logo"></i></a>
          <a href="https://www.linkedin.com/company/pico-modern-agriculture-company" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="ph ph-linkedin-logo"></i></a>
        </div>
      </div>
      <div class="footer__cols">
        <div>
          <h4 data-i18n="footerColProduce">Harvest</h4>
          <a href="crop-calendar.html" data-i18n="navGrow">What we grow</a>
          <a href="value-add.html" data-i18n="navRange">Products</a>
          <a href="value-add.html" data-i18n="footerBrands">Our brands</a>
        </div>
        <div>
          <h4 data-i18n="footerColCompany">Company</h4>
          <a href="about.html" data-i18n="navHeritage">Heritage</a>
          <a href="standards.html" data-i18n="navStandards">Standards</a>
          <a href="standards.html" data-i18n="navReach">Global reach</a>
        </div>
        <div>
          <h4 data-i18n="footerColConnect">Connect</h4>
          <a href="contact.html" data-i18n="navContact">Contact</a>
          <a href="mailto:info@pico-agriculture.com">info@pico-agriculture.com</a>
          <a href="tel:+20233377266">(+202) 3337-7266</a>
        </div>
      </div>
    </div>
    <div class="footer__base">
      <span data-i18n="footerRights">© <span id="year"></span> PICO Modern Agriculture. Concept redesign.</span>
      <button class="tractor" id="tractor" aria-label="🚜" title="beep beep">🚜</button>
    </div>
  </footer>
  <div class="fruit-rain" id="fruitRain" aria-hidden="true"></div>'''

def scripts(three=False):
    libs = ('  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n'
            '  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>\n'
            '  <script src="js/fruits3d.js"></script>\n') if three else ''
    return f'''
{libs}  <script src="js/i18n.js"></script>
  <script src="js/main.js"></script>
</body>
</html>'''

# ---------- reusable section blocks ----------
PHONE_HERO = '''
    <section class="hero">
      <div class="hero__glow" aria-hidden="true"></div>
      <div class="hero__grid">
        <div class="hero__copy">
          <span class="eyebrow" data-i18n="heroEyebrow">As fresh as it gets</span>
          <h1 class="hero__title">
            <span data-i18n="heroTitle1">From our farms</span>
            <span class="hero__accent" data-i18n="heroTitle2">straight to your home.</span>
          </h1>
          <p class="hero__lede" data-i18n="heroLede">A family-grown Egyptian harvest since 1974. Premium fruit, picked on order and delivered at its peak.</p>
          <div class="hero__cta">
            <a href="crop-calendar.html" class="btn" data-i18n="heroCtaPrimary">Explore the harvest</a>
            <a href="contact.html" class="btn btn--ghost" data-i18n="heroCtaSecondary">Talk to sales</a>
          </div>
          <div class="hero__apps">
            <span class="store-badge"><i class="ph ph-google-play-logo" aria-hidden="true"></i><span><small data-i18n="getItOn">Get it on</small>Google Play</span></span>
            <span class="store-badge"><i class="ph ph-apple-logo" aria-hidden="true"></i><span><small data-i18n="downloadOn">Download on the</small>App Store</span></span>
          </div>
        </div>
        <div class="hero__stage">
          <div class="hero__blob" aria-hidden="true"></div>
          <div class="phone" role="img" aria-label="The PICO app placing a fresh produce order">
            <div class="phone__frame">
              <div class="phone__notch"></div>
              <div class="phone__screen">
                <div class="app">
                  <div class="app__bar">
                    <span class="app__loc"><i class="ph ph-map-pin"></i> <b data-i18n="appDeliver">Cairo</b></span>
                    <svg class="app__logo" viewBox="0 0 172 66" width="52" height="20" aria-hidden="true"><path d="M40 31 C42 15 55 4 66 2 C61 17 52 27 46 29 Z" fill="#7ac143"/><text x="0" y="55" font-family="Montserrat, sans-serif" font-weight="800" font-size="56" letter-spacing="-2" fill="#d60633">PICO</text></svg>
                  </div>
                  <div class="app__search"><i class="ph ph-magnifying-glass"></i> <span data-i18n="appSearch">Search fresh produce…</span></div>
                  <div class="app__banner"><span data-i18n="appBanner">Harvest upon order</span></div>
                  <div class="app__feedwrap">
                    <div class="app__feed">
                      <div class="prod"><span class="prod__img prod--straw"></span><div><b data-i18n="prodStraw">Frozen Strawberries</b><span class="prod__price">EGP 419</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--honey"></span><div><b data-i18n="prodHoney">Anise Honey 350g</b><span class="prod__price">EGP 96</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--corn"></span><div><b data-i18n="prodCorn">Super Sweet Corn</b><span class="prod__price">EGP 40</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--mango"></span><div><b data-i18n="prodMango">Frozen Mango</b><span class="prod__price">EGP 210</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--avo"></span><div><b data-i18n="prodAvo">PICO Avocado</b><span class="prod__price">EGP 85</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--straw"></span><div><b data-i18n="prodStraw">Frozen Strawberries</b><span class="prod__price">EGP 419</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--honey"></span><div><b data-i18n="prodHoney">Anise Honey 350g</b><span class="prod__price">EGP 96</span></div><span class="prod__add">+</span></div>
                      <div class="prod"><span class="prod__img prod--corn"></span><div><b data-i18n="prodCorn">Super Sweet Corn</b><span class="prod__price">EGP 40</span></div><span class="prod__add">+</span></div>
                    </div>
                  </div>
                  <div class="app__toast"><i class="ph ph-check-circle"></i> <span data-i18n="appToast">Order placed — harvesting now</span></div>
                </div>
              </div>
            </div>
            <span class="float-fruit float-fruit--1">🍓</span>
            <span class="float-fruit float-fruit--2">🥭</span>
            <span class="float-fruit float-fruit--3">🥑</span>
          </div>
        </div>
      </div>
    </section>'''

TRUST = '''
    <section class="trust" aria-label="Certifications">
      <div class="trust__inner">
        <span class="trust__label" data-i18n="trustLabel">Audited to the standards buyers require</span>
        <div class="trust__marks"><span>GlobalG.A.P.</span><span>BRC</span><span>ISO 9001</span><span>SEDEX · ETI</span><span>LEAF Marque</span><span>Select Farm</span></div>
      </div>
    </section>'''

STATS = '''
    <section class="stats" aria-label="Company at a glance">
      <div class="stats__inner">
        <div class="stat"><span class="stat__num" data-count="1974" data-plain="1">0</span><span class="stat__label" data-i18n="statSince">Growing since</span></div>
        <div class="stat"><span class="stat__num" data-count="3">0</span><span class="stat__label" data-i18n="statGen">Generations, one family</span></div>
        <div class="stat"><span class="stat__num" data-count="75" data-suffix="%">0</span><span class="stat__label" data-i18n="statGrapes">of Egypt's grape exports</span></div>
        <div class="stat"><span class="stat__num" data-count="4" data-prefix="#">0</span><span class="stat__label" data-i18n="statStraw">World strawberry producer</span></div>
      </div>
    </section>'''

HOME_TEASER = '''
    <section class="teaser">
      <div class="section-head section-head--center"><h2 data-i18n="homeExploreT">Explore PICO</h2></div>
      <div class="teaser__grid">
        <a class="teaser-card" href="crop-calendar.html">
          <span class="teaser-card__img"><img src="assets/avocado.jpg" alt="" loading="lazy"></span>
          <div class="teaser-card__body"><h3 data-i18n="teaserCropT">What we grow</h3><p data-i18n="teaserCropB">Strawberries, grapes, mango and a full crop calendar.</p><span class="teaser-card__link" data-i18n="teaserLink">Explore</span></div>
        </a>
        <a class="teaser-card" href="value-add.html">
          <span class="teaser-card__img teaser-card__img--pad"><img src="assets/prod-frozen.png" alt="" loading="lazy"></span>
          <div class="teaser-card__body"><h3 data-i18n="teaserValueT">Value-add range</h3><p data-i18n="teaserValueB">Honey, frozen fruit, sweet corn and jams.</p><span class="teaser-card__link" data-i18n="teaserLink">Explore</span></div>
        </a>
        <a class="teaser-card" href="about.html">
          <span class="teaser-card__img"><img src="assets/founder.jpg" alt="" loading="lazy"></span>
          <div class="teaser-card__body"><h3 data-i18n="teaserAboutT">Our story</h3><p data-i18n="teaserAboutB">Three generations, one family, since 1974.</p><span class="teaser-card__link" data-i18n="teaserLink">Explore</span></div>
        </a>
      </div>
    </section>'''

HERITAGE = '''
    <section class="heritage" id="heritage">
      <div class="heritage__media">
        <img src="assets/founder.jpg" alt="Dr. Kamel Tawfik Diab, founder of PICO Modern Agriculture" loading="lazy" />
        <div class="heritage__badge"><strong>1974</strong><span data-i18n="heritageBadge">The seed of our foundation</span></div>
      </div>
      <div class="heritage__copy">
        <span class="eyebrow" data-i18n="heritageEyebrow">Our heritage</span>
        <h2 data-i18n="heritageTitle">Planted by a visionary in 1974</h2>
        <p data-i18n="heritageBody1">PICO was founded by Dr. Kamel Tawfik Diab, a pioneer who cultivated arid desert land and grew varieties that were locally unheard of but prized in the world's most premium markets.</p>
        <p data-i18n="heritageBody2">He built Egypt's first tissue-culture labs, connected the country to global breeders, and introduced the seedless grape that now makes up three quarters of Egypt's grape exports. Three generations on, the same family still runs the farms.</p>
        <div class="heritage__marks">
          <div><strong data-i18n="heritageMark1Val">1st</strong><span data-i18n="heritageMark1">tissue-culture labs in Egypt</span></div>
          <div><strong data-i18n="heritageMark2Val">4th</strong><span data-i18n="heritageMark2">largest strawberry producer, worldwide</span></div>
        </div>
      </div>
    </section>'''

VALUES = '''
    <section class="values">
      <div class="section-head section-head--center"><h2 data-i18n="valuesT">What sets us apart</h2></div>
      <div class="values__grid">
        <div class="value"><span class="value__ico"><i class="ph ph-target"></i></span><h3 data-i18n="val1T">Market-driven</h3><p data-i18n="val1B">Strategy shaped by what the world's best retailers ask for.</p></div>
        <div class="value"><span class="value__ico"><i class="ph ph-leaf"></i></span><h3 data-i18n="val2T">Sustainable</h3><p data-i18n="val2B">Modern, responsible practices from soil to pack.</p></div>
        <div class="value"><span class="value__ico"><i class="ph ph-flask"></i></span><h3 data-i18n="val3T">Varietal development</h3><p data-i18n="val3B">First-movers on new crops, varieties and techniques.</p></div>
        <div class="value"><span class="value__ico"><i class="ph ph-path"></i></span><h3 data-i18n="val4T">Full traceability</h3><p data-i18n="val4B">Every pallet traced back to the block it grew in.</p></div>
      </div>
    </section>'''

def feature(img, tkey, bkey, flip=False):
    cls = "feature feature--flip" if flip else "feature"
    return f'''
    <section class="{cls}">
      <div class="feature__media"><img src="assets/{img}" alt="" loading="lazy"></div>
      <div class="feature__copy">
        <h2 data-i18n="{tkey}">Title</h2>
        <p data-i18n="{bkey}">Body</p>
      </div>
    </section>'''

GROW = '''
    <section class="grow" id="grow">
      <div class="section-head"><h2 data-i18n="growTitle">A basket built over decades</h2><p data-i18n="growSub">Pick a fruit and turn it over in your hands. Every variety below is grown, packed and shipped by PICO.</p></div>
      <div class="grow__layout">
        <div class="grow__stage">
          <canvas id="fruitCanvas" role="img" aria-label="Interactive 3D fruit you can rotate"></canvas>
          <div class="grow__tabs" role="tablist" aria-label="Choose a fruit">
            <button class="fruit-tab is-active" role="tab" data-fruit="strawberry" aria-selected="true"><span class="fruit-tab__dot" style="--c:#e23c56"></span><span data-i18n="fruitStrawberry">Strawberry</span></button>
            <button class="fruit-tab" role="tab" data-fruit="mango" aria-selected="false"><span class="fruit-tab__dot" style="--c:#f5952a"></span><span data-i18n="fruitMango">Mango</span></button>
            <button class="fruit-tab" role="tab" data-fruit="orange" aria-selected="false"><span class="fruit-tab__dot" style="--c:#ff7a1a"></span><span data-i18n="fruitOrange">Citrus</span></button>
          </div>
        </div>
        <div class="grow__detail">
          <div class="fruit-card" data-panel="strawberry"><h3 data-i18n="strawberryName">Strawberries</h3><p class="fruit-card__tag" data-i18n="strawberryTag">The flagship crop</p><p data-i18n="strawberryBody">Egypt is the world's 4th largest strawberry producer.</p><ul class="fruit-card__meta"><li><span data-i18n="labelSeason">Season</span><strong data-i18n="strawberrySeason">Nov – Apr</strong></li><li><span data-i18n="labelShips">Ships to</span><strong data-i18n="strawberryShips">Worldwide</strong></li></ul></div>
          <div class="fruit-card" data-panel="mango" hidden><h3 data-i18n="mangoName">Mango</h3><p class="fruit-card__tag" data-i18n="mangoTag">Late-summer stone fruit</p><p data-i18n="mangoBody">Sun-ripened Egyptian mango.</p><ul class="fruit-card__meta"><li><span data-i18n="labelSeason">Season</span><strong data-i18n="mangoSeason">Aug – Nov</strong></li><li><span data-i18n="labelShips">Ships to</span><strong data-i18n="mangoShips">Fresh &amp; frozen</strong></li></ul></div>
          <div class="fruit-card" data-panel="orange" hidden><h3 data-i18n="orangeName">Citrus</h3><p class="fruit-card__tag" data-i18n="orangeTag">Where it all began</p><p data-i18n="orangeBody">Bright, juice-heavy Egyptian citrus.</p><ul class="fruit-card__meta"><li><span data-i18n="labelSeason">Season</span><strong data-i18n="orangeSeason">Dec – Mar</strong></li><li><span data-i18n="labelShips">Ships to</span><strong data-i18n="orangeShips">Worldwide</strong></li></ul></div>
        </div>
      </div>
      <div class="grow__more">
        <span data-i18n="growMoreLabel">The full crop calendar</span>
        <div class="pill-row">
          <span class="pill" data-i18n="cropGrapes">Seedless grapes</span><span class="pill" data-i18n="cropAvocado">Avocado</span><span class="pill" data-i18n="cropMangoP">Mango</span><span class="pill" data-i18n="cropStone">Peaches &amp; nectarines</span><span class="pill" data-i18n="cropBlue">Blueberry</span><span class="pill" data-i18n="cropBlack">Blackberry</span><span class="pill" data-i18n="cropRasp">Raspberry</span><span class="pill" data-i18n="cropBanana">Banana</span><span class="pill" data-i18n="cropDates">Barhi dates</span><span class="pill" data-i18n="cropLoquat">Loquat</span><span class="pill" data-i18n="cropLychee">Lychee</span><span class="pill" data-i18n="cropCorn">Sweet corn</span>
        </div>
      </div>
    </section>'''

RANGE = '''
    <section class="range" id="range">
      <div class="section-head section-head--center"><h2 data-i18n="rangeTitle">Beyond the fresh harvest</h2><p data-i18n="rangeSub">The same fruit, carried further — frozen at its peak, jarred, and packed ready to eat.</p></div>
      <div class="range__grid">
        <article class="range-card range-card--honey"><span class="range-card__img"><img src="assets/prod-honey.png" alt="" loading="lazy" onerror="this.style.display='none'"><i class="ph ph-drop"></i></span><h3 data-i18n="rangeHoney">Specialty honey</h3><p data-i18n="rangeHoneyB">Eight single-blossom honeys — from citrus and clover to Egyptian mountain and black seed.</p></article>
        <article class="range-card range-card--frozen"><span class="range-card__img"><img src="assets/prod-frozen.png" alt="" loading="lazy" onerror="this.style.display='none'"><i class="ph ph-snowflake"></i></span><h3 data-i18n="rangeFrozen">Frozen fruit</h3><p data-i18n="rangeFrozenB">Mango, strawberry, blueberry and blackberry, flash-frozen to lock in the harvest.</p></article>
        <article class="range-card range-card--corn"><span class="range-card__img"><img src="assets/prod-corn.png" alt="" loading="lazy" onerror="this.style.display='none'"><i class="ph ph-plant"></i></span><h3 data-i18n="rangeCorn">Super sweet corn</h3><p data-i18n="rangeCornB">On the cob or sliced, ready to eat — plus frozen corn and avocado purées.</p></article>
        <article class="range-card range-card--jam"><span class="range-card__img"><img src="assets/prod-jam.png" alt="" loading="lazy" onerror="this.style.display='none'"><i class="ph ph-cookie"></i></span><h3 data-i18n="rangeJam">Honey-based jams</h3><p data-i18n="rangeJamB">Blueberry, strawberry, blackberry and mixed berry, sweetened with our own honey.</p></article>
      </div>
    </section>'''

BRANDS = '''
    <section class="brands" id="brands">
      <div class="section-head section-head--center"><h2 data-i18n="brandsTitle">One harvest, three labels</h2><p data-i18n="brandsSub">Whatever the market, there's a PICO line built to the same standard.</p></div>
      <div class="brands__grid">
        <article class="brand-card brand-card--signature"><span class="brand-card__tag" data-i18n="brandSigTag">Handpicked Perfection</span><h3>Pico Signature</h3><p data-i18n="brandSigB">Our premium line — the best of each block, selected for the world's top shelves.</p></article>
        <article class="brand-card brand-card--family"><span class="brand-card__tag" data-i18n="brandFamTag">Guaranteed Goodness</span><h3>Pico Family</h3><p data-i18n="brandFamB">Everyday quality for every table, grown and packed to the same PICO promise.</p></article>
        <article class="brand-card brand-card--elena"><span class="brand-card__tag" data-i18n="brandElenaTag">International standard</span><h3>Elena</h3><p data-i18n="brandElenaB">An alternative line meeting the same quality and export certifications.</p></article>
      </div>
    </section>'''

STANDARDS = '''
    <section class="standards" id="standards">
      <div class="section-head section-head--center"><h2 data-i18n="standardsTitle">Held to the standards buyers trust</h2><p data-i18n="standardsSub">Our farms and packing houses are audited to the certifications top European and UK supermarkets require.</p></div>
      <div class="cert-grid">
        <div class="cert"><span class="cert__code">GlobalG.A.P.</span><span class="cert__desc" data-i18n="certGap">GRASP good practice</span></div>
        <div class="cert"><span class="cert__code">BRC</span><span class="cert__desc" data-i18n="certBrc">Global food safety</span></div>
        <div class="cert"><span class="cert__code">ISO 9001</span><span class="cert__desc" data-i18n="certIso">Quality management</span></div>
        <div class="cert"><span class="cert__code">SEDEX · ETI</span><span class="cert__desc" data-i18n="certEti">Ethical trade</span></div>
        <div class="cert"><span class="cert__code">LEAF Marque</span><span class="cert__desc" data-i18n="certLeaf">Sustainable farming</span></div>
        <div class="cert"><span class="cert__code">Select Farm</span><span class="cert__desc" data-i18n="certSelect">Assured provenance</span></div>
      </div>
    </section>'''

F2F = '''
    <section class="f2f" id="process">
      <div class="section-head section-head--center"><h2 data-i18n="f2fTitle">From field to fork in hours, not days</h2><p data-i18n="f2fSub">Every pallet traces back to the block it grew in. This is the journey from our soil to your shelf.</p></div>
      <div class="f2f__track">
        <article class="f2f__step"><span class="f2f__ico"><i class="ph ph-plant" aria-hidden="true"></i></span><h3 data-i18n="f2fStep1">Picked at dawn</h3><p data-i18n="f2fStep1b">Harvested by hand at peak ripeness, while the field is still cool.</p></article>
        <article class="f2f__step"><span class="f2f__ico"><i class="ph ph-snowflake" aria-hidden="true"></i></span><h3 data-i18n="f2fStep2">Cooled within the hour</h3><p data-i18n="f2fStep2b">Straight into the cold chain to lock in freshness and shelf life.</p></article>
        <article class="f2f__step"><span class="f2f__ico"><i class="ph ph-package" aria-hidden="true"></i></span><h3 data-i18n="f2fStep3">Graded &amp; packed</h3><p data-i18n="f2fStep3b">Sorted to retailer spec in BRC-certified packing houses, fully traceable.</p></article>
        <article class="f2f__step"><span class="f2f__ico"><i class="ph ph-boat" aria-hidden="true"></i></span><h3 data-i18n="f2fStep4">On its way</h3><p data-i18n="f2fStep4b">Sea and air freight to premium markets around the world.</p></article>
      </div>
    </section>'''

REACH = '''
    <section class="reach" id="reach">
      <div class="reach__head">
        <div class="reach__copy"><span class="eyebrow" data-i18n="reachEyebrow">Global reach</span><h2 data-i18n="reachTitle">Trusted in premium markets worldwide</h2><p data-i18n="reachBody">From Egypt's fields to the world's most demanding retailers — cooled, graded and on its way within hours of picking.</p></div>
        <div class="reach__map" aria-hidden="true">
          <svg viewBox="0 0 600 400" class="routes" role="presentation"><defs><radialGradient id="hub" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="var(--brand)"/><stop offset="100%" stop-color="var(--brand-600)"/></radialGradient></defs><g class="routes__lines"></g><g class="routes__nodes"></g></svg>
        </div>
      </div>
      <ul class="reach__list">
        <li><strong>UK</strong><span data-i18n="reachUk">Supermarket programmes</span></li>
        <li><strong data-i18n="reachEuVal">Continental Europe</strong><span data-i18n="reachEu">Year-round supply</span></li>
        <li><strong data-i18n="reachFeVal">Far East</strong><span data-i18n="reachFe">Airfreight premium</span></li>
        <li><strong data-i18n="reachRuVal">Russia</strong><span data-i18n="reachRu">Winter citrus</span></li>
        <li><strong data-i18n="reachSaVal">South Africa</strong><span data-i18n="reachSa">Counter-season</span></li>
        <li><strong data-i18n="reachGulfVal">Gulf</strong><span data-i18n="reachGulf">Regional retail</span></li>
      </ul>
    </section>'''

CONTACT = '''
    <section class="contact" id="contact">
      <div class="contact__panel">
        <div class="contact__intro">
          <h2 data-i18n="contactTitle">Let's talk supply</h2>
          <p data-i18n="contactSub">Buyers, importers and retail partners — tell us what you need and our commercial team will get back to you.</p>
          <div class="contact__meta">
            <div><span data-i18n="contactPhoneLabel">Phone</span><strong><a href="tel:+20233377266">(+202) 3337-7266</a></strong></div>
            <div><span data-i18n="contactEmailLabel">Email</span><strong><a href="mailto:info@pico-agriculture.com">info@pico-agriculture.com</a></strong></div>
            <div class="contact__meta--wide"><span data-i18n="contactLocLabel">Head office</span><strong data-i18n="contactLoc">8 Geziret Al Arab St, Infinity Tower, Mohandessin, Giza, Egypt</strong></div>
          </div>
          <div class="contact__social">
            <a href="https://facebook.com/PicoEg" target="_blank" rel="noopener" aria-label="Facebook"><i class="ph ph-facebook-logo"></i></a>
            <a href="https://instagram.com/pico.eg" target="_blank" rel="noopener" aria-label="Instagram"><i class="ph ph-instagram-logo"></i></a>
            <a href="https://www.linkedin.com/company/pico-modern-agriculture-company" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="ph ph-linkedin-logo"></i></a>
          </div>
        </div>
        <form class="contact__form" id="contactForm" novalidate>
          <div class="field"><label for="cName" data-i18n="formName">Your name</label><input id="cName" name="name" type="text" autocomplete="name" required /><p class="field__error" data-i18n="formErrName">Please enter your name.</p></div>
          <div class="field"><label for="cEmail" data-i18n="formEmail">Work email</label><input id="cEmail" name="email" type="email" autocomplete="email" required /><p class="field__error" data-i18n="formErrEmail">Please enter a valid email.</p></div>
          <div class="field"><label for="cMsg" data-i18n="formMsg">What are you sourcing?</label><textarea id="cMsg" name="message" rows="3"></textarea></div>
          <button type="submit" class="btn btn--full" id="formSubmit" data-i18n="formSend">Send enquiry</button>
          <p class="form-note" id="formNote" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>'''

def page(fname, active, title, desc, main, three=False):
    html = (head(title, desc) + nav(active) +
            '\n  <main id="main">\n    <span id="top"></span>\n' + main +
            '\n  </main>\n' + FOOTER + scripts(three))
    with open(fname, "w") as f:
        f.write(html)
    print("wrote", fname)

PAGES = [
    ("index.html", "home", "PICO Modern Agriculture — As fresh as it gets",
     "Family-grown Egyptian fruit since 1974. Premium fresh produce, honey, frozen fruit and more.",
     PHONE_HERO + TRUST + STATS + HOME_TEASER + CTA_BAND, False),
    ("about.html", "about", "About — PICO Modern Agriculture",
     "A family-owned, third-generation Egyptian grower and exporter since 1974.",
     page_hero("phAboutT","phAboutS") + HERITAGE + VALUES +
     feature("workers.jpg","aboutPeopleT","aboutPeopleB", flip=True) + CTA_BAND, False),
    ("crop-calendar.html", "crop", "Crop Calendar — PICO Modern Agriculture",
     "PICO's year-round basket of premium fruit, viewable in interactive 3D.",
     page_hero("phCropT","phCropS") + GROW +
     feature("avocado.jpg","cropFeatureT","cropFeatureB") + CTA_BAND, True),
    ("value-add.html", "value", "Value-Add Products — PICO Modern Agriculture",
     "PICO honey, frozen fruit, sweet corn, jams and the Signature, Family and Elena brands.",
     page_hero("phValueT","phValueS") + RANGE + BRANDS + CTA_BAND, False),
    ("standards.html", "std", "Standards & Reach — PICO Modern Agriculture",
     "Audited to GlobalG.A.P., BRC, ISO 9001 and more, shipped to premium markets worldwide.",
     page_hero("phStdT","phStdS") + STANDARDS + F2F + REACH, False),
    ("contact.html", "contact", "Contact — PICO Modern Agriculture",
     "Talk supply with PICO Modern Agriculture, Mohandessin, Giza, Egypt.",
     page_hero("phContactT","phContactS") + CONTACT, False),
]

if __name__ == "__main__":
    for args in PAGES:
        page(*args)
    print("done")
