import os
import sys
import streamlit as st
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from ingredient_database import check_ingredient_safety, PROBLEMATIC_CLAIMS

# Configure Streamlit to use secrets from .env file
# Must be done before any other Streamlit operations
if 'STREAMLIT_ENV' not in os.environ:
    os.environ['STREAMLIT_ENV'] = 'local'

# Load environment variables from .env file
# Try multiple paths to ensure .env is loaded regardless of working directory
project_root = Path(__file__).parent
env_path = project_root / '.env'

# Force reload with override=True to ensure latest values
load_dotenv(str(env_path), override=True)

# Get API key from Streamlit secrets (Streamlit Cloud) or environment (.env for local)
try:
    # Try Streamlit secrets first (for Streamlit Cloud)
    api_key_from_secrets = st.secrets.get("GOOGLE_API_KEY")
    if api_key_from_secrets:
        os.environ["GOOGLE_API_KEY"] = api_key_from_secrets
except (FileNotFoundError, AttributeError):
    # Fall back to environment variable for local development
    pass

# Verify API key is loaded
api_key_loaded = os.getenv("GOOGLE_API_KEY")
if not api_key_loaded:
    # Try alternative loading method
    load_dotenv(dotenv_path='.env', override=True)

# Configure page
st.set_page_config(
    page_title="Nutraceutical AI Reviewer",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

class Ingredient(BaseModel):
    name: str
    dosage: str

class FormulationReview(BaseModel):
    ingredients: list[Ingredient]
    unusual_risky_flags: list[str]
    observations: list[str]
    problematic_claims: list[str]
    summary: str

@st.cache_resource
def init_ai_components():
    """Initialize AI components with comprehensive error handling."""
    try:
        # Check API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key or api_key.strip() == "":
            raise ValueError(
                "GOOGLE_API_KEY is not set in the environment. Please:\n"
                "1. Create a .env file in the project root\n"
                "2. Add: GOOGLE_API_KEY=your_api_key_here\n"
                "3. Restart the Streamlit app"
            )
        
        if len(api_key) < 30:
            raise ValueError(f"API key appears invalid (too short: {len(api_key)} chars)")
        
        # Initialize LLM
        try:
            llm_instance = ChatGoogleGenerativeAI(
                model="gemini-flash-latest",
                temperature=0.2,
                api_key=api_key,
                timeout=30
            )
            # Test the LLM with a simple call
            llm_instance.invoke("test")
        except Exception as e:
            raise ValueError(f"LLM initialization failed: {str(e)}")
        
        # Initialize embeddings
        try:
            embed_instance = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                api_key=api_key,
                timeout=30
            )
        except Exception as e:
            raise ValueError(f"Embeddings initialization failed: {str(e)}")
        
        # Initialize vector store
        try:
            v_store = Chroma(
                embedding_function=embed_instance,
                persist_directory="./chroma_db"
            )
        except Exception as e:
            raise ValueError(f"Vector store initialization failed: {str(e)}")
        
        return llm_instance, v_store
    except Exception as e:
        return None, None

llm, vector_store = init_ai_components()

# Check if initialization was successful
if llm is None or vector_store is None:
    st.error("❌ Failed to initialize AI components")
    st.warning("""
    **Setup Required:**
    
    1. Make sure you have a `.env` file in the project root directory
    2. Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`
    3. Save the file
    4. Refresh this page
    
    **Get your API key:**
    - Visit: https://makersuite.google.com/app/apikey
    - Create a new API key
    - Copy it to your `.env` file
    """)
    st.stop()

# Page Title
st.title("💊 Nutraceutical Formulation AI Reviewer")
st.markdown("---")
st.markdown("""
**AI-powered analysis system for supplement formulations**
- Extracts & structures ingredient data
- Identifies risky dosages & ingredients  
- Flags problematic marketing claims
- Generates scientific observations
- Enables semantic ingredient search with embeddings
""")

st.markdown("---")

