import streamlit as st
from groq import Groq
import datetime
import math
import random
import json
from typing import Optional

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COSMOS · AI Horoscope",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PREMIUM CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Space+Mono:wght@400;700&display=swap');

:root {
    --ink: #0a0612;
    --parchment: #f5f0e8;
    --gold: #c9a84c;
    --gold-light: #e8d5a3;
    --gold-pale: #fdf8ee;
    --violet: #3d1a6e;
    --violet-mid: #6b35b0;
    --violet-soft: #b09ad4;
    --rose: #c0465a;
    --teal: #2a8a8a;
    --star: #ffe566;
    --mist: rgba(201,168,76,0.08);
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #07030f !important;
    color: var(--parchment) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(61,26,110,0.55) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(42,138,138,0.25) 0%, transparent 55%),
        radial-gradient(ellipse 100% 80% at 50% 50%, rgba(10,6,18,1) 40%, #07030f 100%)
    !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ── STARFIELD ── */
.starfield {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.star-dot {
    position: absolute; border-radius: 50%;
    background: white; animation: twinkle var(--dur) ease-in-out infinite;
    animation-delay: var(--delay);
}
@keyframes twinkle {
    0%,100% { opacity: 0.15; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.4); }
}

/* ── HEADER ── */
.cosmos-header {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.cosmos-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
    opacity: 0.8;
}
.cosmos-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 900;
    font-style: italic;
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 40%, #fff8e6 70%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    letter-spacing: -0.02em;
    margin: 0;
}
.cosmos-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-style: italic;
    color: var(--violet-soft);
    margin-top: 0.75rem;
    letter-spacing: 0.05em;
}
.divider-ornament {
    display: flex; align-items: center; gap: 1rem;
    justify-content: center; margin: 1.5rem 0;
}
.divider-ornament .line { height: 1px; width: 80px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.divider-ornament .gem { color: var(--gold); font-size: 1rem; }

/* ── CARDS ── */
.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(61,26,110,0.12) 100%);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

/* ── SIGN GRID ── */
.sign-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1rem 0;
}
.sign-btn {
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(61,26,110,0.15));
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 14px;
    padding: 0.85rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Cormorant Garamond', serif;
}
.sign-btn:hover, .sign-btn.active {
    background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(107,53,176,0.2));
    border-color: var(--gold);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(201,168,76,0.15);
}
.sign-btn .glyph { font-size: 1.8rem; display: block; }
.sign-btn .name { font-size: 0.75rem; letter-spacing: 0.1em; color: var(--gold-light); text-transform: uppercase; }
.sign-btn .dates { font-size: 0.6rem; color: var(--violet-soft); font-family: 'Space Mono', monospace; }

/* ── DOMAIN TILES ── */
.domain-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
    margin: 1rem 0;
}
.domain-tile {
    padding: 0.7rem 1rem;
    border-radius: 10px;
    border: 1px solid rgba(201,168,76,0.1);
    background: rgba(255,255,255,0.03);
    text-align: center;
    cursor: pointer;
    transition: all 0.25s;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.05em;
    color: var(--violet-soft);
    text-transform: uppercase;
}
.domain-tile:hover, .domain-tile.active {
    border-color: var(--violet-mid);
    background: rgba(107,53,176,0.15);
    color: var(--parchment);
}
.domain-tile .icon { display: block; font-size: 1.3rem; margin-bottom: 0.3rem; }

/* ── READING OUTPUT ── */
.reading-container {
    background: linear-gradient(160deg, rgba(7,3,15,0.95) 0%, rgba(30,10,60,0.6) 100%);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 24px;
    padding: 2.5rem;
    position: relative;
    margin-top: 1.5rem;
}
.reading-container::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.reading-sign-badge {
    display: inline-flex; align-items: center; gap: 0.75rem;
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 50px;
    padding: 0.4rem 1rem;
    margin-bottom: 1.5rem;
}
.reading-sign-badge .emoji { font-size: 1.5rem; }
.reading-sign-badge .label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--gold);
    text-transform: uppercase;
}
.reading-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-style: italic;
    color: var(--gold-light);
    margin-bottom: 1rem;
}
.reading-body {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    line-height: 1.9;
    color: #e8e0d4;
}
.reading-body p { margin-bottom: 1.2rem; }

