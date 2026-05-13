# 📖 Usage Guide - Nutraceutical AI Reviewer

## Overview

The Nutraceutical Formulation AI Reviewer is an intelligent tool that analyzes supplement products using:
- **LLM Reasoning** for structured analysis
- **Embeddings** for semantic understanding
- **Vector Search** for ingredient discovery

## Main Workflow

```
1. Enter Product Details
   ↓
2. Analyze with AI
   ↓
3. Review Results
   ↓
4. Search Similar Ingredients
```

## Feature Walkthrough

### 1. Formulation Analysis Tab

#### Input Section (Left Panel)

**Product Name**
- Enter the supplement brand/product name
- Example: "PowerBoost Pre-Workout Elite"
- Used for labeling results and vector search metadata

**Category**
- Select from dropdown:
  - Pre-Workout
  - Post-Workout
  - Sleep Support
  - Energy
  - Immune Support
  - Muscle Building
  - Recovery
  - Other
- Helps organize and categorize the analysis

**Ingredient List with Dosage**
- Format: One ingredient per line
- Include dosage units (mg, g, mcg, etc.)
- Example:
  ```
  Caffeine Anhydrous - 400mg
  L-Citrulline Malate - 8g
  Beta-Alanine - 5g
  ```

**Marketing Claims**
- Enter promotional claims from product label
- One claim per line
- System will identify misleading/problematic claims
- Example:
  ```
  Increases muscle growth by 50%
  Guaranteed to work
  100% safe for everyone
  ```

**Analyze Formulation Button**
- Click to run AI analysis
- Takes 30-60 seconds
- Shows spinning indicator during processing

#### Output Section (Right Panel)

Once analysis completes, you'll see:

**📋 Summary**
- AI-generated overview of the formulation
- Key findings and overall assessment
- Recommendations if any

**🧪 Extracted Ingredients**
- Table of all identified ingredients
- Exact dosages as recognized by AI
- Helps verify correct parsing

**⚠️ Safety Check**
- Ingredient-by-ingredient safety analysis
- Compared against reference database
- Green (✓) = Within safe range
- Red (🚨) = Exceeds recommended max
- Orange (❓) = Not in reference DB

**⚠️ Risky Dosages / Flags**
- Specific safety concerns
- High-dose ingredients
- Potential interactions
- Click to expand for details

**🚨 Problematic Claims**
- Marketing claims flagged as misleading
- Explains why each claim is problematic
- Reference to regulatory guidelines

**🔬 Scientific Observations**
- Evidence-based insights
- Formulation notes
- Synergistic ingredients
- Potential concerns

### 2. Ingredient Search Tab

#### How Vector Search Works

The system uses AI embeddings to find ingredients semantically similar to your search query.

**Example Queries and Results:**

| Query | Results |
|-------|---------|
| "sleep support" | Magnesium, L-Theanine, Melatonin, Valerian |
| "energy boost" | Caffeine, Taurine, B-Vitamins, Ginseng |
| "muscle recovery" | Creatine, BCAAs, Zinc, Protein |
| "focus and concentration" | L-Theanine, Caffeine, Choline, Ginkgo |

**To Search:**
1. Switch to "🔍 Ingredient Search" tab
2. Enter your search query
3. Click "Search" button
4. View results with metadata (dosage, product, category)

**Results Include:**
- Ingredient name
- Dosage from analyzed products
- Product name it came from
- Product category

### 3. Sidebar Information

- **About This Tool**: Overview of capabilities
- **How to Use**: Quick reference
- **Disclaimer**: Important legal notice
- **Example Queries**: Suggested searches

## Best Practices

### ✅ Good Practices

1. **Accurate Data Entry**
   - Use exact product information
   - Include all active ingredients
   - Use official dosage units

2. **Complete Claims**
   - Enter all marketing claims on packaging
   - Include promises from ads
   - Note any medical-style claims

3. **Clear Formatting**
   - One ingredient per line
   - Consistent dosage format
   - Use standard abbreviations (mg, g, mcg)

4. **Realistic Expectations**
   - Tool provides educational analysis
   - Not medical advice
   - Always verify with professionals

### ❌ Things to Avoid

1. **Incomplete Data**
   - Don't omit ingredients
   - Don't guess dosages
   - Don't skip active ingredients