# Create tabs for different sections
tab1, tab2 = st.tabs(["📋 Formulation Analysis", "🔍 Ingredient Search"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Formulation")
        
        product_name = st.text_input(
            "Product Name",
            value="MegaPump Extreme 5000",
            help="Enter the supplement/product name"
        )
        
        category = st.selectbox(
            "Category",
            [
                "Pre-Workout",
                "Post-Workout",
                "Sleep Support",
                "Energy",
                "Immune Support",
                "Muscle Building",
                "Recovery",
                "Other"
            ],
            index=0
        )
        
        ingredients_input = st.text_area(
            "Ingredient List with Dosage",
            height=150,
            value="Caffeine Anhydrous - 800mg\nBeta-Alanine - 500mg\nCreatine Monohydrate - 100mg\nTaurine - 10g\nVitamin C - 5mg",
            help="Enter each ingredient on a new line with dosage (e.g., 'Caffeine - 200mg')"
        )
        
        claims_input = st.text_area(
            "Marketing Claims",
            height=150,
            value="Instantly cures muscle fatigue forever.\nGuaranteed to double your bench press in 2 days.\n100% safe for everyone including pregnant women.\nFDA Approved miracle formula!",
            help="Enter marketing claims you want analyzed (one per line)"
        )

        analyze_button = st.button("🔬 Analyze Formulation", use_container_width=True)

        if analyze_button:
            if not llm or not vector_store:
                st.error("⚠️ AI components not initialized. Check your API key in .env file")
            else:
                prompt = f"""
                Analyze the following supplement formulation thoroughly.
                Product: {product_name}
                Category: {category}
                Ingredients: {ingredients_input}
                Marketing Claims: {claims_input}
                
                Perform the following tasks:
                1. Extract structured ingredient data and dosages carefully.
                2. Identify any unusual, high-risk, or potentially unsafe dosages/ingredients based on medical guidelines.
                3. Generate detailed scientific formulation observations.
                4. Flag each problematic marketing claim and explain why it's problematic.
                5. Generate a comprehensive AI review summary with recommendations.
                
                Be thorough and safety-conscious in your analysis.
                """

                try:
                    structured_llm = llm.with_structured_output(FormulationReview)
                    with st.spinner("🤖 Analyzing formulation via Gemini AI..."):
                        result = structured_llm.invoke(prompt)
                        st.session_state['review'] = result

                    # Add to vector store for semantic search
                    texts = [ing.name for ing in result.ingredients]
                    metadatas = [
                        {
                            "product": product_name,
                            "category": category,
                            "dosage": ing.dosage
                        }
                        for ing in result.ingredients
                    ]
                    
                    if texts:
                        vector_store.add_texts(texts=texts, metadatas=metadatas)
                    
                    st.success("✅ Analysis complete!")
                        
                except Exception as e:
                    st.error(f"❌ Analysis Error: {str(e)}")
                    st.info("Please check your GOOGLE_API_KEY and try again.")

    with col2:
        st.subheader("Analysis Results")
        if 'review' in st.session_state:
            res = st.session_state['review']
            
            st.markdown("### 📋 Summary")
            st.info(res.summary)
            
            st.markdown("### 🧪 Extracted Ingredients")
            ing_data = [
                {"Ingredient": i.name, "Dosage": i.dosage}
                for i in res.ingredients
            ]
            st.table(ing_data)
            
            # Check ingredients against safety database
            st.markdown("### ⚠️ Safety Check")
            for ingredient in res.ingredients:
                safety_check = check_ingredient_safety(ingredient.name, ingredient.dosage)
                if safety_check["safe"] is False:
                    st.error(f"🚨 {ingredient.name}: {safety_check['message']}")
                elif safety_check["safe"] is True:
                    st.success(f"✓ {ingredient.name}: {safety_check['message']}")
                else:
                    st.warning(f"❓ {ingredient.name}: {safety_check['message']}")
            
            if res.unusual_risky_flags:
                st.markdown("### ⚠️ Risky Dosages / Flags")
                for flag in res.unusual_risky_flags:
                    st.error(f"- {flag}")
            else:
                st.info("No unusual risky dosages detected.")
            
            if res.problematic_claims:
                st.markdown("### 🚨 Problematic Claims")
                for claim in res.problematic_claims:
                    st.warning(f"- {claim}")
            else:
                st.info("No problematic claims detected.")
                
            if res.observations:
                st.markdown("### 🔬 Scientific Observations")
                for obs in res.observations:
                    st.success(f"- {obs}")
        else:
            st.info("👈 Enter formulation details and click 'Analyze Formulation' to get started")

with tab2:
    st.subheader("Semantic Ingredient Search")
    st.markdown("""
    Search for ingredients based on their properties, effects, or categories.
    Uses AI embeddings to find semantically related ingredients in the database.
    
    **Example queries:**
    - "energy and stimulation"
    - "sleep support and relaxation"
    - "muscle recovery and performance"
    """)
    
    search_query = st.text_input(
        "Search Query",
        value="sleep support",
        placeholder="Enter search query (e.g., 'energy boost', 'sleep support')"
    )
    
    search_col1, search_col2 = st.columns([3, 1])
    with search_col2:
        search_button = st.button("Search", use_container_width=True)
    
    if search_button and search_query:
        if not vector_store:
            st.error("Vector store not initialized. Run an analysis first.")
        else:
            try:
                with st.spinner("🔍 Searching ingredient database..."):
                    docs = vector_store.similarity_search(search_query, k=5)
                
                if docs:
                    st.success(f"Found {len(docs)} matching ingredients")
                    for i, d in enumerate(docs, 1):
                        col_left, col_right = st.columns([2, 1])
                        with col_left:
                            st.write(f"**{i}. {d.page_content}**")
                        with col_right:
                            st.caption(f"Dosage: {d.metadata.get('dosage', 'N/A')}")
                        st.caption(f"Product: {d.metadata.get('product', 'N/A')} | Category: {d.metadata.get('category', 'N/A')}")
                else:
                    st.info("No matching ingredients found in the database. Run an analysis to populate the database.")
            except Exception as e:
                st.error(f"❌ Search Error: {str(e)}")

# Sidebar information
with st.sidebar:
    st.markdown("### 📚 About This Tool")
    st.markdown("""
    This AI-powered system helps review supplement formulations by:
    
    1. **Extracting Data**: Parses ingredients and dosages using LLM
    2. **Safety Analysis**: Checks against reference safety thresholds
    3. **Claim Validation**: Flags misleading marketing claims
    4. **Vector Search**: Uses embeddings to find similar ingredients
    
    **AI/ML Components:**
    - LLM: Google Gemini 1.5 Flash (structured reasoning)
    - Embeddings: Google's embedding model
    - Vector DB: ChromaDB (similarity search)
    """)
    
    st.divider()
    st.markdown("### 🔧 How to Use")
    st.markdown("""
    1. Fill in product details
    2. List ingredients with dosages
    3. Enter marketing claims
    4. Click "Analyze Formulation"
    5. Review AI analysis
    6. Use search to find related ingredients
    """)
    
    st.divider()
    st.markdown("### ⚠️ Disclaimer")
    st.markdown("""
    This tool provides educational analysis only.
    Always consult healthcare professionals before making
    supplement recommendations.
    """)
    
    st.divider()
    st.markdown("### 🎯 Example Queries")
    st.code("""
    - "ingredients related to sleep"
    - "energy and stimulation"
    - "muscle recovery"
    - "immune support"
    """, language="text")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
<p>🧬 Nutraceutical Formulation AI Reviewer | Powered by Google Gemini & ChromaDB</p>
<p>Built with Streamlit • Using LangChain & Embeddings for semantic analysis</p>
</div>
""", unsafe_allow_html=True)