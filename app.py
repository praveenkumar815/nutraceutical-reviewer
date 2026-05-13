import os
import streamlit as st
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

class Ingredient(BaseModel):
    name: str
    dosage: str

class FormulationReview(BaseModel):
    ingredients: list[Ingredient]
    unusual_risky_flags: list[str]
    observations: list[str]
    problematic_claims: list[str]
    summary: str

st.set_page_config(layout="wide")

@st.cache_resource
def init_ai_components():
    # Using the fast Flash model for your demo
    llm_instance = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2)
    embed_instance = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    v_store = Chroma(embedding_function=embed_instance, persist_directory="./chroma_db")
    return llm_instance, v_store

llm, vector_store = init_ai_components()

st.title("Nutraceutical Formulation AI Reviewer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Formulation")
    product_name = st.text_input("Product Name", value="MegaPump Extreme 5000")
    category = st.text_input("Category", value="Pre-Workout")
    ingredients_input = st.text_area("Ingredient List with Dosage", height=150, value="Caffeine Anhydrous - 800mg\nBeta-Alanine - 500mg\nCreatine Monohydrate - 100mg\nTaurine - 10g\nVitamin C - 5mg")
    claims_input = st.text_area("Marketing Claims", height=150, value="Instantly cures muscle fatigue forever.\nGuaranteed to double your bench press in 2 days.\n100% safe for everyone including pregnant women.\nFDA Approved miracle formula!")

    if st.button("Analyze Formulation"):
        prompt = f"""
        Analyze the following supplement formulation.
        Product: {product_name}
        Category: {category}
        Ingredients: {ingredients_input}
        Claims: {claims_input}
        
        Perform the following tasks:
        1. Extract structured ingredient data and dosages.
        2. Identify any unusual or risky dosages/ingredients.
        3. Generate scientific formulation observations.
        4. Flag potentially problematic marketing claims.
        5. Generate a short AI review summary.
        """

        try:
            structured_llm = llm.with_structured_output(FormulationReview)
            with st.spinner("Analyzing formulation via Gemini AI..."):
                result = structured_llm.invoke(prompt)
                st.session_state['review'] = result

            texts = [ing.name for ing in result.ingredients]
            metadatas = [{"product": product_name, "category": category, "dosage": ing.dosage} for ing in result.ingredients]
            
            if texts:
                vector_store.add_texts(texts=texts, metadatas=metadatas)
                
        except Exception as e:
            st.error(f"API Sync Error: {str(e)}")

with col2:
    st.subheader("AI Analysis Results")
    if 'review' in st.session_state:
        res = st.session_state['review']
        
        st.markdown("### 📋 Review Summary")
        st.info(res.summary)
        
        st.markdown("### 🧪 Extracted Ingredients")
        ing_data = [{"Ingredient": i.name, "Dosage": i.dosage} for i in res.ingredients]
        st.table(ing_data)
        
        if res.unusual_risky_flags:
            st.markdown("### ⚠️ Risky Dosages / Flags")
            for flag in res.unusual_risky_flags:
                st.error(f"- {flag}")
        
        if res.problematic_claims:
            st.markdown("### 🚨 Problematic Claims")
            for claim in res.problematic_claims:
                st.warning(f"- {claim}")
                
        st.markdown("### 🔬 Scientific Observations")
        for obs in res.observations:
            st.success(f"- {obs}")

st.divider()
st.subheader("Semantic Ingredient Search")
search_query = st.text_input("Search Database", value="Energy and stimulation")

if st.button("Search") and search_query:
    try:
        docs = vector_store.similarity_search(search_query, k=5)
        if docs:
            for d in docs:
                st.write(f"- **{d.page_content}** (Dosage: {d.metadata.get('dosage')}, Product: {d.metadata.get('product')})")
        else:
            st.write("No matching ingredients found.")
    except Exception as e:
        st.error(f"Vector DB Error: {str(e)}")