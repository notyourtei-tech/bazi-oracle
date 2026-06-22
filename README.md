# BaZi (八字) Auto Chart System

> A professional Chinese Four Pillars of Destiny (BaZi) analysis system with AI-powered interpretations, true solar time calculations, multi-language support, and guided onboarding.

## ✨ Features

### Core Analysis
- **True Solar Time Calculation** - Uses actual city-level longitude data (200+ cities) with Equation of Time correction
- **Four Pillars (四柱) Generation** - Year, Month, Day, Hour pillars based on astronomical solar terms
- **Five Elements (五行) Analysis** - Detailed strength scoring with hidden stems
- **Divine Stars (神煞) Analysis** - 20+ symbolic stars with detailed interpretations
- **Personality Analysis** - Based on Day Master element and body strength
- **Daily/Weekly/Monthly Fortune** - Personalized fortune based on your BaZi chart
- **Comprehensive Life Advice** - Career, wealth, relationship, health, study, and social guidance

### AI-Powered Insights
- **OpenRouter AI Integration** - Personalized, in-depth analysis of your destiny
- **Streaming Response** - Real-time typewriter effect for analysis display

### User Experience
- **Language Selection Modal** - First-time users choose from 5 languages (中文, 日本語, English, 한국어, Tiếng Việt)
- **Onboarding Tutorial** - 4-step guided introduction to the system
- **My BaZi (我的八字)** - Mark any chart as your own, always displayed on homepage
- **Consultation Page** - Dedicated page with WeChat/LINE QR codes for paid consultation
- **Session Persistence** - Login state remembered for 30 days

### Comprehensive Destiny Reading
- **Grand Fortune (大运)** - 10-year cycle analysis with timeline visualization
- **Annual Fortune (流年)** - Year-by-year predictions covering health, love, wealth, career, education, and social life
- **Ten Gods (十神) Analysis** - Detailed personality traits based on Day Master relationships

### Compatibility Analysis
- **Two-Person Compatibility** - Analyze destiny compatibility between two people
- **Five Elements Complementarity** - See how your elements balance each other

### Sharing & Export
- **Beautiful Share Cards** - Generate shareable destiny cards (requires Pillow)
- **PDF Report Export** - Professional formatted BaZi report (requires ReportLab)
- **User Accounts** - Save charts, track fortune, and manage "My BaZi"

## 🌏 Supported Countries

90+ countries with accurate solar time calculations:

**East Asia:** China, Japan, South Korea, Taiwan, Hong Kong, Macau, Mongolia

**Southeast Asia:** Vietnam, Thailand, Philippines, Malaysia, Singapore, Indonesia, Myanmar, Cambodia, Laos, Brunei

**South Asia:** India, Pakistan, Bangladesh, Sri Lanka, Nepal, Maldives

**West & Central Asia:** Turkey, Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Oman, Israel, Jordan, Lebanon, Iraq, Iran, Kazakhstan, Uzbekistan

**Europe:** UK, Germany, France, Italy, Spain, Portugal, Netherlands, Belgium, Switzerland, Austria, Sweden, Norway, Denmark, Finland, Poland, Czech Republic, Greece, Ireland, Romania, Ukraine, Hungary, Russia

**Americas:** USA, Canada, Mexico, Guatemala, Cuba, Jamaica, Panama, Brazil, Argentina, Chile, Colombia, Peru, Venezuela, Ecuador

**Africa:** Egypt, South Africa, Nigeria, Kenya, Ghana, Morocco, Ethiopia, Tanzania, Algeria

**Oceania:** Australia, New Zealand, Fiji

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
# For AI-powered analysis (OpenRouter)
set OPENROUTER_API_KEY=your_api_key_here
```

## 📁 Project Structure

```
bazi_app/
├── app.py                  # Flask application & routes
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── models/
│   ├── user.py            # User authentication model
│   └── chart.py           # Saved chart model (with is_own field)
├── core/
│   ├── pipeline.py        # Main analysis orchestrator
│   ├── calendar_engine.py  # Solar terms & pillar calculation
│   ├── geo_time_engine.py  # True solar time conversion
│   ├── city_lookup.py     # City longitude database
│   ├── wuxing_engine.py   # Five elements scoring
│   ├── shensha_engine.py  # Divine stars calculation
│   ├── personality_engine.py  # Personality analysis
│   ├── interpretation_engine.py # Comprehensive interpretation
│   ├── daily_fortune_engine.py  # Daily fortune calculation
│   ├── compatibility_engine.py  # Two-person compatibility
│   ├── comprehensive_analysis.py # Multi-dimension analysis
│   ├── ai_engine.py       # OpenRouter AI integration
│   ├── share_card.py      # Share card generation (Pillow)
│   ├── pdf_engine.py      # PDF report generation (ReportLab)
│   └── security.py        # Rate limiting, CSRF, validation
├── templates/
│   ├── base.html          # Base layout with nav, modals, footer
│   ├── index.html         # Homepage with form & "My BaZi"
│   ├── result.html        # Analysis result with tabbed view
│   ├── history.html       # History with "Set as My BaZi"
│   ├── consult.html       # Consultation page with QR codes
│   ├── explain.html       # System explanation & disclaimer
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── static/
│   ├── style.css          # Premium dark theme CSS
│   ├── weixin.jpg         # WeChat QR code
│   ├── line.jpg           # LINE QR code
│   └── i18n/              # Multi-language files
│       ├── zh.json        # Chinese (中文)
│       ├── en.json        # English
│       ├── ja.json        # Japanese (日本語)
│       ├── ko.json        # Korean (한국어)
│       └── vi.json        # Vietnamese (Tiếng Việt)
└── data/
    └── city_coords.json   # 200+ city longitude data
```

## 🔒 Security Features

- Rate limiting (120 requests/minute per IP)
- XSS prevention with input sanitization
- CSRF protection on all forms
- Secure session management (HttpOnly, SameSite, 30-day expiry)
- Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- Password hashing with Werkzeug
- Login attempt brute-force protection
- Blocked common attack paths (wp-admin, phpmyadmin, etc.)

## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI:** OpenRouter API (optional)
- **Charts:** Custom BaZi engine with astronomical calculations
- **i18n:** Client-side JSON translation system (5 languages)
- **Export:** Pillow (share cards), ReportLab (PDF reports)

## 📱 Responsive Design

- Mobile-first responsive layout
- Bottom navigation for mobile devices
- Touch-friendly buttons and inputs
- Optimized for all screen sizes
- Language selection modal for first-time visitors

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
- OpenRouter AI for personalized analysis

---

**Disclaimer:** This system provides BaZi analysis as cultural research and entertainment. Results are for personal reference only and should not be used as the basis for medical, legal, investment, or other high-risk decisions. For detailed personalized consultation, contact the author via WeChat or LINE (paid service).