/* ── METER BARS ── */
.meter-row {
    display: flex; align-items: center; gap: 1rem; margin: 0.6rem 0;
}
.meter-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    color: var(--violet-soft);
    text-transform: uppercase;
    width: 90px;
    flex-shrink: 0;
}
.meter-track {
    flex: 1;
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    overflow: hidden;
}
.meter-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--violet-mid), var(--gold));
    transition: width 1.5s ease;
}
.meter-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold);
    width: 30px;
    text-align: right;
}

/* ── LUCKY STRIP ── */
.lucky-strip {
    display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;
}
.lucky-pill {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 50px;
    padding: 0.35rem 0.9rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: var(--gold-light);
    text-transform: uppercase;
    display: flex; align-items: center; gap: 0.4rem;
}

/* ── PLANET TABLE ── */
.planet-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-family: 'Cormorant Garamond', serif;
}
.planet-row:last-child { border-bottom: none; }
.planet-name { display: flex; align-items: center; gap: 0.6rem; font-size: 0.95rem; color: var(--parchment); }
.planet-glyph { font-size: 1.2rem; }
.planet-sign { font-size: 0.8rem; color: var(--violet-soft); font-style: italic; }
.planet-influence { font-size: 0.75rem; font-family: 'Space Mono', monospace; }
.planet-pos { color: var(--gold); }
.planet-neg { color: var(--rose); }
.planet-neu { color: var(--teal); }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--violet) 0%, var(--violet-mid) 100%) !important;
    color: var(--gold-light) !important;
    border: 1px solid rgba(201,168,76,0.35) !important;
    border-radius: 50px !important;
    padding: 0.6rem 2.5rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(61,26,110,0.4) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(201,168,76,0.2) !important;
}

div[data-testid="stSelectbox"] select,
div[data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    color: var(--parchment) !important;
    border-radius: 10px !important;
}

label { color: var(--violet-soft) !important; font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }

div[data-testid="stSpinner"] { color: var(--gold) !important; }

.stAlert { background: rgba(201,168,76,0.08) !important; border: 1px solid rgba(201,168,76,0.2) !important; border-radius: 12px !important; }

/* Tabs */
div[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.1em !important;
    color: var(--violet-soft) !important;
    text-transform: uppercase !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--violet-mid); border-radius: 99px; }

.section-heading {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
    opacity: 0.8;
    display: flex; align-items: center; gap: 0.75rem;
}
.section-heading::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(201,168,76,0.3), transparent);
}

