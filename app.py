from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import pandas as pd
import joblib

# Load model and dependencies
loaded_model = joblib.load("Model/stroke_log_model.pkl")
loaded_scaler = joblib.load("Model/scaler.pkl")
loaded_features = joblib.load("Model/feature_order.pkl")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("./Templates/index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df_input = pd.DataFrame([data["features"]])
        df_input_encoded = pd.get_dummies(df_input)
        df_input_encoded = df_input_encoded.reindex(columns=loaded_features, fill_value=0)
        scaled_input = loaded_scaler.transform(df_input_encoded)
        proba = loaded_model.predict_proba(scaled_input)[0][1]
        prediction = int(proba >= 0.07)

        return jsonify({
            "stroke_prediction": prediction,
            "confidence": round(proba, 3)
        })
    except Exception as e:
        return jsonify({
            "stroke_prediction": -1,
            "confidence": 0.0,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
