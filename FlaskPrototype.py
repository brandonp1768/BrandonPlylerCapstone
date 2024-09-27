from flask import Flask, render_template, request, redirect, url_for, flash
from ChatClasses.QAAssistant import QAAssistant
import os
from dotenv import load_dotenv
from ChatClasses.ChatCache import ChatCache

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No File Part", "Error")
        return redirect(url_for('index'))
    
    file = request.files['file']

    if file.filename == '':
        flash("No File Selected", "Error")
        return redirect(url_for('index'))
    
    file.save(f'uploads/{file.filename}')  

    fileContent = read_file(file.filename)

    Assistant = QAAssistant() # think about moving the creation of instances out of he functions

    response = Assistant.TestingCases(fileContent)

    cache = ChatCache()

    cache.AddResponse(response)
    print(cache.GetResponses())

    flash(f"{response}", "Success")
    return redirect(url_for('index')) # add a end piece that deletes the files in the uploads

def read_file(fileName):
    try:
        with open(f'uploads/{fileName}', 'r') as file:
            content = file.read()
    except FileNotFoundError:
        flash(f'The File At uploads/{fileName} Does Not Exit.')
    except IOError:
        flash('An IOError Occurred')

    return content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) # look into the waitress package in python to get rid of development server