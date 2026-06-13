# BaZi (八字) Auto Chart System

> A professional Chinese Four Pillars of Destiny (BaZi) analysis system with AI-powered personalized interpretations, accurate true solar time calculations, and multi-language support.

## ✨ Features

### Core Analysis
- **True Solar Time Calculation** - Uses actual city-level longitude data (200+ cities) with Equation of Time correction for maximum accuracy
- **Four Pillars (四柱) Generation** - Year, Month, Day, Hour pillars based on astronomical solar terms
- **Five Elements (五行) Analysis** - Detailed strength scoring with hidden stems
- **Divine Stars (神煞) Analysis** - 20+ symbolic stars calculation
- **Personality Analysis** - Based on Day Master element and body strength
- **Daily/Weekly/Monthly Fortune** - Personalized fortune based on your BaZi chart

### AI-Powered Insights
- **DeepSeek AI Integration** - Personalized, in-depth analysis of your destiny
- **Streaming Response** - Real-time typewriter effect for analysis display
- **Multi-language Support** - Chinese, English, Japanese, Korean, Vietnamese

### Comprehensive Destiny Reading
- **Grand Fortune (大运)** - 10-year cycle analysis with timeline visualization
- **Annual Fortune (流年)** - Year-by-year detailed predictions covering:
  - 💪 Health
  - 💕 Love & Relationships
  - 💰 Wealth & Finances
  - 💼 Career & Business
  - 📚 Education & Exams
  - 👥 Friendships & Social Life
  - 📌 Likely Events
  - ⚠️ What to Watch Out For
  - ✅ Recommended Actions

### Compatibility Analysis
- **Two-Person Compatibility** - Analyze destiny compatibility between two people
- **Five Elements Complementarity** - See how your elements balance each other
- **Day Master Relationship** - Understand the dynamic between two people

### Sharing & Export
- **Beautiful Share Cards** - Generate shareable destiny cards
- **PDF Report Export** - Professional formatted BaZi report
- **User Accounts** - Save your charts and track daily fortune

## 🌏 Supported Countries

33 countries with accurate solar time calculations:

**Asia:** China, Japan, Korea, Taiwan, Hong Kong, Macau, Vietnam, Thailand, Philippines, Malaysia, Singapore, Indonesia, Myanmar, Sri Lanka, India, Nepal, Bangladesh, Pakistan

**Europe & Americas:** USA, Canada, UK, Germany, France, Russia, Australia, Brazil, Mexico

**Middle East & Africa:** Egypt, South Africa, Nigeria, Turkey, Saudi Arabia, UAE

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bazi-app.git
cd bazi-app

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask init-db

# Run the application
python app.py
```

Open http://127.0.0.1:5000 in your browser.

### Environment Variables (Optional)

```bash
# For AI-powered analysis
set DEEPSEEK_API_KEY=your_api_key_here
```

## 📁 Project Structure

```
bazi_app/
├── app.py                 # Flask application & routes
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── models/
│   ├── user.py           # User authentication model
│   └── chart.py          # Saved chart model
├── core/
│   ├── pipeline.py       # Main analysis orchestrator
│   ├── calendar_engine.py # Solar terms & pillar calculation
│   ├── geo_time_engine.py # True solar time conversion
│   ├── city_lookup.py    # City longitude database
│   ├── wuxing_engine.py  # Five elements scoring
│   ├── shensha_engine.py # Divine stars calculation
│   ├── personality_engine.py # Personality analysis
│   ├── daily_fortune_engine.py # Daily fortune calculation
│   ├── compatibility_engine.py # Two-person compatibility
│   ├── comprehensive_analysis.py # Multi-dimension analysis
│   ├── ai_engine.py      # DeepSeek AI integration
│   ├── share_card.py     # Share card generation
│   └── pdf_engine.py     # PDF report generation
├── templates/
│   ├── base.html         # Base layout
│   ├── index.html        # Homepage with form
│   ├── result.html       # Analysis result display
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── history.html      # Saved charts history
├── static/
│   ├── style.css         # Premium dark theme CSS
│   └── i18n/             # Multi-language files
│       ├── zh.json       # Chinese
│       ├── en.json       # English
│       ├── ja.json       # Japanese
│       ├── ko.json       # Korean
│       └── vi.json       # Vietnamese
└── data/
    └── city_coords.json  # 200+ city longitude data
```

## 🔒 Security Features

- Rate limiting (30 requests/minute per IP)
- XSS prevention with input sanitization
- CSRF protection
- Secure session management (HttpOnly, SameSite)
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Password hashing with Werkzeug

## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI:** DeepSeek API
- **Charts:** Custom BaZi engine with astronomical calculations
- **i18n:** Client-side JSON translation system

## 📱 Responsive Design

- Mobile-first responsive layout
- Bottom navigation for mobile devices
- Touch-friendly buttons and inputs
- Optimized for all screen sizes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Traditional Chinese BaZi (Four Pillars) methodology
- Astronomical solar terms calculation algorithms
- DeepSeek AI for personalized analysis

---

**Disclaimer:** This system provides BaZi analysis as cultural research. Results are for personal reference only and should not be used as the basis for medical, legal, investment, or other high-risk decisions.
