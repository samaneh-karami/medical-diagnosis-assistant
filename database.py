"""
database.py

Handles creation and seeding of the SQLite database used by the
Medical Diagnosis Assistant. Run this file directly to (re)build
the database from scratch:

    python database.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "medical_data.db")


# ---------------------------------------------------------------------------
# Seed data
#
# NOTE: This information is simplified for demonstration purposes only.
# It is NOT a substitute for professional medical advice, diagnosis, or
# treatment. Medication entries intentionally omit specific dosages -
# always consult a doctor or pharmacist for that.
# ---------------------------------------------------------------------------

DISEASE_DATA = [
    {
        "name": "Common Cold",
        "description": "A mild viral infection of the nose and throat.",
        "symptoms": ["runny nose", "sneezing", "sore throat", "mild cough", "mild fever", "congestion"],
        "treatments": ["Rest and stay hydrated", "Steam inhalation", "Warm salt water gargle", "Use a humidifier"],
        "medications": [
            ("Acetaminophen / Paracetamol", "For mild fever and body aches"),
            ("Decongestant nasal spray", "For nasal congestion, short-term use only"),
            ("Antihistamine", "For runny nose and sneezing"),
        ],
    },
    {
        "name": "Influenza (Flu)",
        "description": "A contagious viral respiratory illness.",
        "symptoms": ["high fever", "chills", "muscle aches", "fatigue", "headache", "dry cough", "sore throat"],
        "treatments": ["Rest and fluids", "Stay home to avoid spreading infection", "Monitor temperature"],
        "medications": [
            ("Antiviral medication", "Most effective if started within 48 hours of symptom onset; prescription required"),
            ("Acetaminophen or Ibuprofen", "For fever and aches"),
        ],
    },
    {
        "name": "COVID-19",
        "description": "A respiratory illness caused by the SARS-CoV-2 virus.",
        "symptoms": ["fever", "dry cough", "fatigue", "loss of taste", "loss of smell", "shortness of breath", "sore throat"],
        "treatments": ["Isolate from others", "Rest and hydration", "Monitor oxygen levels if available", "Seek emergency care for breathing difficulty"],
        "medications": [
            ("Acetaminophen", "For fever and discomfort"),
            ("Antiviral therapy", "Prescribed by a doctor in specific risk cases"),
        ],
    },
    {
        "name": "Migraine",
        "description": "A neurological condition causing intense, recurring headaches.",
        "symptoms": ["throbbing headache", "nausea", "sensitivity to light", "sensitivity to sound", "visual aura"],
        "treatments": ["Rest in a dark, quiet room", "Cold compress on forehead", "Identify and avoid triggers"],
        "medications": [
            ("NSAIDs (e.g., ibuprofen)", "For pain relief at onset"),
            ("Triptans", "Prescription medication for moderate-to-severe migraines"),
        ],
    },
    {
        "name": "Tension Headache",
        "description": "A common headache causing mild to moderate pain, often stress-related.",
        "symptoms": ["dull headache", "tight band feeling around head", "neck stiffness", "fatigue"],
        "treatments": ["Stress management", "Gentle neck stretches", "Adequate sleep"],
        "medications": [
            ("Acetaminophen or NSAIDs", "For pain relief"),
        ],
    },
    {
        "name": "Hypertension",
        "description": "Chronic high blood pressure that can damage blood vessels over time.",
        "symptoms": ["headache", "dizziness", "blurred vision", "shortness of breath", "nosebleeds"],
        "treatments": ["Reduce salt intake", "Regular exercise", "Routine blood pressure monitoring", "Limit alcohol"],
        "medications": [
            ("ACE inhibitors", "Prescription, lowers blood pressure"),
            ("Beta-blockers", "Prescription, reduces heart workload"),
            ("Diuretics", "Prescription, reduces fluid volume"),
        ],
    },
    {
        "name": "Type 2 Diabetes",
        "description": "A chronic condition affecting how the body processes blood sugar.",
        "symptoms": ["frequent urination", "excessive thirst", "fatigue", "blurred vision", "slow-healing sores", "unexplained weight loss"],
        "treatments": ["Dietary changes", "Regular physical activity", "Blood sugar monitoring", "Weight management"],
        "medications": [
            ("Metformin", "Prescription, first-line treatment"),
            ("Insulin therapy", "Prescription, for advanced cases"),
        ],
    },
    {
        "name": "Asthma",
        "description": "A chronic condition causing inflammation and narrowing of airways.",
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing at night"],
        "treatments": ["Avoid known triggers", "Use a peak flow meter", "Keep rescue inhaler accessible"],
        "medications": [
            ("Short-acting bronchodilator (inhaler)", "For quick relief during attacks"),
            ("Inhaled corticosteroids", "For long-term control"),
        ],
    },
    {
        "name": "Bronchitis",
        "description": "Inflammation of the lining of the bronchial tubes.",
        "symptoms": ["persistent cough", "mucus production", "fatigue", "mild fever", "chest discomfort"],
        "treatments": ["Rest", "Stay hydrated", "Use a humidifier", "Avoid smoke and irritants"],
        "medications": [
            ("Cough suppressant", "For dry, non-productive cough"),
            ("Bronchodilator", "If wheezing is present"),
        ],
    },
    {
        "name": "Pneumonia",
        "description": "An infection that inflames the air sacs in one or both lungs.",
        "symptoms": ["fever", "chills", "productive cough", "shortness of breath", "chest pain", "fatigue"],
        "treatments": ["Seek medical evaluation promptly", "Rest and hydration", "Hospitalization if severe"],
        "medications": [
            ("Antibiotics", "Prescription, for bacterial pneumonia"),
            ("Antipyretics", "For fever management"),
        ],
    },
    {
        "name": "Gastroenteritis",
        "description": "Inflammation of the stomach and intestines, often called 'stomach flu'.",
        "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal cramps", "mild fever"],
        "treatments": ["Oral rehydration", "Bland diet (BRAT)", "Rest"],
        "medications": [
            ("Oral rehydration salts", "To prevent dehydration"),
            ("Antiemetic", "For severe nausea, if prescribed"),
        ],
    },
    {
        "name": "Urinary Tract Infection (UTI)",
        "description": "A bacterial infection affecting the urinary system.",
        "symptoms": ["burning urination", "frequent urination", "pelvic pain", "cloudy urine", "strong-smelling urine"],
        "treatments": ["Increase water intake", "Avoid irritants like caffeine", "Complete prescribed treatment course"],
        "medications": [
            ("Antibiotics", "Prescription, specific to infection type"),
            ("Pain reliever (urinary analgesic)", "For discomfort"),
        ],
    },
    {
        "name": "Sinusitis",
        "description": "Inflammation of the sinuses, often following a cold or allergy.",
        "symptoms": ["facial pain", "nasal congestion", "thick nasal discharge", "headache", "reduced sense of smell"],
        "treatments": ["Saline nasal rinse", "Steam inhalation", "Stay hydrated"],
        "medications": [
            ("Decongestant", "Short-term symptom relief"),
            ("Antibiotics", "Only if bacterial infection is confirmed by a doctor"),
        ],
    },
    {
        "name": "Allergic Rhinitis",
        "description": "An allergic response causing inflammation of the nasal passages.",
        "symptoms": ["sneezing", "itchy eyes", "runny nose", "nasal congestion", "watery eyes"],
        "treatments": ["Avoid known allergens", "Use air purifiers", "Keep windows closed during high pollen season"],
        "medications": [
            ("Antihistamine", "For sneezing and itching"),
            ("Nasal corticosteroid spray", "For ongoing congestion"),
        ],
    },
    {
        "name": "Chickenpox",
        "description": "A highly contagious viral infection causing an itchy, blister-like rash.",
        "symptoms": ["itchy rash", "fluid-filled blisters", "fever", "fatigue", "loss of appetite"],
        "treatments": ["Avoid scratching", "Cool baths with baking soda or oatmeal", "Isolate to prevent spread"],
        "medications": [
            ("Calamine lotion", "To soothe itching"),
            ("Antihistamine", "For itch relief"),
            ("Antiviral medication", "For high-risk individuals, prescribed by a doctor"),
        ],
    },
    {
        "name": "Measles",
        "description": "A highly contagious viral infection affecting the respiratory system.",
        "symptoms": ["high fever", "cough", "runny nose", "red watery eyes", "skin rash"],
        "treatments": ["Rest and isolation", "Hydration", "Vitamin A supplementation in some cases"],
        "medications": [
            ("Acetaminophen", "For fever reduction"),
        ],
    },
    {
        "name": "Malaria",
        "description": "A mosquito-borne infectious disease caused by parasites.",
        "symptoms": ["high fever", "chills", "sweating", "headache", "nausea", "muscle pain"],
        "treatments": ["Seek immediate medical care", "Use mosquito nets and repellents to prevent reinfection"],
        "medications": [
            ("Antimalarial medication", "Prescription, specific to parasite type and region"),
        ],
    },
    {
        "name": "Dengue Fever",
        "description": "A mosquito-borne viral infection common in tropical regions.",
        "symptoms": ["high fever", "severe headache", "joint pain", "muscle pain", "skin rash", "nausea"],
        "treatments": ["Rest and hydration", "Monitor for warning signs of severe dengue", "Avoid NSAIDs (risk of bleeding)"],
        "medications": [
            ("Acetaminophen", "For fever and pain - avoid aspirin and ibuprofen"),
        ],
    },
    {
        "name": "Tuberculosis",
        "description": "A bacterial infection that primarily affects the lungs.",
        "symptoms": ["persistent cough", "coughing up blood", "night sweats", "weight loss", "fatigue", "chest pain"],
        "treatments": ["Complete the full course of prescribed treatment", "Isolation during infectious period", "Regular medical follow-up"],
        "medications": [
            ("Combination antibiotic therapy", "Prescription, long-term multi-drug regimen"),
        ],
    },
    {
        "name": "Iron-Deficiency Anemia",
        "description": "A condition caused by insufficient healthy red blood cells due to low iron.",
        "symptoms": ["fatigue", "pale skin", "shortness of breath", "dizziness", "cold hands and feet"],
        "treatments": ["Iron-rich diet", "Address underlying cause of blood loss if present"],
        "medications": [
            ("Iron supplements", "As recommended by a doctor"),
        ],
    },
    {
        "name": "Hypothyroidism",
        "description": "A condition where the thyroid gland doesn't produce enough hormone.",
        "symptoms": ["fatigue", "weight gain", "cold intolerance", "dry skin", "hair loss", "depression"],
        "treatments": ["Routine thyroid function monitoring", "Consistent medication schedule"],
        "medications": [
            ("Levothyroxine", "Prescription hormone replacement therapy"),
        ],
    },
    {
        "name": "GERD (Acid Reflux)",
        "description": "A digestive disorder where stomach acid frequently flows back into the esophagus.",
        "symptoms": ["heartburn", "regurgitation", "chest discomfort", "difficulty swallowing", "chronic cough"],
        "treatments": ["Avoid trigger foods", "Eat smaller meals", "Avoid lying down after eating", "Elevate head while sleeping"],
        "medications": [
            ("Antacids", "For occasional symptom relief"),
            ("Proton pump inhibitors", "For frequent or chronic symptoms"),
        ],
    },
    {
        "name": "Conjunctivitis (Pink Eye)",
        "description": "Inflammation of the membrane covering the eye, often due to infection or allergy.",
        "symptoms": ["red eyes", "itchy eyes", "watery eyes", "eye discharge", "gritty feeling in eye"],
        "treatments": ["Avoid touching or rubbing eyes", "Warm or cool compress", "Wash hands frequently to prevent spread"],
        "medications": [
            ("Antibiotic eye drops", "Prescription, for bacterial conjunctivitis"),
            ("Antihistamine eye drops", "For allergic conjunctivitis"),
        ],
    },
    {
        "name": "Generalized Anxiety Disorder",
        "description": "A mental health condition characterized by persistent, excessive worry.",
        "symptoms": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "muscle tension", "sleep disturbance"],
        "treatments": ["Cognitive behavioral therapy", "Relaxation techniques", "Regular exercise", "Consistent sleep schedule"],
        "medications": [
            ("SSRIs", "Prescription, commonly used for long-term management"),
            ("Short-term anti-anxiety medication", "Prescription, used cautiously under medical supervision"),
        ],
    },
]


def create_database(force_rebuild: bool = False) -> None:
    """Create and seed the SQLite database.

    If the database file already exists and force_rebuild is False,
    this function does nothing (so re-running the app doesn't wipe data).
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH) and not force_rebuild:
        return

    if os.path.exists(DB_PATH) and force_rebuild:
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );

        CREATE TABLE symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE disease_symptoms (
            disease_id INTEGER NOT NULL,
            symptom_id INTEGER NOT NULL,
            FOREIGN KEY (disease_id) REFERENCES diseases (id),
            FOREIGN KEY (symptom_id) REFERENCES symptoms (id)
        );

        CREATE TABLE treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id INTEGER NOT NULL,
            treatment TEXT NOT NULL,
            FOREIGN KEY (disease_id) REFERENCES diseases (id)
        );

        CREATE TABLE medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id INTEGER NOT NULL,
            medication TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (disease_id) REFERENCES diseases (id)
        );
        """
    )

    symptom_id_cache = {}

    def get_or_create_symptom(name: str) -> int:
        name = name.strip().lower()
        if name in symptom_id_cache:
            return symptom_id_cache[name]
        cur.execute("INSERT OR IGNORE INTO symptoms (name) VALUES (?)", (name,))
        cur.execute("SELECT id FROM symptoms WHERE name = ?", (name,))
        symptom_id = cur.fetchone()[0]
        symptom_id_cache[name] = symptom_id
        return symptom_id

    for disease in DISEASE_DATA:
        cur.execute(
            "INSERT INTO diseases (name, description) VALUES (?, ?)",
            (disease["name"], disease["description"]),
        )
        disease_id = cur.lastrowid

        for symptom in disease["symptoms"]:
            symptom_id = get_or_create_symptom(symptom)
            cur.execute(
                "INSERT INTO disease_symptoms (disease_id, symptom_id) VALUES (?, ?)",
                (disease_id, symptom_id),
            )

        for treatment in disease["treatments"]:
            cur.execute(
                "INSERT INTO treatments (disease_id, treatment) VALUES (?, ?)",
                (disease_id, treatment),
            )

        for medication, notes in disease["medications"]:
            cur.execute(
                "INSERT INTO medications (disease_id, medication, notes) VALUES (?, ?, ?)",
                (disease_id, medication, notes),
            )

    conn.commit()
    conn.close()
    print(f"Database created and seeded at: {DB_PATH}")


if __name__ == "__main__":
    create_database(force_rebuild=True)