.insight-box {
    border-left: 2px solid var(--gold);
    padding: 0.75rem 1rem;
    background: rgba(201,168,76,0.05);
    border-radius: 0 10px 10px 0;
    margin: 1rem 0;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    color: var(--gold-light);
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── STARFIELD JS ────────────────────────────────────────────────────────────
st.markdown("""
<div class="starfield" id="sf"></div>
<script>
(function(){
  var sf = document.getElementById('sf');
  if(!sf) return;
  for(var i=0;i<160;i++){
    var d = document.createElement('div');
    var sz = Math.random()*2.5+0.5;
    d.className='star-dot';
    d.style.cssText=`left:${Math.random()*100}%;top:${Math.random()*100}%;width:${sz}px;height:${sz}px;opacity:${Math.random()*0.6+0.1};--dur:${(Math.random()*4+2).toFixed(1)}s;--delay:${(Math.random()*5).toFixed(1)}s;`;
    sf.appendChild(d);
  }
})();
</script>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
SIGNS = [
    {"name":"Aries","glyph":"♈","emoji":"🔥","dates":"Mar 21–Apr 19","element":"Fire","ruler":"Mars","quality":"Cardinal","stone":"Diamond","color":"Crimson"},
    {"name":"Taurus","glyph":"♉","emoji":"🌿","dates":"Apr 20–May 20","element":"Earth","ruler":"Venus","quality":"Fixed","stone":"Emerald","color":"Green"},
    {"name":"Gemini","glyph":"♊","emoji":"🌬","dates":"May 21–Jun 20","element":"Air","ruler":"Mercury","quality":"Mutable","stone":"Agate","color":"Yellow"},
    {"name":"Cancer","glyph":"♋","emoji":"🌊","dates":"Jun 21–Jul 22","element":"Water","ruler":"Moon","quality":"Cardinal","stone":"Pearl","color":"Silver"},
    {"name":"Leo","glyph":"♌","emoji":"☀️","dates":"Jul 23–Aug 22","element":"Fire","ruler":"Sun","quality":"Fixed","stone":"Ruby","color":"Gold"},
    {"name":"Virgo","glyph":"♍","emoji":"🌾","dates":"Aug 23–Sep 22","element":"Earth","ruler":"Mercury","quality":"Mutable","stone":"Sapphire","color":"Navy"},
    {"name":"Libra","glyph":"♎","emoji":"⚖️","dates":"Sep 23–Oct 22","element":"Air","ruler":"Venus","quality":"Cardinal","stone":"Opal","color":"Pink"},
    {"name":"Scorpio","glyph":"♏","emoji":"🦂","dates":"Oct 23–Nov 21","element":"Water","ruler":"Pluto","quality":"Fixed","stone":"Topaz","color":"Burgundy"},
    {"name":"Sagittarius","glyph":"♐","emoji":"🏹","dates":"Nov 22–Dec 21","element":"Fire","ruler":"Jupiter","quality":"Mutable","stone":"Turquoise","color":"Purple"},
    {"name":"Capricorn","glyph":"♑","emoji":"🏔","dates":"Dec 22–Jan 19","element":"Earth","ruler":"Saturn","quality":"Cardinal","stone":"Garnet","color":"Brown"},
    {"name":"Aquarius","glyph":"♒","emoji":"⚡","dates":"Jan 20–Feb 18","element":"Air","ruler":"Uranus","quality":"Fixed","stone":"Amethyst","color":"Electric Blue"},
    {"name":"Pisces","glyph":"♓","emoji":"🐟","dates":"Feb 19–Mar 20","element":"Water","ruler":"Neptune","quality":"Mutable","stone":"Aquamarine","color":"Sea Green"},
]

DOMAINS = [
    {"id":"daily","icon":"☀️","label":"Daily"},
    {"id":"love","icon":"♥️","label":"Love"},
    {"id":"career","icon":"💼","label":"Career"},
    {"id":"wealth","icon":"💰","label":"Wealth"},
    {"id":"health","icon":"🌿","label":"Health"},
    {"id":"spiritual","icon":"🔮","label":"Spirit"},
]

PLANETS = [
    {"name":"Sun","glyph":"☉","sign":"Leo","influence":"pos"},
    {"name":"Moon","glyph":"☽","sign":"Pisces","influence":"neu"},
    {"name":"Mercury","glyph":"☿","sign":"Virgo","influence":"pos"},
    {"name":"Venus","glyph":"♀","sign":"Libra","influence":"pos"},
    {"name":"Mars","glyph":"♂","sign":"Aries","influence":"neg"},
    {"name":"Jupiter","glyph":"♃","sign":"Sagittarius","influence":"pos"},
    {"name":"Saturn","glyph":"♄","sign":"Capricorn","influence":"neg"},
    {"name":"Uranus","glyph":"♅","sign":"Aquarius","influence":"neu"},
    {"name":"Neptune","glyph":"♆","sign":"Pisces","influence":"neu"},
    {"name":"Pluto","glyph":"♇","sign":"Scorpio","influence":"neg"},
]

# ─── ML: Numerology + Planetary Score Engine ────────────────────────────────
def compute_life_path(dob: datetime.date) -> int:
    s = sum(int(d) for d in str(dob).replace("-",""))
    while s > 9 and s not in (11,22,33):
        s = sum(int(d) for d in str(s))
    return s

def get_chinese_sign(year: int) -> str:
    animals = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Goat","Monkey","Rooster","Dog","Pig"]
    return animals[(year - 1900) % 12]

def planetary_influence_score(sign: dict, dob: datetime.date, domain: str) -> dict:
    """Simulated ML scoring — deterministic via seed from birth data."""
    seed = hash(f"{sign['name']}{dob}{domain}") & 0xFFFF
    rng = random.Random(seed)
    
    element_boosts = {"Fire":{"career":10,"health":-5,"love":5},"Earth":{"wealth":12,"health":8,"career":5},
                      "Air":{"love":10,"spiritual":8,"daily":5},"Water":{"love":12,"spiritual":15,"health":5}}
    
    base = {k: rng.randint(40,75) for k in ["love","career","wealth","health","spiritual","daily"]}
    boosts = element_boosts.get(sign["element"], {})
    for k,v in boosts.items():
        base[k] = min(99, base[k] + v)
    
    lucky_numbers = sorted(rng.sample(range(1,50), 5))
    lucky_colors = rng.sample(["Violet","Gold","Teal","Rose","Amber","Sage","Crimson","Azure","Pearl"], 3)
    lucky_days = rng.sample(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], 3)
    
    life_path = compute_life_path(dob)
    chinese = get_chinese_sign(dob.year)
    
    return {
        "scores": base,
        "lucky_numbers": lucky_numbers,
        "lucky_colors": lucky_colors,
        "lucky_days": lucky_days,
        "life_path": life_path,
        "chinese": chinese,
        "compatibility": rng.sample([s["name"] for s in SIGNS if s["name"] != sign["name"]], 3),
        "challenge_sign": rng.choice([s["name"] for s in SIGNS if s["name"] != sign["name"]]),
    }

# ─── GROQ API ────────────────────────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"   # fast, free, high quality

def generate_horoscope(sign: dict, dob: datetime.date, domain: str, ml: dict, moon_phase: str, api_key: str = "") -> str:
    client = Groq(api_key=api_key)
    today = datetime.date.today().strftime("%B %d, %Y")
    domain_context = {
        "daily":    "a comprehensive daily reading covering all life areas with vivid cosmic imagery",
        "love":     "love, relationships, romance, soul connections, and heart matters",
        "career":   "career, ambition, professional growth, workplace dynamics, and destiny",
        "wealth":   "financial abundance, material prosperity, investment wisdom, and manifestation",
        "health":   "physical vitality, mental wellness, energetic body, and healing paths",
        "spiritual":"spiritual awakening, inner wisdom, metaphysical insights, and cosmic consciousness",
    }
    prompt = f"""You are COSMOS, the world's most gifted astrologer — part mystic oracle, part depth psychologist, part cosmic poet. You blend Hellenistic astrology, Vedic principles, Jungian archetypes, and modern psychological insight.

Today: {today}
Moon Phase: {moon_phase}

Client Profile:
- Sun Sign: {sign['name']} ({sign['glyph']}) — {sign['element']} element, {sign['quality']} modality
- Ruling Planet: {sign['ruler']}
- Date of Birth: {dob.strftime('%B %d, %Y')}
- Life Path Number: {ml['life_path']} (Numerology)
- Chinese Zodiac: Year of the {ml['chinese']}
- Domain Requested: {domain.upper()} — {domain_context.get(domain, domain)}
- Lucky Numbers: {', '.join(map(str, ml['lucky_numbers']))}
- Lucky Colors: {', '.join(ml['lucky_colors'])}
- Compatible Signs: {', '.join(ml['compatibility'][:2])}
- Challenge Sign: {ml['challenge_sign']}

Write a deeply personal, profoundly insightful horoscope for {domain} in exactly 4 rich paragraphs. Each paragraph should:
1. Open with a cosmic observation (planetary position, celestial event, or archetypal energy)
2. Connect it meaningfully to the person's specific {domain} situation
3. Offer a concrete, actionable insight or guidance
4. End with a poetic, memorable image or metaphor

Tone: Mystical yet grounded, poetic yet practical. No generic platitudes. Every sentence should feel like it was written specifically for this person born under {sign['name']} on {dob.strftime('%B %d, %Y')}.

Do not use bullet points. Write in flowing, lyrical prose. Each paragraph should be 4-6 sentences. Begin immediately with the reading — no introduction like "Here is your reading"."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.9,
    )
    return response.choices[0].message.content

def generate_affirmation(sign: dict, domain: str, api_key: str = "") -> str:
    client = Groq(api_key=api_key)
    prompt = f"Write ONE powerful, poetic affirmation (max 20 words) for {sign['name']} focused on {domain}. No quotes, just the affirmation text. Make it mystical and empowering."
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.85,
    )
    return response.choices[0].message.content.strip()

