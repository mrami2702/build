from flask import Flask, request, jsonify
import os # <-- Add this import for file path operations
from werkzeug.utils import secure_filename # <-- Add this for secure filename handling

app = Flask(__name__)

# Define the upload folder
# It's good practice to make this configurable or retrieve from environment variables
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists when the app starts
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return "Welcome to the Data Insight Platform Backend! More features coming soon."

# This will be the endpoint for uploading data
@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 1. Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        # 2. Define the full path where the file will be saved
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # 3. Save the file
            file.save(filepath)
            print(f"File saved to: {filepath}")

            # Here you would typically trigger your data processing logic:
            # e.g., read CSV into Pandas, perform analysis, store results in DB.
            # For now, let's just confirm it's saved.

            return jsonify({
                'message': f'File "{filename}" uploaded successfully and saved!',
                'filepath': filepath,
                'status': 'Ready for processing.'
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

    return jsonify({'error': 'Something went wrong with the upload.'}), 500

@app.route('/insights', methods=['GET'])
def get_insights():
    # In a real application, you'd query your database or analysis results
    # to provide insights based on uploaded data.
    dummy_insights = {
        "total_datasets": 0,
        "latest_analysis": "No data analyzed yet. Please upload data.",
        "recommendations": []
    }
    return jsonify(dummy_insights), 200

if __name__ == '__main__':
    app.run(debug=True)