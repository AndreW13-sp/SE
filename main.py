from pathlib import Path
from flask import Flask, request, render_template, send_file
from gtts import gTTS
from flask_cors import CORS, cross_origin
import speech_recognition as sr

# Application Settings
app = Flask(__name__)
app.config["CORS_HEADERS"] = "application/json"
CORS(app, support_credentials=True)
file_name = "mic.wav"

# API Routes
@app.route("/", methods=["GET", "POST"])
@cross_origin(support_credentials=True)
def index():
   if request.method == "POST":
      data = request.get_json()
      myobj = gTTS(text=data.get("text"), lang="en", slow=False)
      myobj.save(file_name)
      return send_file(Path(file_name), mimetype="audio/wav", as_attachment=True, download_name=file_name)
   return render_template("home.html")


@app.route("/upload", methods=["POST"])
def handle_upload():
   file = request.files.get("speech_file")
   action = request.form.get("action")
   
   if action == "SpeechToText":
      recognizer = sr.Recognizer()
      with sr.AudioFile("./mic.wav") as source:
         audio_text = recognizer.record(source)
         try:
            converted_text = recognizer.recognize_google(audio_text, key=None)
            print(f"My Text: {converted_text}")
            return { "transcribed_speech": "converted_text" }
         except Exception as e:
            return { "error": "Something went wrong when trying to convert stt" }
   else:
      return { "error": "Unsupported action type!" }
   
   return { "foo": "bar" }

# ----------------------------------------------------------------------------
# Running main server here...
# ----------------------------------------------------------------------------
if __name__ == "__main__":
   app.run(debug=True)