from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml"
}


@app.route("/")
def home():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()
        source = data.get("source", "en")
        target = data.get("target", "en")

        if not text:
            return jsonify({
                "success": False,
                "message": "Please enter some text."
            }), 400

        if source == "auto":
            source = "en"

        # MyMemory Translation API
        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{source}|{target}"
        }

        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "message": "Translation service is temporarily unavailable."
            }), 500

        result = response.json()

        translated_text = result["responseData"]["translatedText"]

        return jsonify({
            "success": True,
            "translation": translated_text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Translation failed. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)