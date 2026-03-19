from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
app.secret_key = "autism_secret_key"

UPLOAD_DIR = os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================================================
# QUESTIONNAIRE LOGIC
# ======================================================
def get_stage_from_score(score):
    if score <= 2:
        return "Low Risk", "Non-ASD"
    elif score <= 5:
        return "Level 1 (Classic Autism)", "ASD"
    elif score <= 8:
        return "Level 2 (Aspergers Syndrome)", "ASD"
    else:
        return "Level 3 (PDD-NOS)", "ASD"

# ======================================================
# ROUTES
# ======================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/behavior_screening")
def behavior_screening():
    return render_template("behavior_screening.html")

# ======================================================
# VIDEO UPLOAD → REDIRECT TO QUESTIONNAIRE
# ======================================================
@app.route("/predict_video", methods=["POST"])
def predict_video():
    file = request.files.get('file')

    if file:
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)

    # 🔥 Always go to questionnaire
    return redirect("/behavior_screening")

# ======================================================
# EYE VIDEO → ALSO REDIRECT
# ======================================================
@app.route("/upload_asd_video", methods=["POST"])
def upload_asd_video():
    file = request.files.get('file')

    if file:
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)

    return redirect("/behavior_screening")

# ======================================================
# QUESTIONNAIRE SUBMIT → RESULT
# ======================================================
@app.route("/submit_behavior", methods=["POST"])
def submit_behavior():
    score = sum(int(request.form[f"q{i}"]) for i in range(1, 11))
    stage, prediction = get_stage_from_score(score)

    return render_template(
        "result.html",
        prediction=prediction,
        stage=stage
    )

# ======================================================
# LIVE GAZE CAMERA
# ======================================================
@app.route("/start_gaze_live", methods=["GET", "POST"])
def start_gaze_live():
    return render_template("realtime_gaze.html")

# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)