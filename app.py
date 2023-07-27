from flask import Flask, render_template, request
import pandas as pd
import os
import datetime

app = Flask(__name__)

TEST_CASES_FILES = 'test_cases.xlsx'

def load_test_cases():
    if os.path.exists(TEST_CASES_FILES):
        return pd.read_excel(TEST_CASES_FILES, index_col=0).to_dict(orient='index')
    else:
        return {}

def save_test_cases(test_cases):
    df = pd.DataFrame.from_dict(test_cases, orient='index')
    df.index.name = 'Test ID'
    df.to_excel(TEST_CASES_FILES)

def add_test_case(test_cases, test_id, description):
    if test_id in test_cases:
        return f"Test case with ID {test_id} already exists."
    else:
        created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        test_cases[test_id] = {'Description': description, 'Update': 'N/A', 'Status': 'Open', 'Date': created_date,
                               'Update_date': 'N/A'}
        save_test_cases(test_cases)
        return f"Test case {test_id} added successfully."

def update_test_case_status(test_cases, test_id, update, status):
    if test_id not in test_cases:
        return f"Test case with ID {test_id} does not exist."
    else:
        update_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        test_cases[test_id]['Update'] = update
        test_cases[test_id]['Status'] = status
        test_cases[test_id]['Update_date'] = update_date
        save_test_cases(test_cases)
        return f"Status of test case {test_id} changed to '{update}' and updated to '{status}' on {update_date}."

def view_test_cases(test_cases):
    return test_cases

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_test_case', methods=['POST'])
def add_test_case_route():
    test_cases = load_test_cases()
    test_id = request.form['test_id']
    description = request.form['description']
    message = add_test_case(test_cases, test_id, description)
    return message

@app.route('/update_test_case', methods=['POST'])
def update_test_case_route():
    test_cases = load_test_cases()
    test_id = int(request.form['test_id'])
    change = request.form['change']
    status = request.form['status']

    message = update_test_case_status(test_cases, test_id, change, status)
    return message

@app.route('/view_test_cases', methods=['GET'])
def view_test_cases_route():
    test_cases = load_test_cases()
    # return view_test_cases(test_cases)
    return render_template('test_cases_table.html', test_cases=test_cases)

if __name__ == "__main__":
    app.run(debug=True)
