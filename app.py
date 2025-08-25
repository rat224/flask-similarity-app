import os
from flask import Flask, request, jsonify
from gradio_client import Client
import docx

app = Flask(__name__)

# Connect to your Hugging Face Space
SPACE_URL = "https://rathod31-kannada-english-sim.hf.space"
client = Client(SPACE_URL)

def extract_text_from_file(file_path):
    """Extract plain text from .txt or .docx"""
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

@app.route("/compare", methods=["POST"])
def compare_texts():
    try:
        # 1. Get input from request
        audio_text = request.form.get("audio_text", "").strip()
        uploaded_file = request.files.get("file")

        if not audio_text or not uploaded_file:
            return jsonify({"error": "Both 'audio_text' and 'file' are required."}), 400

        # 2. Save file temporarily and extract text
        file_path = os.path.join("uploads", uploaded_file.filename)
        os.makedirs("uploads", exist_ok=True)
        uploaded_file.save(file_path)
        file_text = extract_text_from_file(file_path)

        if not file_text:
            return jsonify({"error": "Could not extract text from file."}), 400

        # 3. Call Hugging Face Space API
        result_json, similarity = client.predict(
            lang="Kannada",   # can auto-detect later, forcing Kannada now
            a=audio_text,
            b=file_text,
            api_name="/_on_click"
        )

        # 4. Format response
        return jsonify({
            "cosine": result["scores"]["cosine"],
            "similarity": result["similarity"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
