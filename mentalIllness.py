import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Knowledge base
rules = {
    "possible_depression": {
        "symptoms": ["lack_of_interest", "trouble_sleeping", "feeling_tired"],
        "advice": "Consider consulting a therapist. Daily exercise, healthy sleep, and talking to someone may help."
    },
    "possible_anxiety": {
        "symptoms": ["fast_heartbeat", "short_breath", "constant_worry"],
        "advice": "Practice breathing exercises and mindfulness. Seek help if symptoms persist."
    },
    "possible_burnout": {
        "symptoms": ["work_overload", "lack_of_motivation", "mental_exhaustion"],
        "advice": "Take time off, reduce workload, and recharge mentally."
    },
    "possible_insomnia": {
        "symptoms": ["trouble_sleeping", "restless_thoughts", "fatigue"],
        "advice": "Create a sleep routine. Avoid caffeine and screen time before bed."
    }
}

# Shared functions
def infer_conditions(user_symptoms):
    results = []
    for condition, data in rules.items():
        matched = set(data["symptoms"]).intersection(user_symptoms)
        confidence = int((len(matched) / len(data["symptoms"])) * 100)
        if confidence >= 50:
            results.append({
                "condition": condition,
                "confidence": confidence,
                "advice": data["advice"],
                "matched_symptoms": list(matched)
            })
    return results

def save_report(user_symptoms, results):
    filename = f"mental_health_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as file:
        file.write("Mental Health Diagnosis Report\n")
        file.write("="*40 + "\n")
        file.write(f"Date: {datetime.datetime.now()}\n\n")
        file.write(f"User Symptoms: {', '.join(user_symptoms)}\n\n")

        if results:
            for res in results:
                file.write(f"Condition: {res['condition'].replace('_', ' ').title()}\n")
                file.write(f"Confidence: {res['confidence']}%\n")
                file.write(f"Advice: {res['advice']}\n")
                file.write(f"Matched Symptoms: {', '.join(res['matched_symptoms'])}\n")
                file.write("-"*40 + "\n")
        else:
            file.write("No strong matches found. Please monitor symptoms or consult a doctor.\n")
    return filename

# Terminal version
def run_terminal_mode():
    print("\n🧠 Welcome to the Mental Health Advisor Expert System 🧠")
    print("Please answer with 'yes' or 'no'.\n")

    symptom_list = set()
    for rule in rules.values():
        symptom_list.update(rule["symptoms"])

    user_symptoms = set()
    for symptom in sorted(symptom_list):
        response = input(f"Do you experience '{symptom.replace('_', ' ')}'? ").strip().lower()
        if response == 'yes':
            user_symptoms.add(symptom)

    results = infer_conditions(user_symptoms)

    print("\n🩺 Diagnosis Result:")
    if results:
        for res in results:
            print(f"\n→ {res['condition'].replace('_', ' ').title()} ({res['confidence']}% match)")
            print(f"✓ Advice: {res['advice']}")
    else:
        print("→ No major condition matched. Consider seeking professional help if symptoms continue.")

    print("\n📝 Summary:")
    print(f"You reported: {', '.join(user_symptoms)}")

    save_report(user_symptoms, results)
    print("📁 Diagnosis report saved.\n")

# GUI version
def run_gui_mode():
    symptom_list = sorted({symptom for rule in rules.values() for symptom in rule["symptoms"]})

    def show_visualization(results):
        if not results:
            messagebox.showinfo("Visualization", "No significant conditions detected to visualize.")
            return

        conditions = [r['condition'].replace('_', ' ').title() for r in results]
        confidences = [r['confidence'] for r in results]

        plt.figure(figsize=(8, 5))
        bars = plt.bar(conditions, confidences, color='skyblue')
        plt.title("Confidence Levels of Possible Mental Conditions")
        plt.xlabel("Mental Health Condition")
        plt.ylabel("Confidence (%)")
        plt.ylim(0, 100)

        for bar, confidence in zip(bars, confidences):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{confidence}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.show()

    def analyze():
        selected_symptoms = {symptom for symptom, var in symptom_vars.items() if var.get() == 1}

        if not selected_symptoms:
            messagebox.showwarning("Input Error", "Please select at least one symptom.")
            return

        results = infer_conditions(selected_symptoms)

        if results:
            result_text = ""
            for res in results:
                result_text += (f"{res['condition'].replace('_', ' ').title()} ({res['confidence']}% match):\n"
                                f"Advice: {res['advice']}\n\n")
        else:
            result_text = "No major condition matched.\nConsider seeking professional help if symptoms continue."

        messagebox.showinfo("Diagnosis Result", result_text)
        show_visualization(results)

        filename = save_report(selected_symptoms, results)
        messagebox.showinfo("Report Saved", f"Diagnosis report saved as:\n{filename}")

    root = tk.Tk()
    root.title("Mental Health Advisor Expert System")

    tk.Label(root, text="Select the symptoms you experience:", font=("Arial", 14)).pack(pady=10)
    frame = tk.Frame(root)
    frame.pack(padx=20)

    symptom_vars = {}
    for symptom in symptom_list:
        var = tk.IntVar()
        chk = tk.Checkbutton(frame, text=symptom.replace('_', ' ').title(), variable=var, font=("Arial", 12))
        chk.pack(anchor='w')
        symptom_vars[symptom] = var

    btn = tk.Button(root, text="Analyze Symptoms", command=analyze, font=("Arial", 14), bg="skyblue")
    btn.pack(pady=15)

    root.mainloop()

# Program entry
def main():
    print("Select mode:\n1. Terminal\n2. GUI")
    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        run_terminal_mode()
    elif choice == '2':
        run_gui_mode()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