# ─── MOON PHASE ──────────────────────────────────────────────────────────────
def get_moon_phase(date: datetime.date) -> tuple[str, str]:
    known_new = datetime.date(2024, 1, 11)
    diff = (date - known_new).days
    cycle = diff % 29.53
    if cycle < 1.85: return "🌑", "New Moon"
    elif cycle < 7.38: return "🌒", "Waxing Crescent"
    elif cycle < 9.22: return "🌓", "First Quarter"
    elif cycle < 14.77: return "🌔", "Waxing Gibbous"
    elif cycle < 16.61: return "🌕", "Full Moon"
    elif cycle < 22.15: return "🌖", "Waning Gibbous"
    elif cycle < 23.99: return "🌗", "Last Quarter"
    else: return "🌘", "Waning Crescent"

# ─── API KEY SIDEBAR ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✦ COSMOS")
    st.markdown("---")
    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your FREE key at console.groq.com"
    )
    if api_key:
        st.success("✓ Groq Key loaded")
    else:
        st.info("Paste your **Groq API key** above.\n\n🆓 Completely FREE at:\nconsole.groq.com\n\nNo credit card needed.")
    st.markdown("---")
    st.markdown("**⚡ Powered by**")
    st.markdown("• Groq LPU · llama-3.3-70b\n• ML Planetary Engine\n• Numerology Algorithm\n• Moon Phase Calculator")
    st.markdown("---")
    st.markdown("**📖 Quick Guide**")
    st.markdown("1. Enter your birth date\n2. Pick a zodiac sign\n3. Choose a reading domain\n4. Click Reveal My Destiny")

