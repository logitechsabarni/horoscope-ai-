# ✦ COSMOS — AI Horoscope App

> *"The stars have been watching you. Let the cosmos reveal what the universe has written in your celestial blueprint."*

A premium, AI-powered astrology application built with **Python + Streamlit + Groq AI**.  
Dark celestial design · ML planetary scoring · Real numerology · Live moon phases.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🔮 AI Readings | Deep 4-paragraph horoscopes via Groq (LLaMA 3.3 70B) |
| ♈ 12 Zodiac Signs | Auto-detected from your date of birth |
| 🌙 Moon Phases | Real-time lunar cycle calculated from synodic orbit |
| 🔢 Numerology | Life Path number with Pythagorean reduction (incl. master numbers 11, 22, 33) |
| 🐉 Chinese Zodiac | Birth year animal detection |
| 🪐 Planet Table | 10 planets with signs + favorable/challenging/neutral ratings |
| 📊 ML Scoring | Deterministic influence scores per sign × DOB × domain |
| 💫 6 Domains | Daily · Love · Career · Wealth · Health · Spiritual |
| 🍀 Lucky Factors | Numbers, colors, and days of the week |
| 💞 Compatibility | Cosmic soulmates + challenge signs |
| ✨ Affirmation | Personal AI-generated cosmic mantra |
| 🎨 Premium UI | Animated starfield, glass-morphism cards, gold/violet palette |

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
pip install streamlit groq
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Get a FREE Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up with your Google account (free, instant, no credit card)
3. Navigate to **API Keys → Create API Key**
4. Copy the key — it starts with `gsk_...`

> **Why Groq?** It's completely free (14,400 requests/day), blazing fast (LPU hardware), and uses LLaMA 3.3 70B which produces excellent horoscope readings.

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Use the app

1. The sidebar opens automatically — paste your `gsk_...` key there
2. Enter your **Date of Birth**
3. Your zodiac sign is auto-detected (or pick one manually)
4. Choose a **Reading Domain** (Daily, Love, Career, etc.)
5. Click **✦ REVEAL MY DESTINY ✦**

---

## 🗂️ Project Structure

```
cosmos/
├── app.py            ← Main Streamlit app (single file, everything inside)
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🧠 How the ML Engine Works

The app uses a **deterministic ML scoring engine** — not random. The same birth date + sign + domain always produces the same scores (reproducible, like a real astrological chart).

### Planetary Influence Scoring
- Seed = `hash(sign_name + date_of_birth + domain)`
- Base scores (40–75) generated per domain
- **Element boosts** applied on top:
  - 🔥 Fire signs → Career +10, Love +5
  - 🌍 Earth signs → Wealth +12, Health +8
  - 🌬 Air signs → Love +10, Spiritual +8
  - 🌊 Water signs → Spiritual +15, Love +12

### Numerology (Pythagorean Reduction)
```
DOB digits → sum → reduce to single digit
Master numbers 11, 22, 33 are never reduced
```

### Moon Phase (Synodic Cycle Algorithm)
```
Anchor: Known New Moon = Jan 11, 2024
Days since anchor → modulo 29.53 → phase bracket
```

### Chinese Zodiac
```
(birth_year - 1900) % 12 → animal index
```

---

## 🎨 Design System

| Element | Choice |
|---|---|
| Primary Font | Playfair Display (serif, italic headings) |
| Body Font | Cormorant Garamond (elegant prose) |
| Mono Font | Space Mono (labels, data) |
| Theme | Dark celestial — deep violet #07030f |
| Accent | Gold #c9a84c |
| Cards | Glass-morphism with gold border |
| Background | Animated 160-star starfield |
| Layout | 3-tab reading output: Reading · Planets · Numerology |

---

## 🔧 Configuration

You can change the AI model by editing line ~484 in `app.py`:

```python
GROQ_MODEL = "llama-3.3-70b-versatile"   # default (best quality)
# GROQ_MODEL = "llama-3.1-8b-instant"    # faster, lighter
# GROQ_MODEL = "mixtral-8x7b-32768"      # alternative
```

---

## 📦 Requirements

```
streamlit>=1.35.0
groq>=0.9.0
```

Python 3.9+ recommended.

---

## 🚀 Free Tier Limits (Groq)

| Metric | Free Limit |
|---|---|
| Requests per day | 14,400 |
| Requests per minute | 30 |
| Tokens per minute | 6,000 |


✦  COSMOS · AI Celestial Intelligence · Powered by Groq + LLaMA  ✦

*The cosmos speaks — you decide.*

https://spiwiak53fccxzet2mgbdj.streamlit.app/- This is the app
