from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
import datetime

from send_mail import configure_mail, send_bug_report_email  # Import the email functions


app = Flask(__name__)

BUG_REPORT_FILES = 'bug_report.xlsx'

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'     # Replace with your email password

# Create a Mail instance by calling the configure_mail function from email_utils
mail = configure_mail(app)

def load_bug_report():
    if os.path.exists(BUG_REPORT_FILES):
        return pd.read_excel(BUG_REPORT_FILES, index_col=0).to_dict(orient='index')
    else:
        return {}

def save_bug_report(bug_reports):
    df = pd.DataFrame.from_dict(bug_reports, orient='index')
    df.index.name = 'Bug ID'
    df.to_excel(BUG_REPORT_FILES)

def add_bug(bug_report, bug_id, description):
    if bug_id in bug_report:
        return f"Bug with ID {bug_id} already exists."
    else:
        created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bug_report[bug_id] = {'Description': description, 'Update': description, 'Status': 'Open', 'Date': created_date,
                               'Update_date': created_date }
        save_bug_report(bug_report)
        return f"Bug ID {bug_id} added successfully."

def update_bug_status(bug_report, bug_id, update, status):
    if bug_id not in bug_report:
        return f"Bug with ID {bug_id} does not exist."
    else:
        update_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bug_report[bug_id]['Update'] = update
        bug_report[bug_id]['Status'] = status.strip()
        bug_report[bug_id]['Update_date'] = update_date
        save_bug_report(bug_report)
        return f"Successfully updated bug ID {bug_id} and status changed to '{status}'."

def view_bugs(bug_report):
    return bug_report

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_bugs', methods=['POST'])
def add_bugs_route():
    bug_report = load_bug_report()
    bug_id = request.form['bug_id']
    description = request.form['description']
    message = add_bug(bug_report, bug_id, description)
    return message

@app.route('/update_bugs', methods=['POST'])
def update_bugs_route():
    bug_report = load_bug_report()
    bug_id = int(request.form['bug_id'])
    change = request.form['change']
    status = request.form['status'].strip()

    message = update_bug_status(bug_report, bug_id, change, status)
    return message

@app.route('/view_bugs', methods=['GET'])
def view_bugs_route():
    bug_report = load_bug_report()
    # return view_bugs(bug_report)
    return render_template('view_table.html', bug_report=bug_report)

@app.route('/download_bug_report')
def download_bug_report():
    # Ensure the 'bug_report.xlsx' file exists in the same directory as 'app.py'
    file_path = 'bug_report.xlsx'
    return send_file(file_path, as_attachment=True)

@app.route('/get_bug_details')
def get_bug_details():
    bug_report = load_bug_report()
    bug_id = int(request.args.get('bug_id'))
    if bug_id in bug_report:
        return jsonify(bug_report[bug_id])
    else:
        return jsonify({'error': 'Bug with the provided ID does not exist.'})

@app.route('/send_email', methods=['GET'])
def send_email():
    # Ensure the 'bug_report.xlsx' file exists in the same directory as 'app.py'
    file_path = 'bug_report.xlsx'

    # Define the sender and recipient email addresses
    sender_email = app.config['MAIL_USERNAME']
    recipients = ['recipient@example.com']  # Replace with the recipient's email address

    try:
        # Send the email
        send_bug_report_email(mail, sender_email, recipients, file_path)
        return "Bug report email sent successfully!"
    except Exception as e:
        return f"An error occurred while sending the email: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
