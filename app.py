from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

latest_data = {
    "soil": 0,
    "temperature": 0,
    "humidity": 0
}

# ── Multilingual responses with Metric Labels ───────────────────────────────
ANSWERS = {
    "en-IN": {
        "soil_pre": "Soil moisture is",
        "temp_pre": "The temperature is",
        "hum_pre": "Current humidity is",
        "water_dry": "Soil is dry. Please water the crops.",
        "cond_hot":  "Temperature is too high. Check the plants.",
        "cond_ok":   "Conditions are good for crops.",
        "fallback":  "Monitoring your farm live."
    },
    "hi-IN": {
        "soil_pre": "मिट्टी की नमी है",
        "temp_pre": "तापमान है",
        "hum_pre": "वर्तमान आर्द्रता है",
        "water_dry": "मिट्टी सूखी है। कृपया फसलों को पानी दें।",
        "cond_hot":  "तापमान बहुत अधिक है। पौधों की जाँच करें।",
        "cond_ok":   "फसलों के लिए परिस्थितियाँ अच्छी हैं।",
        "fallback":  "आपके खेत की लाइव निगरानी कर रहा हूँ।"
    },
    "te-IN": {
        "soil_pre": "నేల తేమ",
        "temp_pre": "ప్రస్తుత ఉష్ణోగ్రత",
        "hum_pre": "ప్రస్తుత తేమ",
        "water_dry": "నేల పొడిగా ఉంది. దయచేసి పంటలకు నీరు పెట్టండి.",
        "cond_hot":  "ఉష్ణోగ్రత చాలా ఎక్కువగా ఉంది. మొక్కలను తనిఖీ చేయండి.",
        "cond_ok":   "పంటలకు పరిస్థితులు బాగున్నాయి.",
        "fallback":  "మీ పొలాన్ని ప్రత్యక్షంగా పర్యవేక్షిస్తున్నాను."
    },
}

def ans(lang, key):
    t = ANSWERS.get(lang, ANSWERS["en-IN"])
    return t.get(key, t["fallback"])

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data')
def get_data():
    return jsonify(latest_data)

@app.route('/update', methods=['POST'])
def update():
    global latest_data
    data = request.json
    if data:
        if data.get("temperature") not in [0, None]:
            latest_data["temperature"] = float(data["temperature"])
        if data.get("humidity") not in [0, None]:
            latest_data["humidity"] = float(data["humidity"])
        latest_data["soil"] = int(data.get("soil", latest_data["soil"]))
    return jsonify({"status": "ok"})

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    body = request.json
    # Convert question to lowercase for easier matching
    question = body.get("question", "").lower()
    lang = body.get("lang", "en-IN")
    
    soil = latest_data["soil"]
    temp = latest_data["temperature"]
    hum  = latest_data["humidity"]

    # 1. Check for specific Metric Queries (Humidity, Temp, Soil)
    # Checks for English, Hindi, and Telugu keywords
    if any(k in question for k in ["humidity", "आर्द्रता", "నమీ", "తేమ"]):
        return jsonify({"suggestion": f"{ans(lang, 'hum_pre')} {hum}%"})
    
    if any(k in question for k in ["temperature", "तापमान", "ఉష్ణోగ్రత"]):
        return jsonify({"suggestion": f"{ans(lang, 'temp_pre')} {temp}°C"})
    
    if any(k in question for k in ["soil", "moisture", "मिट्टी", "నేల"]):
        return jsonify({"suggestion": f"{ans(lang, 'soil_pre')} {soil}"})

    # 2. Fallback to Autonomous Logic if no specific metric is asked
    if soil > 600:
        msg = ans(lang, "water_dry")
    elif isinstance(temp, (int, float)) and temp > 35:
        msg = ans(lang, "cond_hot")
    else:
        msg = msg = ans(lang, "cond_ok")
    
    return jsonify({"suggestion": msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)