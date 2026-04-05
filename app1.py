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
    --cyan: #38bdf8;
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

#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    padding: 2rem 3rem !important;
    max-width: 1300px !important;
    margin: 0 auto !important;
}

/* STARFIELD */
.starfield { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }
.star-dot { position: absolute; border-radius: 50%; background: white; animation: twinkle var(--dur) ease-in-out infinite; animation-delay: var(--delay); }
@keyframes twinkle { 0%,100% { opacity: 0.15; transform: scale(1); } 50% { opacity: 1; transform: scale(1.4); } }

/* HEADER */
.cosmos-header { text-align: center; padding: 2.5rem 0 1.5rem; }
.cosmos-eyebrow { font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 0.4em; color: var(--gold); text-transform: uppercase; margin-bottom: 1rem; opacity: 0.8; }
.cosmos-title { font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 7vw, 5rem); font-weight: 900; font-style: italic; background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 40%, #fff8e6 70%, var(--gold) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; letter-spacing: -0.02em; margin: 0; }
.cosmos-subtitle { font-family: 'Cormorant Garamond', serif; font-size: 1rem; font-style: italic; color: var(--violet-soft); margin-top: 0.75rem; letter-spacing: 0.05em; }
.divider-ornament { display: flex; align-items: center; gap: 1rem; justify-content: center; margin: 1rem 0; }
.divider-ornament .line { height: 1px; width: 80px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.divider-ornament .gem { color: var(--gold); font-size: 1rem; }

/* GLASS CARDS */
.glass-card { background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(61,26,110,0.12) 100%); border: 1px solid rgba(201,168,76,0.2); border-radius: 20px; padding: 1.75rem; backdrop-filter: blur(20px); position: relative; overflow: hidden; margin-bottom: 1rem; }
.glass-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }

/* SIGN GRID */
.sign-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin: 1rem 0; }
.sign-btn { background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(61,26,110,0.15)); border: 1px solid rgba(201,168,76,0.15); border-radius: 12px; padding: 0.75rem 0.4rem; text-align: center; cursor: pointer; transition: all 0.3s ease; }
.sign-btn.active { background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(107,53,176,0.2)); border-color: var(--gold); box-shadow: 0 4px 20px rgba(201,168,76,0.15); }
.sign-btn .glyph { font-size: 1.6rem; display: block; }
.sign-btn .name { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; color: var(--gold-light); text-transform: uppercase; }
.sign-btn .dates { font-size: 0.55rem; color: var(--violet-soft); font-family: 'Space Mono', monospace; }

/* READING */
.reading-container { background: linear-gradient(160deg, rgba(7,3,15,0.95) 0%, rgba(30,10,60,0.6) 100%); border: 1px solid rgba(201,168,76,0.3); border-radius: 24px; padding: 2.5rem; position: relative; margin-top: 1rem; }
.reading-container::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.reading-sign-badge { display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.25); border-radius: 50px; padding: 0.4rem 1rem; margin-bottom: 1.5rem; }
.reading-sign-badge .emoji { font-size: 1.4rem; }
.reading-sign-badge .label { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em; color: var(--gold); text-transform: uppercase; }
.reading-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-style: italic; color: var(--gold-light); margin-bottom: 1rem; }
.reading-body { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; line-height: 1.9; color: #e8e0d4; }
.reading-body p { margin-bottom: 1.2rem; }

/* METERS */
.meter-row { display: flex; align-items: center; gap: 1rem; margin: 0.6rem 0; }
.meter-label { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.08em; color: var(--violet-soft); text-transform: uppercase; width: 90px; flex-shrink: 0; }
.meter-track { flex: 1; height: 4px; background: rgba(255,255,255,0.06); border-radius: 99px; overflow: hidden; }
.meter-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--violet-mid), var(--gold)); }
.meter-val { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: var(--gold); width: 30px; text-align: right; }

/* LUCKY */
.lucky-strip { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem; }
.lucky-pill { background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.2); border-radius: 50px; padding: 0.3rem 0.8rem; font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.08em; color: var(--gold-light); text-transform: uppercase; display: flex; align-items: center; gap: 0.4rem; }

/* PLANET TABLE */
.planet-row { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-family: 'Cormorant Garamond', serif; }
.planet-row:last-child { border-bottom: none; }
.planet-name { display: flex; align-items: center; gap: 0.6rem; font-size: 0.9rem; color: var(--parchment); }
.planet-glyph { font-size: 1.1rem; }
.planet-sign { font-size: 0.75rem; color: var(--violet-soft); font-style: italic; }
.planet-influence { font-size: 0.7rem; font-family: 'Space Mono', monospace; }
.planet-pos { color: var(--teal); }
.planet_pos { color: var(--teal); }
.planet-neg { color: var(--rose); }
.planet_neg { color: var(--rose); }
.planet-neu { color: #888; }
.planet_neu { color: #888; }

/* CHAT */
.chat-bubble-user { background: linear-gradient(135deg, rgba(107,53,176,0.2), rgba(61,26,110,0.3)); border: 1px solid rgba(107,53,176,0.3); border-radius: 16px 16px 4px 16px; padding: 0.9rem 1.2rem; margin: 0.6rem 0; font-family: 'Cormorant Garamond', serif; font-size: 1rem; color: var(--parchment); text-align: right; }
.chat-bubble-ai { background: linear-gradient(135deg, rgba(201,168,76,0.06), rgba(42,138,138,0.08)); border: 1px solid rgba(201,168,76,0.2); border-radius: 16px 16px 16px 4px; padding: 0.9rem 1.2rem; margin: 0.6rem 0; font-family: 'Cormorant Garamond', serif; font-size: 1rem; color: #e8e0d4; line-height: 1.8; }
.chat-label { font-family: 'Space Mono', monospace; font-size: 0.55rem; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.3rem; }

/* TIMELINE */
.timeline-card { background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(61,26,110,0.1)); border: 1px solid rgba(201,168,76,0.12); border-radius: 14px; padding: 1rem 1.25rem; margin: 0.5rem 0; position: relative; overflow: hidden; transition: all 0.25s; }
.timeline-card:hover { border-color: rgba(201,168,76,0.3); background: linear-gradient(135deg, rgba(201,168,76,0.05), rgba(61,26,110,0.15)); }
.timeline-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; }
.timeline-card.pos::before { background: var(--teal); }
.timeline-card.neg::before { background: var(--rose); }
.timeline-card.neu::before { background: var(--gold); }
.tl-date { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: var(--gold); letter-spacing: 0.1em; }
.tl-title { font-family: 'Playfair Display', serif; font-size: 1rem; font-style: italic; color: var(--parchment); margin: 0.2rem 0; }
.tl-body { font-family: 'Cormorant Garamond', serif; font-size: 0.9rem; color: var(--violet-soft); line-height: 1.6; }

/* COMPATIBILITY */
.compat-card { background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(61,26,110,0.12)); border: 1px solid rgba(201,168,76,0.15); border-radius: 16px; padding: 1.25rem; text-align: center; transition: all 0.3s; }
.compat-card:hover { border-color: var(--gold); transform: translateY(-3px); box-shadow: 0 12px 30px rgba(201,168,76,0.12); }
.compat-score-ring { width: 70px; height: 70px; border-radius: 50%; border: 3px solid; display: flex; align-items: center; justify-content: center; margin: 0.5rem auto; font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; }