# ─── INIT STATE ──────────────────────────────────────────────────────────────
if "selected_sign" not in st.session_state: st.session_state.selected_sign = None
if "selected_domain" not in st.session_state: st.session_state.selected_domain = "daily"
if "reading" not in st.session_state: st.session_state.reading = None
if "ml_data" not in st.session_state: st.session_state.ml_data = None
if "affirmation" not in st.session_state: st.session_state.affirmation = None
if "dob" not in st.session_state: st.session_state.dob = datetime.date(1990,1,1)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cosmos-header">
    <div class="cosmos-eyebrow">✦ Celestial Intelligence · Est. Since Time Immemorial ✦</div>
    <h1 class="cosmos-title">COSMOS</h1>
    <p class="cosmos-subtitle">AI-Powered Celestial Readings · Planetary Intelligence · Soul Mapping</p>
    <div class="divider-ornament">
        <div class="line"></div><div class="gem">✦</div><div class="line"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MOON PHASE BANNER ───────────────────────────────────────────────────────
moon_icon, moon_name = get_moon_phase(datetime.date.today())
today_str = datetime.date.today().strftime("%A, %B %d %Y")
st.markdown(f"""
<div style="text-align:center;margin-bottom:2rem;">
    <span style="font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.25em;color:var(--violet-soft);text-transform:uppercase;">
        {today_str} &nbsp;·&nbsp; {moon_icon} {moon_name} &nbsp;·&nbsp; Tropical Zodiac Active
    </span>
</div>
""", unsafe_allow_html=True)

