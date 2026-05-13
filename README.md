# 💊 Nutraceutical Formulation AI Reviewer

A production-ready AI prototype system for reviewing supplement/nutraceutical formulations using advanced LLMs, embeddings, and semantic search.

## 🎯 Features

- **Structured Data Extraction**: Uses Pydantic models & LLM structured output to extract ingredient data
- **Safety Analysis**: Identifies unusual/risky dosages against reference thresholds
- **Ingredient Intelligence**: Generates scientific observations about formulations
- **Claim Validation**: Flags potentially problematic marketing claims using LLM reasoning
- **AI Review Summaries**: Provides comprehensive AI-generated summaries
- **Semantic Search**: Find related ingredients using Google embeddings + ChromaDB vector search
- **Professional UI**: Clean Streamlit interface with tabs, error handling, and educational content

## 🔬 AI/ML Components

This solution implements **three meaningful AI/ML components** as required:

1. **LLM Reasoning** (Google Gemini 1.5 Flash)
   - Structured output extraction using Pydantic
   - Safety analysis and claim validation
   - Scientific observation generation
   
2. **Embeddings** (Google Generative AI embeddings)
   - Semantic understanding of ingredient properties
   - Query interpretation for search functionality
   
3. **Vector Search** (ChromaDB)
   - Similarity search for ingredient discovery
   - Retrieval pipeline for finding related ingredients
   - Example: "sleep support" finds relevant ingredients like Magnesium, L-Theanine, Melatonin

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/praveenkumar815/nutraceutical-reviewer.git
cd nutraceutical-reviewer
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

**Get your API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

### 5. Run Locally
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📋 Usage

### Analyze a Formulation
1. Enter product name (e.g., "PrePump Energy 3000")
2. Select category from dropdown
3. List ingredients with dosages (one per line)
4. Enter marketing claims to validate
5. Click "🔬 Analyze Formulation"

**Example Input:**
```
Product: PowerLift Pro
Category: Pre-Workout
Ingredients:
  Caffeine - 400mg
  Beta-Alanine - 5g
  Creatine - 5g
  
Claims:
  Guaranteed to increase bench press by 50 lbs
  100% safe for everyone
  FDA approved formula
```

**Output:**
- Extracted & structured ingredients
- Safety flags for over-doses
- Problematic claims highlighted
- Scientific observations
- AI summary with recommendations

### Search Ingredients
1. Switch to "🔍 Ingredient Search" tab
2. Enter semantic query (e.g., "sleep support")
3. Click "Search"
4. View matching ingredients from analyzed products

**Example Queries:**
- "energy and stimulation"
- "sleep support and relaxation"
- "muscle recovery and growth"
- "immune system support"

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add AI nutraceutical reviewer"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repo
4. Select branch: `main`
5. Set file path: `app.py`
6. Click "Deploy"

### Step 3: Add Secrets
1. After deployment, click "Manage" → "Secrets"
2. Add your secret:
   ```
   GOOGLE_API_KEY = "your_api_key"
   ```
3. Click "Save"
4. App will restart automatically

**Live Demo URL:** Will be provided after deployment (format: `https://your-username-nutraceutical-reviewer.streamlit.app`)

## 🏗️ Project Structure

```
nutraceutical-reviewer/
├── app.py                          # Main Streamlit application
├── ingredient_database.py          # Safety database & utilities
├── requirements.txt                # Python dependencies
├── .env                           # Local environment variables
├── README.md                      # This file
├── .streamlit/
│   ├── config.toml               # Streamlit configuration
│   └── secrets_template.toml     # Secrets template
└── chroma_db/                    # Vector database (auto-created)
```

## 📊 How It Works

### Architecture Flow
```
User Input
    ↓
LLM (Gemini 1.5 Flash) - Structured Analysis
    ├─→ Extract Ingredients (Pydantic)
    ├─→ Analyze Safety (vs reference DB)
    ├─→ Validate Claims
    └─→ Generate Observations
    ↓
Embeddings API - Vectorization
    ↓
ChromaDB - Vector Storage
    ↓
Semantic Search - Find Similar Ingredients
    ↓
Display Results UI
```

### Data Flow for Search
```
Query: "sleep support"
    ↓
Embedding Model → Vector representation
    ↓
ChromaDB similarity_search(k=5)
    ↓
Return top 5 matching ingredients
```

## 🛡️ Safety Features

- Input validation on all user inputs
- Error handling with user-friendly messages
- Reference ingredient safety database
- API key protection via environment variables
- No data persistence of personal analyses

## 📝 Example Ingredients Database

The system includes reference data for common ingredients:
- **Caffeine**: Max 400mg, energy/stimulant
- **Beta-Alanine**: Max 6g, performance
- **Creatine**: Max 5g, muscle/strength
- **Magnesium**: Max 400mg, relaxation/sleep
- **L-Theanine**: Max 200mg, focus/relaxation
- And more...

## 🔧 Customization

### Add Custom Ingredients
Edit `ingredient_database.py`:
```python
INGREDIENT_SAFETY_DB = {
    "Your Ingredient": {
        "categories": ["category1", "category2"],
        "max_daily_dose": "XXXmg",
        "warnings": ["warning1", "warning2"],
        "interactions": ["interaction1"],
    },
    ...
}
```

### Modify UI Theme
Edit `.streamlit/config.toml` for colors and styling

### Change LLM Model
In `app.py`, line ~27:
```python
llm_instance = ChatGoogleGenerativeAI(
    model="gemini-pro",  # Try other models
    temperature=0.2
)
```

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'langchain_chroma'"
```bash
pip install -r requirements.txt
```

### "GOOGLE_API_KEY not found"
- Check `.env` file exists with correct key
- On Streamlit Cloud, verify secrets are set in app settings

### "Vector DB Error"
- First run creates the DB automatically
- Run an analysis first to populate the database before searching

### "No matching ingredients found"
- The search database is empty until you run analyses
- Complete at least one formulation analysis to populate the vector DB

## 📚 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.40.0 |
| **LLM** | Google Generative AI (Gemini 1.5 Flash) |
| **Embeddings** | Google Generative AI Embeddings |
| **Vector DB** | ChromaDB 0.5.11 |
| **Framework** | LangChain 0.3.5 |
| **Data Validation** | Pydantic 2.10.0 |
| **Deployment** | Streamlit Cloud |

## 📄 License

This project is provided as-is for educational purposes.

## ⚠️ Medical Disclaimer

This tool provides educational analysis only and should not be used as medical advice. Always consult qualified healthcare professionals before making supplement recommendations. The safety thresholds are based on general guidelines and may vary by individual health conditions.

## 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using LangChain, Streamlit, and Google Generative AI**