/* DASHBOARD ENERGY */
.energy-bar-container { margin: 0.4rem 0; }
.energy-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; letter-spacing: 0.08em; color: var(--violet-soft); text-transform: uppercase; display: flex; justify-content: space-between; margin-bottom: 3px; }
.energy-track { height: 6px; background: rgba(255,255,255,0.05); border-radius: 99px; overflow: hidden; }
.energy-fill { height: 100%; border-radius: 99px; }

/* RITUAL BOX */
.ritual-box { background: linear-gradient(135deg, rgba(42,138,138,0.08), rgba(61,26,110,0.12)); border: 1px solid rgba(42,138,138,0.2); border-radius: 14px; padding: 1.1rem 1.3rem; margin: 0.5rem 0; font-family: 'Cormorant Garamond', serif; font-size: 1rem; color: var(--parchment); }
.ritual-icon { font-size: 1.5rem; margin-right: 0.5rem; }

/* SECTION HEADING */
.section-heading { font-family: 'Space Mono', monospace; font-size: 0.58rem; letter-spacing: 0.3em; color: var(--gold); text-transform: uppercase; margin-bottom: 1rem; opacity: 0.85; display: flex; align-items: center; gap: 0.75rem; }
.section-heading::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(201,168,76,0.3), transparent); }

.insight-box { border-left: 2px solid var(--gold); padding: 0.75rem 1rem; background: rgba(201,168,76,0.05); border-radius: 0 10px 10px 0; margin: 1rem 0; font-family: 'Cormorant Garamond', serif; font-style: italic; color: var(--gold-light); font-size: 1rem; }

/* SCORE RING */
.score-ring { text-align: center; padding: 1.25rem; background: var(--card,rgba(255,255,255,0.03)); border: 1px solid rgba(201,168,76,0.15); border-radius: 12px; }
.score-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; line-height: 1; }
.score-label { font-family: 'Space Mono', monospace; font-size: 0.55rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--violet-soft); margin-top: 5px; }

/* STREAMLIT OVERRIDES */
div[data-testid="stButton"] > button { background: linear-gradient(135deg, var(--violet) 0%, var(--violet-mid) 100%) !important; color: var(--gold-light) !important; border: 1px solid rgba(201,168,76,0.35) !important; border-radius: 50px !important; padding: 0.5rem 1.5rem !important; font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; transition: all 0.3s ease !important; box-shadow: 0 4px 20px rgba(61,26,110,0.4) !important; }
div[data-testid="stButton"] > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(201,168,76,0.2) !important; }

