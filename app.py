from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import datetime

app = Flask(__name__)

BUG_REPORT_FILES = 'bug_report.xlsx'

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
        bug_report[bug_id] = {'Description': description, 'Update': 'N/A', 'Status': 'Open', 'Date': created_date,
                               'Update_date': 'N/A'}
        save_bug_report(bug_report)
        return f"Bug ID {bug_id} added successfully."

def update_bug_status(bug_report, bug_id, update, status):
    if bug_id not in bug_report:
        return f"Bug with ID {bug_id} does not exist."
    else:
        update_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bug_report[bug_id]['Update'] = update
        bug_report[bug_id]['Status'] = status
        bug_report[bug_id]['Update_date'] = update_date
        save_bug_report(bug_report)
        return f"Status of bug ID {bug_id} changed to '{update}' and updated to '{status}' on {update_date}."

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
    status = request.form['status']

    message = update_bug_status(bug_report, bug_id, change, status)
    return message

@app.route('/view_bugs', methods=['GET'])
def view_bugs_route():
    bug_report = load_bug_report()
    # return view_bugs(bug_report)
    return render_template('bugs_table.html', bug_report=bug_report)

@app.route('/download_bug_report')
def download_bug_report():
    # Ensure the 'bug_report.xlsx' file exists in the same directory as 'app.py'
    file_path = 'bug_report.xlsx'
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
