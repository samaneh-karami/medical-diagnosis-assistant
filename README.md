# Medical Diagnosis Assistant

A Python-based command-line tool that analyzes user-reported symptoms,
suggests possible diagnoses, and provides general treatment and
medication information by disease name.

## Features

- **Symptom-based diagnosis** — enter a list of symptoms and get ranked
  disease matches based on how closely they align with each condition's
  known symptom profile.
- **Disease lookup** — search by disease name (with fuzzy matching for
  typos) to view its description, common symptoms, suggested treatments,
  and general medication info.
- **Local database** — all data is stored in a lightweight SQLite
  database (`data/medical_data.db`), built automatically on first run.
- **No external dependencies** — built entirely with the Python
  standard library (`sqlite3`, `difflib`).

## Project Structure

```
medical-diagnosis-assistant/
├── main.py          # CLI entry point and menu logic
├── diagnosis.py      # Symptom matching and disease lookup logic
├── database.py       # Database schema + seed data
├── data/              # SQLite database (auto-generated, gitignored)
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
```bash
git clone https://github.com/<your-username>/medical-diagnosis-assistant.git
cd medical-diagnosis-assistant
python main.py
```

The database is created automatically the first time you run the app.
To force a fresh rebuild of the database at any point:
```bash
python database.py
```

## Usage

Run `main.py` and choose from the menu:

1. **Diagnose based on symptoms** — type a comma-separated list of
   symptoms (e.g. `fever, cough, fatigue`) and view ranked possible
   conditions.
2. **Look up treatment & medication info by disease name** — type a
   disease name (e.g. `Migraine`) to see its full profile.
3. **View full list of diseases** in the database.
4. **View full list of known symptoms** in the database.

### Example

```
Enter your symptoms separated by commas (e.g. fever, cough, fatigue).
> fever, headache, muscle pain, chills

Top 3 possible matches based on your symptoms:

  1. Influenza (Flu)  (match score: 71.4%)
     Matched symptoms: chills, fever, headache, muscle aches
  2. Malaria  (match score: 66.7%)
     Matched symptoms: chills, fever, headache, muscle pain
  3. Dengue Fever  (match score: 50.0%)
     Matched symptoms: fever, headache, muscle pain
```

## How the Matching Works

Each disease has a defined set of associated symptoms. When a user
enters their symptoms, the tool calculates a match score for every
disease in the database:

```
score = (number of matched symptoms / total symptoms for that disease) × 100
```

Results are ranked from highest to lowest score, and the top matches
are presented to the user.

## Disclaimer

This project is intended for **educational and portfolio purposes
only**. It is a simplified rule-based tool and is **not a substitute
for professional medical advice, diagnosis, or treatment**. Always
consult a qualified healthcare provider for any medical concerns.

## Possible Future Improvements

- Add a machine learning classifier trained on a larger symptom dataset
- Build a web interface (Flask) or GUI (Tkinter)
- Add weighted symptom importance (some symptoms are more diagnostic than others)
- Expand the database with more conditions and multilingual support

## License

MIT License — feel free to use this project as a reference or starting
point for your own work.
