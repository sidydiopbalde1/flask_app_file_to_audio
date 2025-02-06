from flask import Flask, render_template, request, send_file
import os
import pypdf
from gtts import gTTS

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/output"

# Assurez-vous que les dossiers existent
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    audio_file = None
    if request.method == "POST":
        # Vérifier si un fichier a été uploadé
        if "file" not in request.files:
            return render_template("index.html", error="Aucun fichier sélectionné")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="Fichier invalide")
        
        # Sauvegarder le fichier uploadé
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extraire le texte du PDF
        pdf_reader = pypdf.PdfReader(file_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        # Vérifier si du texte a été extrait
        if not text.strip():
            return render_template("index.html", error="Impossible d'extraire du texte du PDF")

        # Convertir le texte en audio
        audio_file = os.path.join(OUTPUT_FOLDER, "output.mp3")
        tts = gTTS(text, lang="fr")
        tts.save(audio_file)

    return render_template("index.html", audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
