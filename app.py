from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import pickle
import joblib
import pandas as pd
import random
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"

# enable server logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# ---------- Load Model & Features ----------
try:
    with open("stackedd_model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception:
    model = joblib.load("stackedd_model.pkl")

with open("column_order.pkl", "rb") as f:
    model_features = pickle.load(f)

# ---------- Helper Functions ----------
def clamp_score(x):
    return max(0, min(100, round(x, 0)))


def rescale_score(raw, min_val=40):
    """Rescale scores so they stay between min_val and 100."""
    return max(min_val, min(100, int(min_val + (raw * (100 - min_val) / 100))))


def bucket_label(score):
    thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for t in thresholds:
        if score < t:
            return f"<{t}"
    return "<100"


def score_category(score):
    if score >= 80:
        return "🌟 Excellent"
    elif score >= 60:
        return "👍 Good"
    elif score >= 40:
        return "🙂 Fair"
    else:
        return "⚠️ Needs Improvement"


def lifestyle_category(score):
    """Higher = worse lifestyle impact. Lower = healthier."""
    if score <= 20:
        return "🌟 Low Impact (Healthy Lifestyle)"
    elif score <= 40:
        return "🙂 Moderate Impact"
    elif score <= 70:
        return "⚠️ Concerning Impact"
    else:
        return "🚨 High Negative Impact"


def calculate_memory_score(form, session):
    attempts = int(session.get("MemoryGame_Attempts", 0))
    if attempts <= 0:
        raw = 0
    else:
        raw = 100 - (attempts - 1) * 5

    if form.get("MMSE_Normal Cognitive Function") == "TRUE":
        raw += 10
    if form.get("MMSE_Moderate Impairment") == "TRUE":
        raw -= 20
    if form.get("MMSE_Severe Impairment") == "TRUE":
        raw -= 40
    if form.get("Forgetfulness_Yes") == "TRUE":
        raw -= 15
    if form.get("MemoryComplaints") == "1":
        raw -= 10

    return rescale_score(raw)


def calculate_reaction_score(session, form):
    avg = float(session.get("ReactionGame_FinalAvg", 0.0))
    if avg <= 0:
        raw = 0
    else:
        raw = 100 * (1500 - avg) / (1500 - 300)

    if form.get("Confusion_Yes") == "TRUE":
        raw -= 10
    if form.get("Disorientation_Yes") == "TRUE":
        raw -= 10

    return rescale_score(raw)


def calculate_lifestyle_score(form):
    """Return a score where higher = worse lifestyle (higher Alzheimer's impact)."""
    raw = 0
    if form.get("Smoking") == "1":
        raw += 15
    if form.get("AlcoholConsumption") == "1":
        raw += 10
    if form.get("PhysicalActivity") == "0":
        raw += 15
    if form.get("DietQuality") == "0":
        raw += 15
    if form.get("SleepQuality") == "0":
        raw += 10
    if form.get("Depression") == "1":
        raw += 15
    if form.get("DifficultyCompletingTasks") == "3":
        raw += 10
    if form.get("MemoryComplaints") == "1":
        raw += 10

    return clamp_score(raw)


def _convert_value_for_model(val):
    """Convert various string forms to numeric values model expects."""
    if val is None or val == "":
        return 0
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ("true", "t", "1", "yes", "y"):
            return 1
        if v in ("false", "f", "0", "no", "n"):
            return 0
    try:
        return float(val)
    except Exception:
        return 0


# ---------- Recommendations ----------
def generate_recommendations(memory, reaction, lifestyle, form, prediction):
    categories = {
        "Lifestyle & Habits": [],
        "Medical & Health": [],
        "Cognitive & Memory": [],
        "Biometric & Vitals": [],
        "General Positives": []
    }

    cholesterol_suggestions = [
        "Eat nuts, olive oil, and fish to boost healthy fats.",
        "Include avocados, seeds, and salmon to raise HDL cholesterol.",
        "Switch from fried food to grilled options for better cholesterol control."
    ]
    memory_exercises = [
        "Practice journaling daily to strengthen recall.",
        "Play puzzle or memory games for 20 minutes daily.",
        "Try storytelling exercises to improve memory retention."
    ]
    social_activities = [
        "Engage in group hobbies like book clubs or gardening.",
        "Have regular conversations with friends or family.",
        "Join a community class to stay socially connected."
    ]

    # Lifestyle
    if form.get("Smoking") == "1":
        categories["Lifestyle & Habits"].append("Quit smoking completely. Consider therapy or counseling.")
    if form.get("AlcoholConsumption") == "1":
        categories["Lifestyle & Habits"].append("Reduce or stop alcohol consumption. Replace with non-alcoholic alternatives.")
    if form.get("PhysicalActivity") == "0":
        categories["Lifestyle & Habits"].append("Engage in at least 30 minutes of daily physical activity.")
    if form.get("SleepQuality") == "0":
        categories["Lifestyle & Habits"].append("Improve sleep hygiene: 7–8 hours, reduce screen time before bed.")
    if form.get("DietQuality") == "0":
        categories["Lifestyle & Habits"].append("Adopt a Mediterranean diet rich in vegetables, fish, and whole grains.")

    # Medical
    if form.get("Diabetes") == "1":
        categories["Medical & Health"].append("Monitor blood sugar with a low-GI diet and regular checkups.")
    if form.get("CardiovascularDisease") == "1":
        categories["Medical & Health"].append("Protect heart health: reduce saturated fats, follow doctor guidance.")
    if form.get("Hypertension") == "1":
        categories["Medical & Health"].append("Control blood pressure with a low-salt diet and meditation.")
    if form.get("Depression") == "1":
        categories["Medical & Health"].append("Seek counseling or therapy to improve mood.")

    # Cognitive
    if form.get("MemoryComplaints") == "1":
        categories["Cognitive & Memory"].append(random.choice(memory_exercises))
    if form.get("Forgetfulness_Yes") == "TRUE":
        categories["Cognitive & Memory"].append("Use reminders and structured routines to reduce forgetfulness.")
    if form.get("MMSE_Severe Impairment") == "TRUE":
        categories["Cognitive & Memory"].append("Schedule neurological assessments and seek specialist support.")
    if form.get("BehavioralProblems") == "1":
        categories["Cognitive & Memory"].append("Consider behavioral therapy and caregiver support groups for assistance.")
    if form.get("Disorientation_Yes") == "TRUE" or form.get("Confusion_Yes") == "TRUE":
        categories["Cognitive & Memory"].append("Ensure a safe, supervised home environment with visual cues and reminders.")

    # Biometric
    if form.get("CholesterolTotal") == "2":
        categories["Biometric & Vitals"].append("High total cholesterol. Reduce saturated fats and exercise regularly.")
    if form.get("CholesterolLDL") == "2":
        categories["Biometric & Vitals"].append("High LDL cholesterol. Limit fried foods, increase soluble fiber intake.")
    if form.get("CholesterolHDL") == "0":
        categories["Biometric & Vitals"].append(random.choice(cholesterol_suggestions))
    if form.get("CholesterolTriglycerides") == "3":
        categories["Biometric & Vitals"].append("Very high triglycerides. Strongly reduce sugar, alcohol, and refined carbs.")
    try:
        bmi = float(form.get("BMI", 0))
        if bmi < 18.5:
            categories["Biometric & Vitals"].append("Underweight detected. Increase calorie intake with nutrient-rich foods.")
        elif 25 <= bmi < 30:
            categories["Biometric & Vitals"].append("Overweight detected. Aim for gradual weight loss with portion control.")
        elif bmi >= 30:
            categories["Biometric & Vitals"].append("Obesity detected. Consult a healthcare provider for a structured plan.")
    except:
        pass

    # Risk-specific
    if "Low Risk" in prediction:
        categories["General Positives"].append("Excellent overall health! Maintain your balanced lifestyle.")
    elif "Moderate Risk" in prediction:
        categories["General Positives"].append("Take proactive steps to address lifestyle and medical issues.")
    elif "High Risk" in prediction:
        categories["Medical & Health"].append("⚠️ Seek immediate medical consultation with a neurologist.")
        categories["Medical & Health"].append("⚠️ Consider assisted living or caregiver support if impairments increase.")

        # Fallbacks if blank
        if not categories["Cognitive & Memory"]:
            fallback_cognitive = [
                "⚠️ Enroll in structured memory care programs.",
                "⚠️ Ensure a safe home environment with supervision.",
                "⚠️ Seek caregiver support groups for daily assistance.",
                "⚠️ Establish strict routines to reduce confusion."
            ]
            categories["Cognitive & Memory"].append(random.choice(fallback_cognitive))

        if not categories["Biometric & Vitals"]:
            fallback_biometrics = [
                "⚠️ Regularly monitor blood pressure, sugar, and cholesterol at home.",
                "⚠️ Schedule full body check-ups every 6 months.",
                "⚠️ Ensure proper hydration and nutrition even with cognitive decline."
            ]
            categories["Biometric & Vitals"].append(random.choice(fallback_biometrics))

    # General positives
    categories["General Positives"].append(random.choice(social_activities))

    # Limit to 3 per category
    for cat in categories:
        if len(categories[cat]) > 3:
            categories[cat] = random.sample(categories[cat], 3)

    return categories


def generate_health_story(prediction, mem, react, life, mem_bucket, react_bucket, life_bucket):
    return (
        f"Risk Assessment: {prediction}. "
        f"Memory score: {mem}/100 ({mem_bucket}). "
        f"Reaction score: {react}/100 ({react_bucket}). "
        f"Alzheimer Detection Form score: {life}/100 ({life_bucket}). "
        "This suggests focusing on weaker areas while maintaining strong ones."
    )


def get_progress_class(category, is_lifestyle=False):
    if not is_lifestyle:
        if "Excellent" in category: return "progress-green"
        if "Good" in category: return "progress-yellow"
        if "Fair" in category: return "progress-orange"
        return "progress-red"
    else:
        if "Low Impact" in category: return "progress-green"
        if "Moderate" in category: return "progress-orange"
        if "Concerning" in category: return "progress-redorange"
        return "progress-darkred"

# ---------- Routes ----------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists"
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session.clear()
            session["user"] = username
            session["MemoryGame_Attempts"] = 0
            session["ReactionGame_FinalAvg"] = 0.0
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/reaction_game", methods=["GET", "POST"])
def reaction_game():
    if request.method == "POST":
        final_avg = request.form.get("FinalAvg")
        if final_avg:
            session["ReactionGame_FinalAvg"] = float(final_avg)
        return redirect(url_for("dashboard"))
    return render_template("reaction_game.html")


@app.route("/memory_game", methods=["GET", "POST"])
def memory_game():
    if request.method == "POST":
        attempts = request.form.get("Attempts")
        if attempts:
            session["MemoryGame_Attempts"] = int(attempts)
        return redirect(url_for("dashboard"))
    return render_template("memory_game.html")


@app.route("/save_game_result", methods=["POST"])
def save_game_result():
    data = request.get_json()
    game = data.get("game")

    if game == "reaction":
        score = data.get("final_time", 0)
        session["ReactionGame_FinalAvg"] = float(score)
    elif game == "memory":
        attempts = data.get("attempts", 0)
        session["MemoryGame_Attempts"] = int(attempts)

    return jsonify({"status": "success"})


@app.route("/diagnosis", methods=["GET", "POST"])
def diagnosis():
    if request.method == "POST":
        try:
            form = request.form.to_dict()

            memory_score = calculate_memory_score(form, session)
            reaction_score = calculate_reaction_score(session, form)
            lifestyle_score = calculate_lifestyle_score(form)

            mem_bucket = bucket_label(memory_score)
            react_bucket = bucket_label(reaction_score)
            life_bucket = bucket_label(lifestyle_score)

            input_data = {}
            for field in model_features:
                if field == "MemoryGame_Attempts":
                    input_data[field] = float(session.get("MemoryGame_Attempts", 0))
                elif field == "ReactionGame_FinalAvg":
                    input_data[field] = float(session.get("ReactionGame_FinalAvg", 0.0))
                else:
                    raw_val = form.get(field)
                    input_data[field] = _convert_value_for_model(raw_val)

            df = pd.DataFrame([input_data])
            df = df.reindex(columns=model_features, fill_value=0)

            result = model.predict(df)[0]
            if result == 0:
                prediction = "Low Risk of Alzheimer's"
            elif result == 1:
                prediction = "Moderate Risk of Alzheimer's"
            else:
                prediction = "High Risk of Alzheimer's"

            categories = generate_recommendations(memory_score, reaction_score, lifestyle_score, form, prediction)
            story = generate_health_story(prediction, memory_score, reaction_score, lifestyle_score,
                                          mem_bucket, react_bucket, life_bucket)

            session["final_prediction"] = prediction
            session["final_memory"] = memory_score
            session["final_reaction"] = reaction_score
            session["final_lifestyle"] = lifestyle_score
            session["final_mem_bucket"] = mem_bucket
            session["final_react_bucket"] = react_bucket
            session["final_life_bucket"] = life_bucket
            session["final_recs"] = categories
            session["final_story"] = story
            session["final_mem_category"] = score_category(memory_score)
            session["final_react_category"] = score_category(reaction_score)
            session["final_life_category"] = lifestyle_category(lifestyle_score)

            return redirect(url_for("show_result"))

        except Exception as e:
            app.logger.exception("Error in /diagnosis:")
            return f"Error: {str(e)}"

    return render_template("index.html")


@app.route("/result")
def show_result():
    if "final_prediction" not in session:
        return redirect(url_for("dashboard"))

    return render_template(
        "result.html",
        prediction=session["final_prediction"],
        memory_score=session["final_memory"],
        reaction_score=session["final_reaction"],
        lifestyle_score=session["final_lifestyle"],
        memory_bucket=session["final_mem_bucket"],
        reaction_bucket=session["final_react_bucket"],
        lifestyle_bucket=session["final_life_bucket"],
        recommendations=session["final_recs"],
        story=session["final_story"],
        memory_category=session["final_mem_category"],
        reaction_category=session["final_react_category"],
        lifestyle_category=session["final_life_category"],
        memory_class=get_progress_class(session["final_mem_category"]),
        reaction_class=get_progress_class(session["final_react_category"]),
        lifestyle_class=get_progress_class(session["final_life_category"], is_lifestyle=True),
    )


if __name__ == "__main__":
    app.run(debug=True)
