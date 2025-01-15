# app.py
import logging
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from scraper import XScraper
from database import Database
import traceback

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False

# Initialize database connection at startup
try:
    db = Database()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise

@app.route('/')
def index():
    try:
        latest_trends = db.get_latest_trends()
        return render_template('index.html', trends=latest_trends)
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch-trends')
def fetch_trends():
    scraper = None
    try:
        # Initialize scraper
        logger.debug("Initializing X scraper...")
        scraper = XScraper()
        
        # Login and fetch trends
        logger.debug("Logging into X...")
        scraper.login_to_x()
        
        logger.debug("Fetching trending topics...")
        trends = scraper.get_trending_topics()
        
        if not trends or len(trends) < 5:
            raise ValueError("Failed to fetch 5 trending topics")
        
        # Save to database
        saved_record = db.save_trends(trends, scraper.get_current_ip())
        
        if not saved_record:
            raise ValueError("Failed to save trends to database")
        
        # Fetch the latest record to confirm save
        latest_record = db.get_latest_trends()
        
        if not latest_record:
            raise ValueError("Failed to retrieve saved trends")
        
        # Format the response
        response_data = {
            'trends': [
                latest_record['nameoftrend1'],
                latest_record['nameoftrend2'],
                latest_record['nameoftrend3'],
                latest_record['nameoftrend4'],
                latest_record['nameoftrend5']
            ],
            'timestamp': latest_record['timestamp'].isoformat(),
            'ip_address': latest_record['ip_address']
        }
        
        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        error_msg = f"Error in fetch-trends: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500
        
    finally:
        if scraper:
            try:
                logger.debug("Cleaning up scraper...")
                scraper.cleanup()
            except Exception as e:
                logger.error(f"Error during cleanup: {str(e)}")

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)