label { color: var(--violet-soft) !important; font-family: 'Space Mono', monospace !important; font-size: 0.6rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
div[data-testid="stSpinner"] { color: var(--gold) !important; }
.stAlert { background: rgba(201,168,76,0.08) !important; border: 1px solid rgba(201,168,76,0.2) !important; border-radius: 12px !important; }

div[data-testid="stTabs"] [data-baseweb="tab"] { font-family: 'Space Mono', monospace !important; font-size: 0.58rem !important; letter-spacing: 0.1em !important; color: var(--violet-soft) !important; text-transform: uppercase !important; }
div[data-testid="stTabs"] [aria-selected="true"] { color: var(--gold) !important; border-bottom-color: var(--gold) !important; }
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(201,168,76,0.2) !important; color: var(--parchment) !important; border-radius: 12px !important; font-family: 'Cormorant Garamond', serif !important; font-size: 1rem !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--violet-mid); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# STARFIELD
st.markdown("""
<div class="starfield" id="sf"></div>
<script>
(function(){
  var sf=document.getElementById('sf'); if(!sf) return;
  for(var i=0;i<180;i++){
    var d=document.createElement('div'); var sz=Math.random()*2.5+0.5;
    d.className='star-dot';
    d.style.cssText=`left:${Math.random()*100}%;top:${Math.random()*100}%;width:${sz}px;height:${sz}px;opacity:${Math.random()*0.5+0.1};--dur:${(Math.random()*4+2).toFixed(1)}s;--delay:${(Math.random()*6).toFixed(1)}s;`;
    sf.appendChild(d);
  }
})();
</script>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
SIGNS = [
    {"name":"Aries","glyph":"♈","emoji":"🔥","dates":"Mar 21–Apr 19","element":"Fire","ruler":"Mars","quality":"Cardinal","stone":"Diamond","color":"Crimson","keyword":"Pioneer"},
    {"name":"Taurus","glyph":"♉","emoji":"🌿","dates":"Apr 20–May 20","element":"Earth","ruler":"Venus","quality":"Fixed","stone":"Emerald","color":"Green","keyword":"Builder"},
    {"name":"Gemini","glyph":"♊","emoji":"🌬","dates":"May 21–Jun 20","element":"Air","ruler":"Mercury","quality":"Mutable","stone":"Agate","color":"Yellow","keyword":"Messenger"},
    {"name":"Cancer","glyph":"♋","emoji":"🌊","dates":"Jun 21–Jul 22","element":"Water","ruler":"Moon","quality":"Cardinal","stone":"Pearl","color":"Silver","keyword":"Nurturer"},
    {"name":"Leo","glyph":"♌","emoji":"☀️","dates":"Jul 23–Aug 22","element":"Fire","ruler":"Sun","quality":"Fixed","stone":"Ruby","color":"Gold","keyword":"Sovereign"},
    {"name":"Virgo","glyph":"♍","emoji":"🌾","dates":"Aug 23–Sep 22","element":"Earth","ruler":"Mercury","quality":"Mutable","stone":"Sapphire","color":"Navy","keyword":"Alchemist"},
    {"name":"Libra","glyph":"♎","emoji":"⚖️","dates":"Sep 23–Oct 22","element":"Air","ruler":"Venus","quality":"Cardinal","stone":"Opal","color":"Pink","keyword":"Diplomat"},
    {"name":"Scorpio","glyph":"♏","emoji":"🦂","dates":"Oct 23–Nov 21","element":"Water","ruler":"Pluto","quality":"Fixed","stone":"Topaz","color":"Burgundy","keyword":"Transformer"},
    {"name":"Sagittarius","glyph":"♐","emoji":"🏹","dates":"Nov 22–Dec 21","element":"Fire","ruler":"Jupiter","quality":"Mutable","stone":"Turquoise","color":"Purple","keyword":"Seeker"},
    {"name":"Capricorn","glyph":"♑","emoji":"🏔","dates":"Dec 22–Jan 19","element":"Earth","ruler":"Saturn","quality":"Cardinal","stone":"Garnet","color":"Brown","keyword":"Architect"},
    {"name":"Aquarius","glyph":"♒","emoji":"⚡","dates":"Jan 20–Feb 18","element":"Air","ruler":"Uranus","quality":"Fixed","stone":"Amethyst","color":"Electric Blue","keyword":"Visionary"},
    {"name":"Pisces","glyph":"♓","emoji":"🐟","dates":"Feb 19–Mar 20","element":"Water","ruler":"Neptune","quality":"Mutable","stone":"Aquamarine","color":"Sea Green","keyword":"Dreamer"},
]

DOMAINS = [
    {"id":"daily","icon":"☀️","label":"Daily"},
    {"id":"love","icon":"♥️","label":"Love"},
    {"id":"career","icon":"💼","label":"Career"},
    {"id":"wealth","icon":"💰","label":"Wealth"},
    {"id":"health","icon":"🌿","label":"Health"},
    {"id":"spiritual","icon":"🔮","label":"Spirit"},
    {"id":"karma","icon":"🧿","label":"Karma"},
    {"id":"dream","icon":"🌙","label":"Dreams"},
    {"id":"ritual","icon":"🕯️","label":"Ritual"},
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

DOMAIN_CONTEXTS = {
    "daily":    "a comprehensive daily reading covering all life areas with vivid cosmic imagery",
    "love":     "love, relationships, romance, soul connections, and heart matters",
    "career":   "career, ambition, professional growth, workplace dynamics, and destiny",
    "wealth":   "financial abundance, material prosperity, investment wisdom, and manifestation",
    "health":   "physical vitality, mental wellness, energetic body, and healing paths",
    "spiritual":"spiritual awakening, inner wisdom, metaphysical insights, and cosmic consciousness",
    "karma":    "karmic patterns, past-life echoes, soul lessons, and dharmic purpose in this incarnation",
    "dream":    "dream symbolism, the subconscious landscape, night visions, and their waking meaning",
    "ritual":   "sacred rituals, daily practices, lunar ceremonies, and embodied spiritual tools",
}

RETROGRADE_ALERTS = [
    "⚠️ Mercury Retrograde begins April 9 — back up data, avoid signing contracts",
    "🪐 Saturn squares your natal Sun — a period of karmic reckoning and deep restructuring",
    "♆ Neptune stations retrograde — heightened intuition but beware illusions in partnerships",
]

# ─── ML ENGINE ───────────────────────────────────────────────────────────────
def compute_life_path(dob: datetime.date) -> int:
    s = sum(int(d) for d in str(dob).replace("-",""))
    while s > 9 and s not in (11,22,33):
        s = sum(int(d) for d in str(s))
    return s

def get_chinese_sign(year: int) -> str:
    animals = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Goat","Monkey","Rooster","Dog","Pig"]
    return animals[(year - 1900) % 12]

def planetary_influence_score(sign: dict, dob: datetime.date, domain: str) -> dict:
    seed = hash(f"{sign['name']}{dob}{domain}") & 0xFFFF
    rng = random.Random(seed)
    element_boosts = {
        "Fire":  {"career":10,"health":-5,"love":5,"spiritual":3,"daily":4},
        "Earth": {"wealth":12,"health":8,"career":5,"daily":3,"spiritual":-2},
        "Air":   {"love":10,"spiritual":8,"daily":5,"career":4,"dream":6},
        "Water": {"love":12,"spiritual":15,"health":5,"dream":10,"karma":8},
    }
    base = {k: rng.randint(38,78) for k in ["love","career","wealth","health","spiritual","daily","karma","dream","ritual"]}
    boosts = element_boosts.get(sign["element"], {})
    for k,v in boosts.items():
        base[k] = min(99, max(20, base[k]+v))
    lucky_numbers = sorted(rng.sample(range(1,50), 5))
    lucky_colors  = rng.sample(["Violet","Gold","Teal","Rose","Amber","Sage","Crimson","Azure","Pearl","Indigo"], 3)
    lucky_days    = rng.sample(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], 3)
    life_path     = compute_life_path(dob)
    chinese       = get_chinese_sign(dob.year)
    compat_pool   = [s["name"] for s in SIGNS if s["name"] != sign["name"]]
    return {
        "scores": base,
        "lucky_numbers": lucky_numbers,
        "lucky_colors":  lucky_colors,
        "lucky_days":    lucky_days,
        "life_path":     life_path,
        "chinese":       chinese,
        "compatibility": rng.sample(compat_pool, 3),
        "challenge_sign":rng.choice(compat_pool),
        "soul_mate":     rng.choice(compat_pool),
        "twin_flame":    rng.choice(compat_pool),
    }

def synastry_score(sign1: dict, sign2: dict, dob1: datetime.date, dob2: datetime.date) -> dict:
    seed = hash(f"{sign1['name']}{sign2['name']}{dob1}{dob2}") & 0xFFFF
    rng = random.Random(seed)
    element_harmony = {"Fire":{"Fire":85,"Air":80,"Earth":45,"Water":40},"Earth":{"Earth":82,"Water":78,"Fire":42,"Air":48},"Air":{"Air":88,"Fire":82,"Water":44,"Earth":46},"Water":{"Water":86,"Earth":80,"Air":42,"Fire":40}}
    base_compat = element_harmony.get(sign1["element"],{}).get(sign2["element"],60)
    noise = rng.randint(-12,12)
    overall = min(99, max(20, base_compat+noise))
    return {
        "overall": overall,
        "emotional": min(99, max(15, overall + rng.randint(-15,15))),
        "physical":  min(99, max(15, overall + rng.randint(-15,15))),
        "mental":    min(99, max(15, overall + rng.randint(-15,15))),
        "spiritual": min(99, max(15, overall + rng.randint(-15,15))),
        "growth":    min(99, max(15, overall + rng.randint(-15,15))),
    }

def generate_timeline(sign: dict, dob: datetime.date, domain: str) -> list:
    seed = hash(f"{sign['name']}{dob}{domain}timeline") & 0xFFFF
    rng = random.Random(seed)
    today = datetime.date.today()
    events_pool = {
        "daily":    [("Energetic Peak","Your vitality crests — schedule demanding tasks today","pos"),("Rest Needed","Lunar opposition drains energy; prioritize recovery","neg"),("Unexpected Encounter","Mercury trines your natal chart — chance meetings carry meaning","neu"),("Creative Flow","Venus illuminates your 5th house; artistic projects flourish","pos"),("Review & Reflect","Saturn asks you to audit recent decisions before proceeding","neg"),("Social Magnetism","Your aura amplifies — gatherings and conversations will uplift","pos"),("Inner Guidance Day","Intuitive flashes peak; journal and meditate before acting","neu")],
        "love":     [("Heart Opening","Venus direct lifts barriers — be vulnerable, be seen","pos"),("Tension Point","Mars squares Venus; miscommunication likely — choose words gently","neg"),("Karmic Meeting","A significant soul may cross your path — remain open","neu"),("Rekindled Flame","Old connections resurface with new meaning under this transit","pos"),("Clarity in Love","The fog lifts; you see your relationship or desire with fresh eyes","pos"),("Challenge Week","Saturn tests the foundation — only authentic bonds endure","neg"),("Union Blessing","A rare Jupiter conjunction blesses romantic intentions today","pos")],
        "career":   [("Breakthrough Day","Jupiter expands your professional vision — pitch the bold idea","pos"),("Setback & Lesson","Saturn's friction reveals where mastery is still needed","neg"),("Recognition Moment","Your efforts surface in the right eyes — stay visible","pos"),("Strategic Retreat","Mars retrograde: plan rather than act; let things marinate","neg"),("Power Meeting","A key conversation reshapes your professional trajectory","neu"),("Creative Surge","Innovative solutions flow — present unconventional approaches","pos"),("Contract Caution","Mercury warns: read all documents twice before signing","neg")],
        "wealth":   [("Abundance Window","Jupiter opens a rare portal of financial opportunity this week","pos"),("Guard Your Resources","Neptune squares your 2nd house — watch for hidden costs","neg"),("Investment Insight","Saturn's discipline rewards careful, long-view financial moves","pos"),("Windfall Possibility","Unexpected gains possible through an overlooked channel","pos"),("Reassess Strategy","Pluto urges you to strip away financial patterns that no longer serve","neu"),("Spending Caution","Impulsive Venus transits your 8th house — delay large purchases","neg"),("Manifestation Peak","New Moon amplifies intention — plant seeds for material growth","pos")],
        "health":   [("Vitality Peak","Sun trines your natal Mars — physical energy is exceptional","pos"),("Recovery Phase","Moon in your 12th house calls for rest, not exertion","neg"),("Healing Breakthrough","A long-standing physical pattern finds its resolution","pos"),("Stress Alert","Chiron transit activates old wounds — prioritize nervous system care","neg"),("Movement Ritual","Mars blesses athletic endeavors — begin or intensify practice","pos"),("Detox Window","Waning Moon supports releasing toxins — hydrate, cleanse, rest","neu"),("Mind-Body Sync","Meditation and body practices integrate deeply this week","pos")],
        "spiritual":[ ("Awakening Surge","Neptune direct opens a portal of heightened mystical awareness","pos"),("Dark Night","Pluto demands you descend before you can ascend — trust the void","neg"),("Vision Quest","Vivid dreams and synchronicities cluster — document everything","neu"),("Soul Retrieval","A lost part of yourself returns; integration work is powerful now","pos"),("Ego Dissolution","Saturn dismantles an identity you've outgrown — allow it","neg"),("Cosmic Download","Jupiter stations direct in your 9th — profound philosophical clarity","pos"),("Ritual Power","New Moon ceremony now carries 10x the ordinary potency","pos")],
    }
    pool = events_pool.get(domain, events_pool["daily"])
    rng.shuffle(pool)
    result = []
    for i, (title, body, tone) in enumerate(pool[:7]):
        day = today + datetime.timedelta(days=rng.randint(i*3, i*3+4))
        result.append({"date": day.strftime("%b %d"), "title": title, "body": body, "tone": tone})
    return sorted(result, key=lambda x: x["date"])

# ─── MOON PHASE ──────────────────────────────────────────────────────────────
def get_moon_phase(date: datetime.date) -> tuple:
    known_new = datetime.date(2024,1,11)
    diff  = (date - known_new).days
    cycle = diff % 29.53
    if cycle < 1.85:   return "🌑","New Moon"
    elif cycle < 7.38: return "🌒","Waxing Crescent"
    elif cycle < 9.22: return "🌓","First Quarter"
    elif cycle < 14.77:return "🌔","Waxing Gibbous"
    elif cycle < 16.61:return "🌕","Full Moon"
    elif cycle < 22.15:return "🌖","Waning Gibbous"
    elif cycle < 23.99:return "🌗","Last Quarter"
    else:              return "🌘","Waning Crescent"

# ─── GROQ API ────────────────────────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"

def _make_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)

def generate_horoscope(sign, dob, domain, ml, moon_name, api_key) -> str:
    client = _make_client(api_key)
    today  = datetime.date.today().strftime("%B %d, %Y")
    prompt = f"""You are COSMOS, the world's most gifted astrologer — part mystic oracle, part depth psychologist, part cosmic poet.

Today: {today} | Moon Phase: {moon_name}
Client: {sign['name']} ({sign['glyph']}) · {sign['element']} · {sign['quality']} · Ruler: {sign['ruler']}
DOB: {dob.strftime('%B %d, %Y')} | Life Path: {ml['life_path']} | Chinese Zodiac: {ml['chinese']}
Domain: {domain.upper()} — {DOMAIN_CONTEXTS.get(domain, domain)}
Lucky Numbers: {', '.join(map(str, ml['lucky_numbers']))} | Lucky Colors: {', '.join(ml['lucky_colors'])}
Compatible: {', '.join(ml['compatibility'][:2])} | Challenge: {ml['challenge_sign']}

Write a deeply personal, profoundly insightful horoscope for {domain} in exactly 4 rich paragraphs.
Each paragraph must: (1) open with a cosmic observation, (2) connect to the {domain} situation, (3) offer concrete actionable insight, (4) close with a poetic image or metaphor.

Tone: Mystical yet grounded, poetic yet practical. No generic platitudes. Write specifically for {sign['name']} born {dob.strftime('%B %d, %Y')}.
No bullet points. Flowing lyrical prose, 4-6 sentences per paragraph. Begin immediately — no preamble."""
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=1200, temperature=0.9)
    return r.choices[0].message.content

def generate_affirmation(sign, domain, api_key) -> str:
    client = _make_client(api_key)
    prompt = f"Write ONE powerful, poetic affirmation (max 20 words) for {sign['name']} focused on {domain}. No quotes, just the affirmation. Mystical and empowering."
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=60, temperature=0.85)
    return r.choices[0].message.content.strip()

def generate_compatibility_reading(s1, s2, dob1, dob2, scores, api_key) -> str:
    client = _make_client(api_key)
    prompt = f"""You are COSMOS, cosmic relationship oracle. Analyse the synastry between {s1['name']} (born {dob1}) and {s2['name']} (born {dob2}).

Compatibility scores: Overall {scores['overall']}%, Emotional {scores['emotional']}%, Physical {scores['physical']}%, Mental {scores['mental']}%, Spiritual {scores['spiritual']}%.
Element dynamic: {s1['element']} meets {s2['element']}. Rulers: {s1['ruler']} and {s2['ruler']}.

Write 3 paragraphs: (1) the cosmic chemistry between these two, (2) where they clash and grow, (3) the soul purpose of this connection.
Poetic, insightful, deeply personal. No bullet points. No preamble."""
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=700, temperature=0.88)
    return r.choices[0].message.content

def generate_karma_past_life(sign, dob, ml, api_key) -> str:
    client = _make_client(api_key)
    prompt = f"""You are COSMOS. Reveal the karmic story and past-life echoes of {sign['name']} born {dob.strftime('%B %d, %Y')}.
Life Path {ml['life_path']} · Year of the {ml['chinese']} · Ruling planet: {sign['ruler']}.

Write 3 evocative paragraphs: (1) their dominant past life (era, role, unfinished business), (2) karmic lessons carried into this incarnation, (3) their soul's purpose and dharmic calling.
Mystical, poetic, vivid. No disclaimers. Begin immediately."""
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=700, temperature=0.92)
    return r.choices[0].message.content

def generate_dream_reading(sign, dream_text, api_key) -> str:
    client = _make_client(api_key)
    prompt = f"""You are COSMOS, dream oracle. Interpret this dream for {sign['name']}: "{dream_text}"
Consider {sign['element']} element, {sign['ruler']} rulership, and the archetypal patterns of {sign['name']}.
Write 3 paragraphs: (1) core symbols and their meaning, (2) emotional and subconscious message, (3) guidance for waking life.
Poetic, psychological, mystical. Begin immediately."""
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=600, temperature=0.9)
    return r.choices[0].message.content

def generate_ritual(sign, domain, moon_name, api_key) -> str:
    client = _make_client(api_key)
    prompt = f"""You are COSMOS. Create a personalized ritual for {sign['name']} focused on {domain} under {moon_name}.
Element: {sign['element']} · Ruler: {sign['ruler']} · Stone: {sign['stone']} · Color: {sign['color']}.
Write 1 concise paragraph describing a specific, beautiful ritual (tools, timing, steps, intention).
Practical, sacred, poetic. Include what to gather, what to say or visualize, and how to close. No preamble."""
    r = client.chat.completions.create(model=GROQ_MODEL, messages=[{"role":"user","content":prompt}], max_tokens=350, temperature=0.88)
    return r.choices[0].message.content

def chat_with_cosmos(sign, dob, ml, moon_name, domain, history, user_message, api_key) -> str:
    client = _make_client(api_key)
    sys_prompt = f"""You are COSMOS, the world's wisest astrologer and spiritual advisor. You know this person deeply:
Sign: {sign['name']} ({sign['glyph']}) · {sign['element']} · Ruler: {sign['ruler']} · Quality: {sign['quality']}
DOB: {dob.strftime('%B %d, %Y')} · Life Path: {ml['life_path']} · Chinese: {ml['chinese']} · Moon: {moon_name}
Domain focus: {domain} | Lucky: {', '.join(map(str, ml['lucky_numbers']))} | Compat: {', '.join(ml['compatibility'])}

Respond as a compassionate, wise, mystical advisor. Be specific to their sign and situation. 2-4 sentences max. Poetic but direct. Do not repeat the question."""
    msgs = [{"role":"system","content":sys_prompt}]
    for h in history[-8:]:
        msgs.append({"role":h["role"],"content":h["content"]})
    msgs.append({"role":"user","content":user_message})
    r = client.chat.completions.create(model=GROQ_MODEL, messages=msgs, max_tokens=300, temperature=0.85)
    return r.choices[0].message.content

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✦ COSMOS v2")
    st.markdown("---")
    api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...", help="Free at console.groq.com", label_visibility="visible")
    if api_key: st.success("✓ Groq Key loaded")
    else: st.info("Paste your **Groq key** above.\n\n🆓 Free at console.groq.com")
    st.markdown("---")
    st.markdown("""**⚡ What's New in v2**
- 💬 AI Chat Astrologer
- 💞 Advanced Compatibility
- 📅 7-Day Predictions
- 🧿 Karma & Past Lives
- 🌙 Dream Interpreter
- 🕯️ Personalized Rituals
- 🎛️ Cosmic Dashboard
- ⚠️ Retrograde Alerts""")
    st.markdown("---")
    st.markdown("**⚠️ Active Transits**")
    for alert in RETROGRADE_ALERTS:
        st.caption(alert)

# ─── SESSION STATE ───────────────────────────────────────────────────────────
_defaults = {
    "selected_sign": None, "selected_domain": "daily",
    "reading": None, "ml_data": None, "affirmation": None,
    "dob": datetime.date(1990,1,1),
    "chat_history": [], "compat_reading": None, "compat_scores": None,
    "karma_reading": None, "dream_reading": None, "ritual_text": None,
    "timeline": None,
    "sign2_name": "Libra", "dob2": datetime.date(1992,6,15),
}
for k,v in _defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ─── HEADER ──────────────────────────────────────────────────────────────────
moon_icon, moon_name = get_moon_phase(datetime.date.today())
today_str = datetime.date.today().strftime("%A, %B %d %Y")

st.markdown(f"""
<div class="cosmos-header">
    <div class="cosmos-eyebrow">✦ Celestial Intelligence · Est. Since Time Immemorial ✦</div>
    <h1 class="cosmos-title">COSMOS</h1>
    <p class="cosmos-subtitle">AI Astrologer · Compatibility Oracle · Soul Mapper · Dream Interpreter</p>
    <div class="divider-ornament"><div class="line"></div><div class="gem">✦</div><div class="line"></div></div>
</div>
<div style="text-align:center;margin-bottom:1.5rem;">
    <span style="font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.25em;color:var(--violet-soft);text-transform:uppercase;">
        {today_str} &nbsp;·&nbsp; {moon_icon} {moon_name} &nbsp;·&nbsp; Tropical Zodiac Active
    </span>
</div>
""", unsafe_allow_html=True)

# ─── SIGN DETECTION ──────────────────────────────────────────────────────────
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

# ─── MAIN LAYOUT ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.65], gap="large")

with col_left:
    # BIRTH INFO
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Birth Details</div>', unsafe_allow_html=True)
    dob = st.date_input("Date of Birth", value=st.session_state.dob, min_value=datetime.date(1920,1,1), max_value=datetime.date.today(), key="dob_input")
    st.session_state.dob = dob
    auto_sign = sign_from_dob(dob)
    if st.session_state.selected_sign is None: st.session_state.selected_sign = auto_sign
    life_path = compute_life_path(dob)
    chinese   = get_chinese_sign(dob.year)
    st.markdown(f"""
    <div style="display:flex;gap:1rem;margin-top:0.5rem;flex-wrap:wrap;">
        <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:var(--gold);letter-spacing:0.08em;">✦ {auto_sign['emoji']} {auto_sign['name']}</span>
        <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:var(--violet-soft);">LP {life_path}</span>
        <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:var(--violet-soft);">🐉 {chinese}</span>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SIGN SELECTOR
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Choose Your Sign</div>', unsafe_allow_html=True)
    st.markdown('<div class="sign-grid">', unsafe_allow_html=True)
    for s in SIGNS:
        active = "active" if st.session_state.selected_sign and st.session_state.selected_sign["name"]==s["name"] else ""
        st.markdown(f'<div class="sign-btn {active}"><span class="glyph">{s["emoji"]}</span><span class="name">{s["name"]}</span><span class="dates">{s["dates"]}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,s in enumerate(SIGNS):
        with cols[i%4]:
            if st.button(s["glyph"], key=f"sign_{i}", help=s["name"]):
                st.session_state.selected_sign = s; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # DOMAIN SELECTOR
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Reading Domain</div>', unsafe_allow_html=True)
    dcols = st.columns(3)
    for i,d in enumerate(DOMAINS):
        with dcols[i%3]:
            if st.button(f"{d['icon']} {d['label']}", key=f"dom_{d['id']}"):
                st.session_state.selected_domain = d["id"]; st.rerun()
    active_dom = next((d for d in DOMAINS if d["id"]==st.session_state.selected_domain), DOMAINS[0])
    st.markdown(f'<div style="text-align:center;margin-top:0.5rem;font-family:Space Mono,monospace;font-size:0.58rem;color:var(--gold);letter-spacing:0.1em;">Active: {active_dom["icon"]} {active_dom["label"].upper()}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # GENERATE
    if st.button("✦  REVEAL MY DESTINY  ✦", key="gen_btn"):
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        else:
            sign   = st.session_state.selected_sign or auto_sign
            domain = st.session_state.selected_domain
            ml     = planetary_influence_score(sign, dob, domain)
            with st.spinner("The cosmos is aligning your reading…"):
                reading     = generate_horoscope(sign, dob, domain, ml, moon_name, api_key)
                affirmation = generate_affirmation(sign, domain, api_key)
                timeline    = generate_timeline(sign, dob, domain)
            st.session_state.ml_data     = ml
            st.session_state.reading     = reading
            st.session_state.affirmation = affirmation
            st.session_state.timeline    = timeline
            st.rerun()

# ─── RIGHT COLUMN ─────────────────────────────────────────────────────────────
with col_right:
    sign   = st.session_state.selected_sign or auto_sign
    domain = st.session_state.selected_domain
    ml     = st.session_state.ml_data

    if st.session_state.reading and ml:
        dom_label = next((d["label"] for d in DOMAINS if d["id"]==domain), domain)
        dom_icon  = next((d["icon"]  for d in DOMAINS if d["id"]==domain), "✦")

        tabs = st.tabs(["📜 Reading","📅 Timeline","💬 AI Chat","💞 Compat","🧿 Karma","🌙 Dreams","🕯️ Ritual","🎛️ Dashboard","🪐 Planets"])

        # ── TAB 1: READING ────────────────────────────────────────────────
        with tabs[0]:
            if st.session_state.affirmation:
                st.markdown(f'<div class="insight-box">✦ {st.session_state.affirmation}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="reading-container">
                <div class="reading-sign-badge">
                    <span class="emoji">{sign['emoji']}</span>
                    <span class="label">{sign['name']} · {dom_icon} {dom_label} · {moon_icon} {moon_name}</span>
                </div>
                <div class="reading-title">{sign['name']} · {dom_label} Reading</div>
                <div class="reading-body">""", unsafe_allow_html=True)
            for para in st.session_state.reading.split("\n\n"):
                if para.strip(): st.markdown(f"<p>{para.strip()}</p>", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

            # Scores
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Cosmic Influence Meters</div>', unsafe_allow_html=True)
            for dom_id, score in ml["scores"].items():
                dom_info = next((d for d in DOMAINS if d["id"]==dom_id), {"icon":"✦","label":dom_id})
                st.markdown(f"""<div class="meter-row">
                    <span class="meter-label">{dom_info.get('icon','')} {dom_info.get('label',dom_id)}</span>
                    <div class="meter-track"><div class="meter-fill" style="width:{score}%"></div></div>
                    <span class="meter-val">{score}</span></div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Lucky
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Cosmic Luck Factors</div>', unsafe_allow_html=True)
            st.markdown('<div class="lucky-strip">', unsafe_allow_html=True)
            for n in ml["lucky_numbers"]: st.markdown(f'<span class="lucky-pill">🔢 {n}</span>', unsafe_allow_html=True)
            for c in ml["lucky_colors"]:  st.markdown(f'<span class="lucky-pill">🎨 {c}</span>', unsafe_allow_html=True)
            for d in ml["lucky_days"]:    st.markdown(f'<span class="lucky-pill">📅 {d}</span>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        # ── TAB 2: TIMELINE ───────────────────────────────────────────────
        with tabs[1]:
            st.markdown('<div class="section-heading">7-Day Cosmic Forecast</div>', unsafe_allow_html=True)
            if st.session_state.timeline:
                for ev in st.session_state.timeline:
                    color_map = {"pos":"var(--teal)","neg":"var(--rose)","neu":"var(--gold)"}
                    icon_map  = {"pos":"▲","neg":"▼","neu":"◆"}
                    c = color_map.get(ev["tone"],"var(--gold)")
                    ic= icon_map.get(ev["tone"],"◆")
                    st.markdown(f"""<div class="timeline-card {ev['tone']}">
                        <div class="tl-date">{ic} {ev['date']}</div>
                        <div class="tl-title">{ev['title']}</div>
                        <div class="tl-body">{ev['body']}</div></div>""", unsafe_allow_html=True)
            else:
                st.info("Generate a reading first to see your timeline.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Retrograde & Transit Alerts</div>', unsafe_allow_html=True)
            for alert in RETROGRADE_ALERTS:
                st.markdown(f'<div class="ritual-box">{alert}</div>', unsafe_allow_html=True)

        # ── TAB 3: AI CHAT ────────────────────────────────────────────────
        with tabs[2]:
            st.markdown('<div class="section-heading">Ask the Cosmos</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="max-height:400px;overflow-y:auto;">', unsafe_allow_html=True)
            if not st.session_state.chat_history:
                st.markdown(f'<div style="text-align:center;padding:2rem;font-family:Cormorant Garamond,serif;font-style:italic;color:var(--violet-soft);">The stars await your question, {sign["name"]}…</div>', unsafe_allow_html=True)
            for msg in st.session_state.chat_history[-16:]:
                if msg["role"]=="user":
                    st.markdown(f'<div class="chat-label" style="color:var(--violet-soft);text-align:right;">You</div><div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-label" style="color:var(--gold);">✦ COSMOS</div><div class="chat-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            user_q = st.text_input("Your question", placeholder="e.g. When will I find love? Why is my career stagnant?", label_visibility="collapsed", key="chat_input")
            c1,c2 = st.columns([4,1])
            with c1:
                if st.button("✦ Ask the Stars", key="chat_send", use_container_width=True):
                    if user_q.strip() and api_key:
                        with st.spinner("Consulting the cosmos…"):
                            resp = chat_with_cosmos(sign, dob, ml, moon_name, domain, st.session_state.chat_history, user_q, api_key)
                        st.session_state.chat_history.append({"role":"user","content":user_q})
                        st.session_state.chat_history.append({"role":"assistant","content":resp})
                        st.rerun()
                    elif not api_key: st.error("Add your Groq key in the sidebar.")
            with c2:
                if st.button("Clear", key="chat_clear"):
                    st.session_state.chat_history = []; st.rerun()

        # ── TAB 4: COMPATIBILITY ──────────────────────────────────────────
        with tabs[3]:
            st.markdown('<div class="section-heading">Synastry Compatibility Oracle</div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                st.markdown(f'<div class="glass-card" style="text-align:center;"><div style="font-size:2.5rem">{sign["emoji"]}</div><div style="font-family:Space Mono,monospace;font-size:0.65rem;color:var(--gold);">{sign["name"]}</div><div style="font-family:Cormorant Garamond,serif;font-size:0.85rem;color:var(--violet-soft);">{dob.strftime("%b %d, %Y")}</div></div>', unsafe_allow_html=True)
            with cb:
                sign2_name = st.selectbox("Partner's Sign", [s["name"] for s in SIGNS], index=[s["name"] for s in SIGNS].index(st.session_state.sign2_name), key="sign2_sel")
                sign2 = next(s for s in SIGNS if s["name"]==sign2_name)
                st.session_state.sign2_name = sign2_name
                dob2  = st.date_input("Partner's DOB", value=st.session_state.dob2, key="dob2_input")
                st.session_state.dob2 = dob2
                st.markdown(f'<div style="text-align:center;font-size:2rem;">{sign2["emoji"]}</div>', unsafe_allow_html=True)

            scores = synastry_score(sign, sign2, dob, dob2)
            score_colors = {
                "overall":"var(--gold)","emotional":"var(--rose)","physical":"var(--teal)",
                "mental":"var(--cyan)","spiritual":"var(--violet-mid)","growth":"#a8e6cf"
            }
            st.markdown("<br>", unsafe_allow_html=True)
            s1,s2,s3,s4,s5,s6 = st.columns(6)
            for col, (key, label) in zip([s1,s2,s3,s4,s5,s6], [("overall","Overall"),("emotional","Emotional"),("physical","Physical"),("mental","Mental"),("spiritual","Spiritual"),("growth","Growth")]):
                v = scores[key]; c = score_colors[key]
                col.markdown(f'<div class="compat-card"><div class="compat-score-ring" style="border-color:{c};color:{c};">{v}%</div><div style="font-family:Space Mono,monospace;font-size:0.55rem;color:var(--violet-soft);text-transform:uppercase;letter-spacing:0.08em;">{label}</div></div>', unsafe_allow_html=True)

            if st.button("✦ Generate Compatibility Reading", key="compat_btn", use_container_width=True):
                if not api_key: st.error("Add your Groq key.")
                else:
                    with st.spinner("Reading the synastry chart…"):
                        cr = generate_compatibility_reading(sign, sign2, dob, dob2, scores, api_key)
                    st.session_state.compat_reading = cr
                    st.session_state.compat_scores  = scores
                    st.rerun()
            if st.session_state.compat_reading:
                st.markdown('<div class="reading-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="reading-sign-badge"><span class="emoji">{sign["emoji"]}</span><span class="label">{sign["name"]} × {sign2["emoji"]} {sign2["name"]}</span></div>', unsafe_allow_html=True)
                for para in st.session_state.compat_reading.split("\n\n"):
                    if para.strip(): st.markdown(f'<p class="reading-body">{para.strip()}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ── TAB 5: KARMA ──────────────────────────────────────────────────
        with tabs[4]:
            st.markdown('<div class="section-heading">Karma & Past Life Oracle</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ritual-box"><span class="ritual-icon">🧿</span>Soul Profile: Life Path <strong>{ml["life_path"]}</strong> · Year of the <strong>{ml["chinese"]}</strong> · {sign["name"]} archetype: <em>{sign["keyword"]}</em></div>', unsafe_allow_html=True)

            if st.button("✦ Reveal My Karmic Story", key="karma_btn", use_container_width=True):
                if not api_key: st.error("Add your Groq key.")
                else:
                    with st.spinner("Traversing the Akashic records…"):
                        kr = generate_karma_past_life(sign, dob, ml, api_key)
                    st.session_state.karma_reading = kr
                    st.rerun()
            if st.session_state.karma_reading:
                st.markdown('<div class="reading-container">', unsafe_allow_html=True)
                st.markdown('<div class="reading-sign-badge"><span class="emoji">🧿</span><span class="label">Karmic Record · Past Lives & Soul Purpose</span></div>', unsafe_allow_html=True)
                for para in st.session_state.karma_reading.split("\n\n"):
                    if para.strip(): st.markdown(f'<p class="reading-body">{para.strip()}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ── TAB 6: DREAMS ─────────────────────────────────────────────────
        with tabs[5]:
            st.markdown('<div class="section-heading">Dream Interpretation Oracle</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f'<p style="font-family:Cormorant Garamond,serif;font-style:italic;color:var(--violet-soft);font-size:0.95rem;">Describe your dream and COSMOS will decode its symbols through the lens of {sign["name"]}…</p>', unsafe_allow_html=True)
            dream_text = st.text_area("Your Dream", height=110, placeholder="Last night I dreamed of a vast ocean, a lighthouse, and a silver key that…", label_visibility="collapsed", key="dream_text")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("✦ Interpret My Dream", key="dream_btn", use_container_width=True):
                if not dream_text.strip(): st.warning("Describe your dream first.")
                elif not api_key: st.error("Add your Groq key.")
                else:
                    with st.spinner("Entering the dream realm…"):
                        dr = generate_dream_reading(sign, dream_text, api_key)
                    st.session_state.dream_reading = dr
                    st.rerun()
            if st.session_state.dream_reading:
                st.markdown('<div class="reading-container">', unsafe_allow_html=True)
                st.markdown('<div class="reading-sign-badge"><span class="emoji">🌙</span><span class="label">Dream Oracle · Subconscious Decoded</span></div>', unsafe_allow_html=True)
                for para in st.session_state.dream_reading.split("\n\n"):
                    if para.strip(): st.markdown(f'<p class="reading-body">{para.strip()}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ── TAB 7: RITUAL ─────────────────────────────────────────────────
        with tabs[6]:
            st.markdown('<div class="section-heading">Sacred Ritual Generator</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="glass-card">
                <div style="font-family:Cormorant Garamond,serif;font-size:1rem;color:var(--violet-soft);line-height:1.7;">
                    Your ritual will be crafted for <strong style="color:var(--gold)">{sign['name']}</strong>, 
                    focused on <strong style="color:var(--gold)">{dom_label}</strong>, 
                    aligned with the <strong style="color:var(--gold)">{moon_icon} {moon_name}</strong>.
                    Tools may include your birthstone (<em>{sign['stone']}</em>) and power color (<em>{sign['color']}</em>).
                </div></div>""", unsafe_allow_html=True)
            if st.button("✦ Create My Ritual", key="ritual_btn", use_container_width=True):
                if not api_key: st.error("Add your Groq key.")
                else:
                    with st.spinner("Weaving your sacred practice…"):
                        rt = generate_ritual(sign, domain, moon_name, api_key)
                    st.session_state.ritual_text = rt
                    st.rerun()
            if st.session_state.ritual_text:
                st.markdown('<div class="reading-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="reading-sign-badge"><span class="emoji">🕯️</span><span class="label">{sign["name"]} · {dom_label} Ritual · {moon_name}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="reading-body"><p>{st.session_state.ritual_text}</p></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown(f"""<div class="glass-card" style="margin-top:1rem;">
                    <div class="section-heading">Ritual Toolkit</div>
                    <div class="lucky-strip">
                        <span class="lucky-pill">💎 {sign['stone']}</span>
                        <span class="lucky-pill">🎨 {sign['color']}</span>
                        <span class="lucky-pill">🪐 {sign['ruler']}</span>
                        <span class="lucky-pill">{moon_icon} {moon_name}</span>
                        {''.join(f'<span class="lucky-pill">🔢 {n}</span>' for n in ml['lucky_numbers'][:3])}
                    </div></div>""", unsafe_allow_html=True)

        # ── TAB 8: DASHBOARD ──────────────────────────────────────────────
        with tabs[7]:
            st.markdown('<div class="section-heading">Cosmic Energy Dashboard</div>', unsafe_allow_html=True)

            # Top metrics
            overall_energy = ml["scores"].get(domain, 65)
            peak_domain    = max(ml["scores"], key=ml["scores"].get)
            peak_dom_info  = next((d for d in DOMAINS if d["id"]==peak_domain), {"icon":"✦","label":peak_domain})
            da,db,dc,dd = st.columns(4)
            da.metric(f"{dom_icon} {dom_label} Energy", f"{overall_energy}%")
            db.metric("Peak Domain", f"{peak_dom_info['icon']} {peak_dom_info['label']}")
            dc.metric("Life Path", ml["life_path"])
            dd.metric("Chinese Sign", f"🐉 {ml['chinese']}")

            st.markdown("<br>", unsafe_allow_html=True)
            d1, d2 = st.columns(2)
            with d1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Energy by Domain</div>', unsafe_allow_html=True)
                for dom_id, score in sorted(ml["scores"].items(), key=lambda x: -x[1]):
                    dom_info = next((d for d in DOMAINS if d["id"]==dom_id), {"icon":"✦","label":dom_id})
                    colors   = ["var(--teal)","var(--gold)","var(--violet-mid)","var(--rose)","var(--cyan)","#a78bfa","#f472b6","#34d399","#fb923c"]
                    color    = colors[list(ml["scores"].keys()).index(dom_id) % len(colors)]
                    st.markdown(f"""<div class="energy-bar-container">
                        <div class="energy-label"><span>{dom_info.get('icon','')} {dom_info.get('label',dom_id)}</span><span style="color:var(--gold)">{score}</span></div>
                        <div class="energy-track"><div class="energy-fill" style="width:{score}%;background:{color};"></div></div></div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with d2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Soul Profile</div>', unsafe_allow_html=True)
                lp_meanings = {1:"Pioneer",2:"Diplomat",3:"Creator",4:"Builder",5:"Explorer",6:"Nurturer",7:"Seeker",8:"Achiever",9:"Humanitarian",11:"Illuminator",22:"Master Builder",33:"Master Teacher"}
                lp_label = lp_meanings.get(ml["life_path"],"Mystic")
                st.markdown(f"""
                <div style="text-align:center;padding:1.5rem 0;">
                    <div style="font-family:Playfair Display,serif;font-size:4rem;font-weight:900;background:linear-gradient(135deg,var(--gold-light),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;">{ml['life_path']}</div>
                    <div style="font-family:Space Mono,monospace;font-size:0.58rem;color:var(--gold);letter-spacing:0.15em;text-transform:uppercase;">{lp_label}</div>
                </div>""", unsafe_allow_html=True)
                attrs = [("Sign",f"{sign['emoji']} {sign['name']}"),("Element",sign['element']),("Ruler",sign['ruler']),("Modality",sign['quality']),("Stone",sign['stone']),("Soul Mates"," · ".join(ml['compatibility'][:2])),("Challenge",ml['challenge_sign'])]
                for k,v in attrs:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.05);"><span style="font-family:Space Mono,monospace;font-size:0.57rem;color:var(--violet-soft);text-transform:uppercase;">{k}</span><span style="font-family:Cormorant Garamond,serif;font-size:0.95rem;color:var(--gold-light);">{v}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="glass-card" style="margin-top:0;">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Lucky Factors</div>', unsafe_allow_html=True)
                st.markdown('<div class="lucky-strip">', unsafe_allow_html=True)
                for n in ml["lucky_numbers"]: st.markdown(f'<span class="lucky-pill">🔢 {n}</span>', unsafe_allow_html=True)
                for c in ml["lucky_colors"]:  st.markdown(f'<span class="lucky-pill">🎨 {c}</span>', unsafe_allow_html=True)
                for d in ml["lucky_days"]:    st.markdown(f'<span class="lucky-pill">📅 {d}</span>', unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)

        # ── TAB 9: PLANETS ────────────────────────────────────────────────
        with tabs[8]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Planetary Positions & Influences</div>', unsafe_allow_html=True)
            for p in PLANETS:
                ic = {"pos":"▲ Favorable","neg":"▼ Challenging","neu":"◆ Neutral"}[p["influence"]]
                cls = f"planet_{p['influence']}"
                st.markdown(f"""<div class="planet-row">
                    <div class="planet-name"><span class="planet-glyph">{p['glyph']}</span><span>{p['name']}</span><span class="planet-sign">in {p['sign']}</span></div>
                    <span class="planet-influence {cls}">{ic}</span></div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Sign Archetype Profile</div>', unsafe_allow_html=True)
            for k,v in [("Element",sign["element"]),("Modality",sign["quality"]),("Ruler",sign["ruler"]),("Birthstone",sign["stone"]),("Power Color",sign["color"]),("Archetype",sign["keyword"]),("Soul Mates"," · ".join(ml["compatibility"])),("Growth Challenge",ml["challenge_sign"]),("Soul Mate",ml["soul_mate"]),("Twin Flame",ml["twin_flame"])]:
                st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.05)"><span style="font-family:Space Mono,monospace;font-size:0.58rem;color:var(--violet-soft);letter-spacing:0.08em;text-transform:uppercase">{k}</span><span style="font-family:Cormorant Garamond,serif;font-size:1rem;color:var(--gold-light)">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # WELCOME STATE
        st.markdown(f"""
        <div class="reading-container" style="text-align:center;padding:3.5rem 2rem">
            <div style="font-size:3.5rem;margin-bottom:1rem">{sign['emoji']}</div>
            <div style="font-family:Playfair Display,serif;font-size:1.8rem;font-style:italic;color:var(--gold-light);margin-bottom:0.75rem">Welcome, {sign['name']}</div>
            <div style="font-family:Cormorant Garamond,serif;font-size:1.05rem;color:var(--violet-soft);line-height:1.8;max-width:420px;margin:0 auto;">
                The stars have been watching you. Choose your sign, select a domain, and let the cosmic intelligence reveal your celestial blueprint.
            </div>
            <div style="margin-top:1.5rem;font-family:Space Mono,monospace;font-size:0.58rem;letter-spacing:0.2em;color:var(--gold);opacity:0.6">{moon_icon} {moon_name}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">All Twelve Signs</div>', unsafe_allow_html=True)
        for row_signs in [SIGNS[:6], SIGNS[6:]]:
            rcols = st.columns(6)
            for col, s in zip(rcols, row_signs):
                with col:
                    st.markdown(f'<div style="text-align:center;padding:0.6rem 0"><div style="font-size:1.6rem">{s["emoji"]}</div><div style="font-family:Space Mono,monospace;font-size:0.52rem;color:var(--gold);letter-spacing:0.08em;text-transform:uppercase;margin-top:0.25rem">{s["name"]}</div><div style="font-family:Cormorant Garamond,serif;font-size:0.72rem;color:var(--violet-soft)">{s["element"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:2.5rem 0 1rem;border-top:1px solid rgba(201,168,76,0.1);margin-top:2rem">
    <div style="font-family:Space Mono,monospace;font-size:0.52rem;letter-spacing:0.25em;color:rgba(176,154,212,0.45);text-transform:uppercase">
        ✦ &nbsp; COSMOS v2 · AI Celestial Intelligence · Powered by Groq &amp; LLaMA 3.3 &nbsp; ✦
    </div>
    <div style="font-family:Cormorant Garamond,serif;font-size:0.8rem;color:rgba(176,154,212,0.3);margin-top:0.4rem;font-style:italic">
        For entertainment and personal reflection · {moon_icon} {moon_name}
    </div>
</div>
""", unsafe_allow_html=True)
