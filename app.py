from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
# 1. Old package mathitu pudhiya 'google' package import panrom
from google import genai
import os

# Load environment variables
load_dotenv()

# 2. Configure & Client Creation (GEMINI_API_KEY automatic ah load aagidump)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Flask App
app = Flask(__name__)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- LOGIN ----------------

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- PHISHING ----------------
@app.route("/phishing")
def phishing():
    return render_template("phishing.html")

@app.route("/analyze-phishing", methods=["POST"])
def analyze_phishing():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"response": "Empty text provided"}), 400

        prompt = f"""
        You are a Cybersecurity Expert.

        Analyze the following message or URL.

        {text}

        Return your response in this format:

        Verdict:
        Risk Level:
        Reasons:
        Safety Tips:
        """

        # புது 'client' சின்டாக்ஸ் மற்றும் 'gemini-2.5-flash' மாடலுக்கு மாத்தியாச்சு
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return jsonify({
            "response": response.text
        })
        
    except Exception as e:
        print("PHISHING ANALYZER ERROR:", e)
        return jsonify({"response": "Error analyzing phishing data"}), 500
# ---------------- QUIZ ----------------
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    prompt = """
    Generate 5 multiple choice questions on cybersecurity.
    Return ONLY valid JSON format like this:

    [
      {
        "question": "Question text here",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "answer": "The exact correct option string"
      }
    ]
    """

    try:
        # 1. 'model'க்கு பதிலா புது 'client' சின்டாக்ஸ்
        # 2. 'response_mime_type' குடுத்தா கரெக்டா சுத்தமான JSON மட்டும் தான் ரிட்டர்ன் ஆகும்
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json'
            }
        )

        return jsonify({
            "quiz": response.text
        })
        
    except Exception as e:
        print("QUIZ ERROR:", e)
        return jsonify({"response": "Error generating quiz"}), 500
# ---------------- AI TUTOR ----------------

@app.route("/ai-tutor")
def ai_tutor():
    return render_template("ai_tutor.html")

# ---------------- GEMINI AI API ----------------

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"response": "empty prompt"}), 400
            
        # 3. New Client Syntax standard model version oda
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return jsonify({
            "response": response.text
        })
        
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": "AI error occurred. Check logs."}), 500

# ---------------- RUN APP ----------------

if __name__== "__main__":
    app.run(debug=True)