2. **Unformatted Input**
   - Avoid unclear abbreviations
   - Don't mix formats
   - Avoid generic descriptions

3. **Medical Decisions**
   - Don't use as sole decision maker
   - Don't ignore professional advice
   - Don't self-diagnose based on results

## Understanding Results

### Safety Check Colors

- **✓ Green**: Within recommended daily dose
- **🚨 Red**: Exceeds safety threshold
- **❓ Orange**: Ingredient not in reference DB

### Risk Flags Explained

Common flag types:

| Flag | Meaning | Action |
|------|---------|--------|
| Exceeds max dose | Dosage too high | Reduce or skip ingredient |
| Drug interaction | May conflict with meds | Check with pharmacist |
| Pregnancy concern | Unsafe if pregnant | Pregnant users should avoid |
| Not enough data | Limited safety info | Use with caution |

### Claim Analysis

Problematic claim patterns detected:
- Absolute claims ("100% safe", "guaranteed")
- Medical claims ("cures disease")
- Unsubstantiated promises
- Missing disclaimers

## Troubleshooting

### "No matching ingredients found" in search

**Cause**: Vector database is empty

**Solution**: 
1. Analyze at least one formulation first
2. Click "Analyze Formulation" button
3. Wait for analysis to complete
4. Then try search again

### "API Sync Error" when analyzing

**Cause**: Google API key issue

**Solution**:
1. Check `.env` file has `GOOGLE_API_KEY=...`
2. Verify key is valid (test at makersuite.google.com)
3. Ensure internet connection is active
4. Try again after 10 seconds

### "Vector DB Error" when searching

**Cause**: Database access issue

**Solution**:
1. Check disk space available
2. Restart app: refresh browser
3. Run an analysis to reinitialize DB
4. Check file permissions

### "No analysis results displayed"

**Cause**: Analysis didn't complete

**Solution**:
1. Check spinner finished
2. Look for error messages
3. Check API key validity
4. Try with simpler input first

## Example Workflows

### Workflow 1: Verify a Pre-Workout

```
1. Enter: "Pump XL Pre-Workout"
2. Category: Pre-Workout
3. Ingredients: Copy from label
4. Claims: Copy marketing promises
5. Analyze
6. Review: Are dosages safe?
7. Check: Are claims honest?
```

### Workflow 2: Compare Formulations

```
1. Analyze Product A
2. Note: Key ingredients & dosages
3. Analyze Product B
4. Compare: Which is safer?
5. Search: Find similar ingredients
6. Decide: Based on analysis
```

### Workflow 3: Find Sleep Ingredients

```
1. Analyze any sleep supplement
2. Go to search tab
3. Query: "sleep support"
4. View: Related ingredients
5. Learn: What works for sleep
```

## Frequently Asked Questions

### Q: Is this AI analysis accurate?

A: This tool provides educational analysis using AI/ML. While advanced, it's not medical advice. Always verify with healthcare professionals.

### Q: How is dosage safety determined?

A: Against reference thresholds based on industry guidelines (RDA, established safe upper limits). Individual tolerance varies.

### Q: Can I download the results?

A: Currently no built-in download. Screenshot or copy text as needed. Can export CSV in future versions.

### Q: What ingredients are in the database?

A: See `ingredient_database.py` for ~30 common supplement ingredients. Unlisted ingredients show as "not in reference DB".

### Q: How often is the database updated?

A: Reference database is static. Can be updated by editing `ingredient_database.py`.

### Q: What about side effects?

A: Safety checks cover dosage risks, not individual side effects. Consult a healthcare provider for personal health concerns.

### Q: Is my data saved?

A: No. Data is analyzed in real-time but not permanently stored (except vector DB for search).

## Advanced Usage

### Custom Ingredient Analysis

For unlisted ingredients:
1. Analyze with the product
2. Note AI's assessment in observations
3. Manual research for safety
4. Consult healthcare provider

### Search Tips for Better Results

- Use benefit-focused terms: "energy", "sleep", "muscle"
- Include modifiers: "natural energy", "deep sleep"
- Be specific: "caffeine alternatives" vs just "caffeine"

### Understanding Vector Search

The system doesn't just match keywords - it understands meaning:
- Query: "tiredness support"
- Finds: Caffeine, Ginseng (energy), Iron (fatigue)
- Even if you didn't use exact words

---

**Need help? Check the README.md or DEPLOYMENT.md**
