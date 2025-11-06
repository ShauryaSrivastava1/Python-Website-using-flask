from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'hospital_secret_key'  


USERNAME = "Shaurya"
PASSWORD = "abc"


patients = []
doctors = [
    {"id": 1, "name": "Dr. Shaurya", "specialization": "Dermatology"},
    {"id": 2, "name": "Dr. Anish", "specialization": "Orthopedics"},
    {"id": 3, "name": "Dr. Zahra", "specialization": "Cardiology"}
]


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.", "error")
    return render_template('login.html')


@app.route('/dashboard')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', patients=patients, doctors=doctors)


@app.route('/add_patient', methods=['POST'])
def add_patient():
    if 'user' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    doctor_id = int(request.form['doctor_id'])

    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    patients.append({
        "name": name,
        "age": age,
        "gender": gender,
        "doctor": doctor["name"] if doctor else "Unknown"
    })
    return redirect(url_for('home'))


@app.route('/delete_patient/<name>')
def delete_patient(name):
    if 'user' not in session:
        return redirect(url_for('login'))
    global patients
    patients = [p for p in patients if p['name'] != name]
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
