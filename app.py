from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    if request.method == 'POST':
        file = request.files['checkfile']
        if file:
            filename = file.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            
            # Only look at the filename
            if 'fraud' in filename.lower():
                result = "⚠️ Fraudulent Check Detected"
            else:
                result = "✅ Check Appears Safe"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
