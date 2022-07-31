from cgitb import text
from flask import Flask, request, render_template, send_file
from gtts import gTTS
from flask_cors import CORS, cross_origin

import os


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/', methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def index():
    if request.method == 'POST':
        myvariable=request.json['text']
        myobj = gTTS(text= myvariable, lang='en', slow=False)
        myobj.save('mic.mp3')
        return send_file('mic.mp3',as_attachment=True)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)