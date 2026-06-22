"""
main.py

Medical Diagnosis Assistant
----------------------------
A simple command-line tool that:
  1. Suggests possible diagnoses based on reported symptoms
  2. Looks up treatment and medication info by disease name
  3. Lists every disease in the database

DISCLAIMER: This tool is for educational / portfolio demonstration
purposes only. It is NOT a substitute for professional medical advice,
diagnosis, or treatment. Always consult a qualified healthcare provider
for any medical concerns.
"""

import sys
from diagnosis import (
    match_symptoms,
    get_disease_details,
    list_all_diseases,
    list_all_symptoms,
)

DISCLAIMER = (
    "=" * 70 + "\n"
    "DISCLAIMER: This tool is for educational/demonstration purposes only.\n"
    "It is NOT a substitute for professional medical advice. Always\n"
    "consult a licensed doctor or pharmacist for real medical concerns.\n"
    + "=" * 70
)


def print_header():
    print("\n" + "=" * 70)
    print("           MEDICAL DIAGNOSIS ASSISTANT".center(70))
    print("=" * 70)


def print_menu():
    print("\nWhat would you like to do?")
    print("  1. Diagnose based on symptoms")
    print("  2. Look up treatment & medication info by disease name")
    print("  3. View full list of diseases in the database")
    print("  4. View full list of known symptoms")
    print("  5. Exit")


def show_disease_details(name: str):
    details = get_disease_details(name)
    if details is None:
        print(f"\nSorry, no information found for '{name}'.")
        return

    print(f"\n--- {details['name']} ---")
    print(f"Description: {details['description']}")

    print("\nCommon symptoms:")
    for s in details["symptoms"]:
        print(f"  - {s}")

    print("\nSuggested treatments:")
    for t in details["treatments"]:
        print(f"  - {t}")

    print("\nMedication info:")
    for m in details["medications"]:
        print(f"  - {m['medication']}: {m['notes']}")

    print(f"\n{DISCLAIMER}")


def handle_diagnose():
    print("\nEnter your symptoms separated by commas (e.g. fever, cough, fatigue).")
    print("Type 'list' to see all known symptoms.")
    raw = input("> ").strip()

    if raw.lower() == "list":
        symptoms = list_all_symptoms()
        print("\nKnown symptoms:")
        for s in symptoms:
            print(f"  - {s}")
        return

    reported = [s.strip() for s in raw.split(",") if s.strip()]
    if not reported:
        print("No symptoms entered.")
        return

    matches = match_symptoms(reported)

    if not matches:
        print("\nNo close matches found. Try different or fewer symptoms,")
        print("or type 'list' to see exactly how symptoms are named in the database.")
        return

    print(f"\nTop {len(matches)} possible matches based on your symptoms:\n")
    for i, m in enumerate(matches, start=1):
        print(f"  {i}. {m['disease']}  (match score: {m['score']}%)")
        print(f"     Matched symptoms: {', '.join(m['matched_symptoms'])}")

    choice = input(
        "\nEnter a number to see full details, or press Enter to go back: "
    ).strip()

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(matches):
            show_disease_details(matches[idx]["disease"])
        else:
            print("Invalid selection.")


def handle_lookup_by_name():
    name = input("\nEnter a disease name to look up: ").strip()
    if not name:
        print("No disease name entered.")
        return
    show_disease_details(name)


def handle_list_diseases():
    diseases = list_all_diseases()
    print(f"\n{len(diseases)} diseases currently in the database:\n")
    for d in diseases:
        print(f"  - {d}")


def handle_list_symptoms():
    symptoms = list_all_symptoms()
    print(f"\n{len(symptoms)} known symptoms in the database:\n")
    for s in symptoms:
        print(f"  - {s}")


def main():
    print_header()
    print(DISCLAIMER)

    while True:
        print_menu()
        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            handle_diagnose()
        elif choice == "2":
            handle_lookup_by_name()
        elif choice == "3":
            handle_list_diseases()
        elif choice == "4":
            handle_list_symptoms()
        elif choice == "5":
            print("\nGoodbye! Stay healthy.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
