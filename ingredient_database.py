"""
Reference database for ingredient safety thresholds and categories.
Based on general supplement industry guidelines.
"""

INGREDIENT_SAFETY_DB = {
    "Caffeine Anhydrous": {
        "categories": ["stimulant", "energy", "focus"],
        "max_daily_dose": "400mg",
        "warnings": ["May increase heart rate", "Can cause jitteriness", "Sleep disruption possible"],
        "interactions": ["Blood pressure medications", "Heart conditions"],
    },
    "Beta-Alanine": {
        "categories": ["performance", "endurance", "muscle"],
        "max_daily_dose": "6g",
        "warnings": ["May cause tingling sensation", "Avoid if pregnant"],
        "interactions": ["None major"],
    },
    "Creatine Monohydrate": {
        "categories": ["performance", "muscle", "strength"],
        "max_daily_dose": "5g",
        "warnings": ["May increase water retention", "Ensure adequate hydration"],
        "interactions": ["Kidney conditions"],
    },
    "Taurine": {
        "categories": ["energy", "performance", "cardiovascular"],
        "max_daily_dose": "3g",
        "warnings": ["Generally safe", "Excessive amounts may affect liver"],
        "interactions": ["None major"],
    },
    "L-Theanine": {
        "categories": ["relaxation", "focus", "sleep"],
        "max_daily_dose": "200mg",
        "warnings": ["May cause drowsiness", "Avoid if allergic to tea"],
        "interactions": ["Stimulants can be balanced with L-Theanine"],
    },
    "Magnesium": {
        "categories": ["relaxation", "sleep", "muscle"],
        "max_daily_dose": "400mg",
        "warnings": ["May have laxative effect", "Take with food"],
        "interactions": ["Certain antibiotics", "Bisphosphonates"],
    },
    "Melatonin": {
        "categories": ["sleep", "rest"],
        "max_daily_dose": "10mg",
        "warnings": ["May cause grogginess", "Avoid long-term use without medical advice"],
        "interactions": ["Sedatives", "Blood thinners"],
    },
    "Vitamin C": {
        "categories": ["immune", "antioxidant"],
        "max_daily_dose": "2000mg",
        "warnings": ["May cause diarrhea at high doses"],
        "interactions": ["Can increase iron absorption"],
    },
    "Zinc": {
        "categories": ["immune", "recovery"],
        "max_daily_dose": "40mg",
        "warnings": ["May cause nausea", "Zinc lozenges may affect taste"],
        "interactions": ["Copper absorption", "Antibiotics"],
    },
    "Iron": {
        "categories": ["energy", "recovery"],
        "max_daily_dose": "18mg",
        "warnings": ["Can cause constipation", "May stain teeth"],
        "interactions": ["Tea and coffee reduce absorption"],
    },
}

PROBLEMATIC_CLAIMS = [
    "cures",
    "guaranteed",
    "FDA approved",
    "100% safe",
    "forever",
    "instantly",
    "miracle",
    "approved by doctors",
    "clinically proven without data",
    "works for everyone",
]

def check_ingredient_safety(ingredient_name: str, dosage_str: str) -> dict:
    """Check if an ingredient and dosage are within safe limits."""
    if ingredient_name not in INGREDIENT_SAFETY_DB:
        return {"safe": None, "message": "Ingredient not in reference database"}
    
    info = INGREDIENT_SAFETY_DB[ingredient_name]
    
    # Extract numeric dosage (simple parsing)
    try:
        import re
        dosage_value = re.search(r'(\d+(?:\.\d+)?)', dosage_str)
        if dosage_value:
            dosage_value = float(dosage_value.group(1))
            max_dose_str = info["max_daily_dose"]
            max_dose = float(re.search(r'(\d+(?:\.\d+)?)', max_dose_str).group(1))
            
            if dosage_value > max_dose:
                return {
                    "safe": False,
                    "message": f"Dosage {dosage_str} exceeds recommended max of {max_dose_str}",
                    "warnings": info["warnings"],
                }
    except Exception:
        pass
    
    return {
        "safe": True,
        "message": f"{ingredient_name} at {dosage_str} appears within normal range",
        "warnings": info["warnings"],
    }
