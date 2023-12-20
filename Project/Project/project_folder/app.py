# app.py
from flask import Flask, render_template, jsonify, request
import openpyxl
from datetime import datetime

app = Flask(__name__)

# In-memory data store for simplicity
file_tempo_responses = []

@app.route('/api/file_tempo', methods=['POST'])
def file_tempo():
    # Assume the request contains JSON data
    data = request.get_json()

    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_tempo_responses.append(data)

    # Include the received data in the response
    response_data = {
        "message": "Data stored successfully!",
        "received_data": data
    }

    return jsonify(response_data)

@app.route('/table')
def table():
    return render_template('table.html', responses=file_tempo_responses)

@app.route('/export')
def export():
    # Create Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Timestamp', 'Data'])  # Header

    # Add data to Excel file
    for response in file_tempo_responses:
        ws.append([response['timestamp'], response['data']])

    # Save the Excel file
    excel_filename = f"export_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    wb.save(excel_filename)

    return f"Excel file exported as {excel_filename}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
