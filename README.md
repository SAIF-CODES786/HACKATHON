# Automated Resume Screening System

An AI-powered full-stack web application that automates resume parsing, scoring, and ranking for recruitment processes using machine learning.

![Resume Screening System](https://img.shields.io/badge/Status-Production%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![React](https://img.shields.io/badge/React-18.2-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

## 🎯 Features

- **📄 Resume Parsing**: Automatically extract information from PDF and DOCX resumes
  - Personal details (name, email, phone)
  - Skills and technologies
  - Work experience and years
  - Education history
  - Certifications

- **🤖 ML-Based Scoring**: Intelligent candidate ranking using:
  - TF-IDF vectorization for skill matching (40% weight)
  - Experience level scoring (25% weight)
  - Education qualification scoring (20% weight)
  - Certification relevance (15% weight)
  - Cosine similarity for job description matching

- **📊 Visual Analytics**: Interactive charts and insights
  - Skill distribution across candidate pool
  - Experience level breakdown
  - Score distribution histogram
  - Top candidate comparisons

- **💼 Modern UI**: Clean, responsive React interface
  - Drag-and-drop resume upload
  - Real-time candidate rankings
  - Filterable dashboard
  - Detailed candidate profiles
  - Export to CSV/Excel

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX parsing
- **spaCy** - NLP for entity extraction
- **scikit-learn** - TF-IDF and ML algorithms
- **pandas** - Data processing
- **matplotlib/seaborn** - Chart generation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Axios** - API communication
- **react-dropzone** - File upload

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Create environment file**
```bash
cp .env.example .env
```

6. **Run the backend server**
```bash
python main.py
```

The backend will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

## 🚀 Usage

1. **Upload Resumes**
   - Drag and drop PDF or DOCX files
   - Or click to browse and select files
   - Upload multiple resumes at once

2. **Enter Job Description**
   - Paste the complete job description
   - Optionally specify required skills (comma-separated)
   - Set experience range (min/max years)

3. **Score & Rank**
   - Click "Score & Rank Candidates"
   - View ranked candidates with detailed scores
   - Filter by minimum score threshold
   - Sort by different criteria

4. **View Analytics**
   - Switch to Analytics tab
   - View skill distribution charts
   - Analyze experience levels
   - See score distributions

5. **Export Results**
   - Export ranked candidates to CSV or Excel
   - Download for further analysis

## 📁 Project Structure

```
resume-screening-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── resume_parser.py      # Resume parsing logic
│   │   ├── scoring_engine.py     # ML scoring algorithm
│   │   ├── analytics.py          # Chart generation
│   │   └── routes.py             # API endpoints
│   ├── main.py                   # FastAPI app entry
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadSection.jsx
│   │   │   ├── JobDescriptionForm.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── CandidateDetail.jsx
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.jsx               # Main component
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── sample_data/                  # Sample resumes and job descriptions
├── README.md
└── API_DOCUMENTATION.md
```

## 🔧 Configuration

### Backend Environment Variables (.env)

```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,docx
```

### Scoring Weights

Customize scoring weights in `backend/app/scoring_engine.py`:

```python
WEIGHTS = {
    'skills': 0.40,         # 40%
    'experience': 0.25,     # 25%
    'education': 0.20,      # 20%
    'certifications': 0.15  # 15%
}
```

## 📊 API Endpoints

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API documentation.

**Key Endpoints:**
- `POST /api/upload` - Upload resumes
- `POST /api/score` - Score candidates
- `GET /api/rankings` - Get ranked candidates
- `GET /api/analytics` - Get analytics data
- `GET /api/export` - Export results

## 🧪 Testing

### Test with Sample Data

Sample resumes and job descriptions are provided in `sample_data/`:

```bash
# Use the sample files to test the system
# Upload the PDFs/DOCX files through the UI
# Use sample_job_description.txt for scoring
```

### Run Backend Tests

```bash
cd backend
pytest tests/
```

## 🎨 Customization

### Adding New Skills

Edit `SKILLS_DATABASE` in `backend/app/resume_parser.py`:

```python
SKILLS_DATABASE = {
    'programming': ['python', 'java', ...],
    'web': ['react', 'angular', ...],
    # Add your categories
}
```

### Modifying UI Theme

Edit colors in `frontend/tailwind.config.js`:

```javascript
colors: {
  primary: { ... },
  accent: { ... }
}
```

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure Python 3.9+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

**Frontend build errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version`

**Resume parsing issues:**
- Ensure spaCy model is downloaded
- Check file format (PDF/DOCX only)
- Verify file is not corrupted

**CORS errors:**
- Check ALLOWED_ORIGINS in .env
- Ensure backend is running on port 8000

## 📝 License

MIT License - feel free to use for your hackathon or commercial projects!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🏆 Hackathon Tips

- **Demo Flow**: Upload → Score → Show Analytics → Export
- **Talking Points**: ML algorithms, real-time processing, scalability
- **Improvements**: Add more ML models, database integration, user authentication
- **Deployment**: Can be deployed on Heroku, AWS, or Vercel

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ for hackathons and recruitment automation**
