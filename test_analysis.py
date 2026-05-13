"""
Sample/demo script to test the ingredient analysis without running the full Streamlit app.
Can be run from command line: python test_analysis.py
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

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

def test_formulation_analysis():
    """Test the LLM analysis without vector DB."""
    print("🧬 Testing Nutraceutical Formulation Analyzer")
    print("=" * 50)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return
    
    try:
        # Initialize LLM
        print("\n🔄 Initializing Gemini AI...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
        
        # Test formulation
        test_product = "PowerBoost Energy"
        test_category = "Pre-Workout"
        test_ingredients = """
        Caffeine Anhydrous - 800mg
        Beta-Alanine - 6000mg
        Taurine - 15000mg
        Vitamin B12 - 1000mcg
        """
        test_claims = """
        Guaranteed to increase strength by 100%
        Safe for children and pregnant women
        FDA approved
        """
        
        prompt = f"""
        Analyze this supplement formulation:
        Product: {test_product}
        Category: {test_category}
        Ingredients: {test_ingredients}
        Claims: {test_claims}
        
        Extract structured data, identify safety issues, and flag problematic claims.
        """
        
        print(f"\n📊 Analyzing: {test_product}")
        print(f"Category: {test_category}")
        
        structured_llm = llm.with_structured_output(FormulationReview)
        result = structured_llm.invoke(prompt)
        
        print("\n✅ Analysis Complete!")
        print("-" * 50)
        
        print(f"\n🧪 Extracted Ingredients ({len(result.ingredients)}):")
        for ing in result.ingredients:
            print(f"  • {ing.name}: {ing.dosage}")
        
        print(f"\n⚠️  Risk Flags ({len(result.unusual_risky_flags)}):")
        for flag in result.unusual_risky_flags:
            print(f"  • {flag}")
        
        print(f"\n🚨 Problematic Claims ({len(result.problematic_claims)}):")
        for claim in result.problematic_claims:
            print(f"  • {claim}")
        
        print(f"\n🔬 Observations ({len(result.observations)}):")
        for obs in result.observations:
            print(f"  • {obs}")
        
        print(f"\n📋 AI Summary:")
        print(f"  {result.summary}")
        
        print("\n" + "=" * 50)
        print("✨ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check that .env file exists with GOOGLE_API_KEY")
        print("2. Verify API key is valid at https://makersuite.google.com/app/apikey")
        print("3. Ensure internet connection is available")

if __name__ == "__main__":
    test_formulation_analysis()