# ─── MAIN LAYOUT ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    # BIRTH INFO
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Birth Details</div>', unsafe_allow_html=True)
    
    dob = st.date_input(
        "Date of Birth",
        value=st.session_state.dob,
        min_value=datetime.date(1920,1,1),
        max_value=datetime.date.today(),
        key="dob_input"
    )
    st.session_state.dob = dob
    
    # Auto-detect sign from DOB
    def sign_from_dob(d: datetime.date) -> dict:
        m, day = d.month, d.day
        if (m==3 and day>=21) or (m==4 and day<=19): return SIGNS[0]
        if (m==4 and day>=20) or (m==5 and day<=20): return SIGNS[1]
        if (m==5 and day>=21) or (m==6 and day<=20): return SIGNS[2]
        if (m==6 and day>=21) or (m==7 and day<=22): return SIGNS[3]
        if (m==7 and day>=23) or (m==8 and day<=22): return SIGNS[4]
        if (m==8 and day>=23) or (m==9 and day<=22): return SIGNS[5]
        if (m==9 and day>=23) or (m==10 and day<=22): return SIGNS[6]
        if (m==10 and day>=23) or (m==11 and day<=21): return SIGNS[7]
        if (m==11 and day>=22) or (m==12 and day<=21): return SIGNS[8]
        if (m==12 and day>=22) or (m==1 and day<=19): return SIGNS[9]
        if (m==1 and day>=20) or (m==2 and day<=18): return SIGNS[10]
        return SIGNS[11]
    
    auto_sign = sign_from_dob(dob)
    if st.session_state.selected_sign is None:
        st.session_state.selected_sign = auto_sign
    
    st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:0.6rem;color:var(--gold);letter-spacing:0.1em;margin:0.5rem 0;">✦ Detected: {auto_sign["emoji"]} {auto_sign["name"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SIGN SELECTOR
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Choose Your Sign</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sign-grid">', unsafe_allow_html=True)
    for i, s in enumerate(SIGNS):
        active = "active" if st.session_state.selected_sign and st.session_state.selected_sign["name"] == s["name"] else ""
        st.markdown(f"""
        <div class="sign-btn {active}" onclick="
            window.parent.postMessage({{type:'streamlit:setComponentValue', key:'sign_{i}'}}, '*')
        ">
            <span class="glyph">{s['emoji']}</span>
            <span class="name">{s['name']}</span>
            <span class="dates">{s['dates']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sign buttons via Streamlit (hidden but functional)
    cols = st.columns(4)
    for i, s in enumerate(SIGNS):
        with cols[i % 4]:
            if st.button(s["glyph"], key=f"sign_sel_{i}", help=s["name"]):
                st.session_state.selected_sign = s
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # DOMAIN SELECTOR
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Reading Domain</div>', unsafe_allow_html=True)
    
    dom_cols = st.columns(3)
    for i, d in enumerate(DOMAINS):
        with dom_cols[i % 3]:
            active_style = "background:rgba(107,53,176,0.25);border-color:var(--violet-mid);" if st.session_state.selected_domain == d["id"] else ""
            if st.button(f"{d['icon']} {d['label']}", key=f"dom_{d['id']}"):
                st.session_state.selected_domain = d["id"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GENERATE BUTTON
    if st.button("✦  REVEAL MY DESTINY  ✦", key="generate_btn"):
        if not api_key:
            st.error("Please enter your Anthropic API key in the sidebar (click > at top-left).")
        else:
            sign = st.session_state.selected_sign or auto_sign
            domain = st.session_state.selected_domain
            ml_data = planetary_influence_score(sign, dob, domain)

            with st.spinner("The cosmos is aligning your reading..."):
                reading = generate_horoscope(sign, dob, domain, ml_data, moon_name, api_key=api_key)
                affirmation = generate_affirmation(sign, domain, api_key=api_key)

            st.session_state.ml_data = ml_data
            st.session_state.reading = reading
            st.session_state.affirmation = affirmation
            st.rerun()

# ─── RIGHT COLUMN: OUTPUT ────────────────────────────────────────────────────
with col_right:
    sign = st.session_state.selected_sign or auto_sign
    
    if st.session_state.reading and st.session_state.ml_data:
        ml = st.session_state.ml_data
        domain = st.session_state.selected_domain
        dom_label = next((d["label"] for d in DOMAINS if d["id"]==domain), domain)
        dom_icon = next((d["icon"] for d in DOMAINS if d["id"]==domain), "✦")
        
        tab1, tab2, tab3 = st.tabs(["📜  Reading", "🪐  Planets", "🔢  Numerology"])
        
        with tab1:
            # Affirmation
            if st.session_state.affirmation:
                st.markdown(f'<div class="insight-box">"{st.session_state.affirmation}"</div>', unsafe_allow_html=True)
            
            # Reading header
            st.markdown(f"""
            <div class="reading-container">
                <div class="reading-sign-badge">
                    <span class="emoji">{sign['emoji']}</span>
                    <span class="label">{sign['name']} · {dom_icon} {dom_label} · {moon_icon} {moon_name}</span>
                </div>
                <div class="reading-title">{sign['name']} · {dom_label} Reading</div>
                <div class="reading-body">
            """, unsafe_allow_html=True)
            
            for para in st.session_state.reading.split("\n\n"):
                if para.strip():
                    st.markdown(f"<p>{para.strip()}</p>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Domain scores meters
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Cosmic Influence Meters</div>', unsafe_allow_html=True)
            
            for dom_id, score in ml["scores"].items():
                dom_info = next((d for d in DOMAINS if d["id"]==dom_id), {"icon":"✦","label":dom_id})
                st.markdown(f"""
                <div class="meter-row">
                    <span class="meter-label">{dom_info.get('icon','')} {dom_info.get('label',dom_id)}</span>
                    <div class="meter-track"><div class="meter-fill" style="width:{score}%"></div></div>
                    <span class="meter-val">{score}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Lucky strip
            st.markdown('<div class="glass-card" style="margin-top:1rem">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Cosmic Luck Factors</div>', unsafe_allow_html=True)
            st.markdown('<div class="lucky-strip">', unsafe_allow_html=True)
            for n in ml["lucky_numbers"]:
                st.markdown(f'<span class="lucky-pill">🔢 {n}</span>', unsafe_allow_html=True)
            for c in ml["lucky_colors"]:
                st.markdown(f'<span class="lucky-pill">🎨 {c}</span>', unsafe_allow_html=True)
            for day in ml["lucky_days"]:
                st.markdown(f'<span class="lucky-pill">📅 {day}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Planetary Positions & Influences</div>', unsafe_allow_html=True)
            
            for p in PLANETS:
                cls = f"planet_{p['influence']}"
                infl_label = {"pos":"▲ Favorable","neg":"▼ Challenging","neu":"◆ Neutral"}[p["influence"]]
                st.markdown(f"""
                <div class="planet-row">
                    <div class="planet-name">
                        <span class="planet-glyph">{p['glyph']}</span>
                        <span>{p['name']}</span>
                        <span class="planet-sign">in {p['sign']}</span>
                    </div>
                    <span class="planet-influence {cls}">{infl_label}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sign profile
            st.markdown('<div class="glass-card" style="margin-top:1rem">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Sign Archetype Profile</div>', unsafe_allow_html=True)
            
            attrs = [
                ("Element", sign["element"]),
                ("Modality", sign["quality"]),
                ("Ruler", sign["ruler"]),
                ("Birthstone", sign["stone"]),
                ("Power Color", sign["color"]),
            ]
            for k, v in attrs:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                    <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:var(--violet-soft);letter-spacing:0.08em;text-transform:uppercase">{k}</span>
                    <span style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--gold-light)">{v}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Compatibility
            st.markdown(f"""
            <div style="margin-top:1rem">
                <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:var(--violet-soft);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.5rem">Cosmic Soulmates</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--gold-light)">{' · '.join(ml['compatibility'])}</div>
            </div>
            <div style="margin-top:0.75rem">
                <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:var(--rose);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.5rem">Growth Challenge</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--rose)">{ml['challenge_sign']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Numerological Blueprint</div>', unsafe_allow_html=True)
            
            lp = ml["life_path"]
            lp_meanings = {
                1:"The Pioneer — Independence, leadership, originality. You forge paths others follow.",
                2:"The Diplomat — Harmony, partnership, intuition. You bridge worlds with grace.",
                3:"The Creator — Expression, joy, creativity. Your words and art move the world.",
                4:"The Builder — Stability, discipline, foundation. You create lasting legacies.",
                5:"The Explorer — Freedom, adventure, change. You thrive in transformation.",
                6:"The Nurturer — Love, responsibility, healing. You are the heart of any circle.",
                7:"The Seeker — Wisdom, analysis, mysticism. The inner world is your true home.",
                8:"The Achiever — Power, abundance, manifestation. Material and spiritual mastery.",
                9:"The Humanitarian — Compassion, completion, universal love. You serve the collective.",
                11:"The Illuminator — Master number of spiritual insight and psychic sensitivity.",
                22:"The Master Builder — Grandest visions made real through disciplined action.",
                33:"The Master Teacher — Pure compassion and divine creative expression.",
            }
            
            st.markdown(f"""
            <div style="text-align:center;padding:2rem 0">
                <div style="font-family:'Playfair Display',serif;font-size:5rem;font-weight:900;background:linear-gradient(135deg,var(--gold-light),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1">{lp}</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:var(--gold);text-transform:uppercase;margin:0.5rem 0">Life Path Number</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;color:var(--parchment);line-height:1.7;margin-top:1rem">{lp_meanings.get(lp, "A unique vibrational frequency beyond common classification.")}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Chinese zodiac
            st.markdown(f"""
            <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:1.5rem;margin-top:0.5rem">
                <div style="font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;color:var(--violet-soft);text-transform:uppercase;margin-bottom:1rem">Chinese Zodiac</div>
                <div style="display:flex;align-items:center;gap:1rem">
                    <div style="font-size:3rem">🐉</div>
                    <div>
                        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--gold-light)">Year of the {ml['chinese']}</div>
                        <div style="font-family:'Cormorant Garamond',serif;font-size:0.9rem;color:var(--violet-soft);margin-top:0.25rem">Eastern celestial influence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # DOB breakdown
            st.markdown(f"""
            <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:1.5rem;margin-top:1rem">
                <div style="font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;color:var(--violet-soft);text-transform:uppercase;margin-bottom:0.75rem">Vibrational Breakdown</div>
            """, unsafe_allow_html=True)
            
            breakdown = {
                "Day Vibration": sum(int(d) for d in str(dob.day)),
                "Month Vibration": sum(int(d) for d in str(dob.month)),
                "Year Vibration": sum(int(d) for d in str(dob.year)),
            }
            for k, v in breakdown.items():
                while v > 9: v = sum(int(d) for d in str(v))
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                    <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:var(--violet-soft);letter-spacing:0.06em">{k}</span>
                    <span style="font-family:'Playfair Display',serif;font-size:1.1rem;color:var(--gold)">{v}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    else:
        # Welcome state
        st.markdown(f"""
        <div class="reading-container" style="text-align:center;padding:4rem 2rem">
            <div style="font-size:4rem;margin-bottom:1.5rem">{sign['emoji']}</div>
            <div style="font-family:'Playfair Display',serif;font-size:2rem;font-style:italic;color:var(--gold-light);margin-bottom:1rem">
                Welcome, {sign['name']}
            </div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--violet-soft);line-height:1.8;max-width:400px;margin:0 auto">
                The stars have been watching you. Enter your birth date, select your domain of inquiry, and let the cosmic intelligence reveal what the universe has written in your celestial blueprint.
            </div>
            <div style="margin-top:2rem;font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:var(--gold);opacity:0.6">
                {moon_icon} {moon_name} · {today_str}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sign info cards
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">All Twelve Signs</div>', unsafe_allow_html=True)
        
        row1 = st.columns(6)
        for i, s in enumerate(SIGNS[:6]):
            with row1[i]:
                st.markdown(f"""
                <div style="text-align:center;padding:0.75rem 0">
                    <div style="font-size:1.8rem">{s['emoji']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.55rem;color:var(--gold);letter-spacing:0.1em;text-transform:uppercase;margin-top:0.3rem">{s['name']}</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:0.75rem;color:var(--violet-soft)">{s['element']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        row2 = st.columns(6)
        for i, s in enumerate(SIGNS[6:]):
            with row2[i]:
                st.markdown(f"""
                <div style="text-align:center;padding:0.75rem 0">
                    <div style="font-size:1.8rem">{s['emoji']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.55rem;color:var(--gold);letter-spacing:0.1em;text-transform:uppercase;margin-top:0.3rem">{s['name']}</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:0.75rem;color:var(--violet-soft)">{s['element']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid rgba(201,168,76,0.1);margin-top:3rem">
    <div style="font-family:'Space Mono',monospace;font-size:0.55rem;letter-spacing:0.25em;color:rgba(176,154,212,0.5);text-transform:uppercase">
        ✦ &nbsp; COSMOS · AI Celestial Intelligence · Powered by Claude &amp; Astrology ML &nbsp; ✦
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:0.8rem;color:rgba(176,154,212,0.35);margin-top:0.5rem;font-style:italic">
        For entertainment and personal reflection. The cosmos speaks — you decide.
    </div>
</div>
""", unsafe_allow_html=True)
