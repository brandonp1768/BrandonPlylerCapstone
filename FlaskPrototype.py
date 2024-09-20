from flask import Flask, render_template, request, redirect, url_for, flash
from ChatClasses.QAAssistant import QAAssistant
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Move this to the environment variables

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
    
    # Save the file or process it as needed
    file.save(f'uploads/{file.filename}')  

    fileContent = read_file(file.filename)

    Assistant = QAAssistant()

    response = Assistant.EdgeCases(fileContent)

    flash(f"{response}", "Success")
    return redirect(url_for('index'))

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