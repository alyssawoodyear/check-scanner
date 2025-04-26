from flask import Flask, request, render_template_string
import csv

app = Flask(__name__)

@app.route('/')
def upload_page():
    return open('index.html').read()

@app.route('/scan', methods=['POST'])
def scan_checks():
    uploaded_file = request.files['file']
    safe_checks = []
    fraudulent_checks = []

    if uploaded_file.filename.endswith('.csv'):
        csvfile = uploaded_file.stream.read().decode("UTF8").splitlines()
        reader = csv.reader(csvfile)
        
        for row in reader:
            check_text = row[0]
            if "suspicious" in check_text.lower() or "fake" in check_text.lower():
                fraudulent_checks.append(check_text)
            else:
                safe_checks.append(check_text)

    return render_template_string('''
        <h1>Scan Results</h1>
        <h2>✅ Safe Checks:</h2>
        <ul>
        {% for check in safe_checks %}
            <li>{{ check }}</li>
        {% endfor %}
        </ul>
        <h2>❌ Fraudulent Checks:</h2>
        <ul>
        {% for check in fraudulent_checks %}
            <li>{{ check }}</li>
        {% endfor %}
        </ul>
        <a href="/">🔙 Upload Another</a>
    ''', safe_checks=safe_checks, fraudulent_checks=fraudulent_checks)

if __name__ == '__main__':
    app.run(debug=True)
