"""
diagnosis.py

Core logic for the Medical Diagnosis Assistant:
- matching a list of reported symptoms against the database
- looking up full details (description, treatments, medications) for a disease
- fuzzy-matching disease names so small typos still work
"""

import sqlite3
import difflib
from database import DB_PATH, create_database


def get_connection() -> sqlite3.Connection:
    create_database()  # no-op if the DB already exists
    return sqlite3.connect(DB_PATH)


def list_all_symptoms() -> list:
    """Return a sorted list of every known symptom name."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM symptoms ORDER BY name")
    symptoms = [row[0] for row in cur.fetchall()]
    conn.close()
    return symptoms


def list_all_diseases() -> list:
    """Return a sorted list of every known disease name."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM diseases ORDER BY name")
    diseases = [row[0] for row in cur.fetchall()]
    conn.close()
    return diseases


def match_symptoms(reported_symptoms: list, top_n: int = 5) -> list:
    """
    Compare a list of user-reported symptoms against every disease's
    symptom profile and return the closest matches.

    Returns a list of dicts, sorted by match score (highest first):
        {
            "disease": str,
            "score": float,        # 0-100, how well the disease's
                                    # known symptoms are covered
            "matched_symptoms": list,
            "total_symptoms": int,
        }
    """
    reported = {s.strip().lower() for s in reported_symptoms if s.strip()}
    if not reported:
        return []

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, description FROM diseases")
    diseases = cur.fetchall()

    results = []
    for disease_id, name, _description in diseases:
        cur.execute(
            """
            SELECT s.name FROM symptoms s
            JOIN disease_symptoms ds ON ds.symptom_id = s.id
            WHERE ds.disease_id = ?
            """,
            (disease_id,),
        )
        disease_symptoms = {row[0] for row in cur.fetchall()}

        matched = reported & disease_symptoms
        if not matched:
            continue

        score = (len(matched) / len(disease_symptoms)) * 100

        results.append(
            {
                "disease": name,
                "score": round(score, 1),
                "matched_symptoms": sorted(matched),
                "total_symptoms": len(disease_symptoms),
            }
        )

    conn.close()
    results.sort(key=lambda r: (r["score"], len(r["matched_symptoms"])), reverse=True)
    return results[:top_n]


def find_closest_disease_name(query: str) -> str:
    """Fuzzy-match a user-typed disease name against known diseases."""
    known = list_all_diseases()
    matches = difflib.get_close_matches(query, known, n=1, cutoff=0.4)
    return matches[0] if matches else None


def get_disease_details(disease_name: str) -> dict:
    """
    Return full details for a disease: description, symptoms,
    treatments, and medication info. Returns None if no reasonable
    match is found.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, description FROM diseases WHERE name = ? COLLATE NOCASE", (disease_name,))
    row = cur.fetchone()

    if row is None:
        closest = find_closest_disease_name(disease_name)
        if closest is None:
            conn.close()
            return None
        cur.execute("SELECT id, name, description FROM diseases WHERE name = ?", (closest,))
        row = cur.fetchone()

    disease_id, name, description = row

    cur.execute(
        """
        SELECT s.name FROM symptoms s
        JOIN disease_symptoms ds ON ds.symptom_id = s.id
        WHERE ds.disease_id = ?
        ORDER BY s.name
        """,
        (disease_id,),
    )
    symptoms = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT treatment FROM treatments WHERE disease_id = ?", (disease_id,))
    treatments = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT medication, notes FROM medications WHERE disease_id = ?", (disease_id,))
    medications = [{"medication": r[0], "notes": r[1]} for r in cur.fetchall()]

    conn.close()

    return {
        "name": name,
        "description": description,
        "symptoms": symptoms,
        "treatments": treatments,
        "medications": medications,
    }
