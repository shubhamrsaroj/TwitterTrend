# Twitter Trending Topics Scraper

## Overview
This project is a web scraping application that utilizes Selenium and ProxyMesh to extract the top 5 trending topics from Twitter. The scraped data is stored in a MongoDB database, and a simple web interface is provided to run the script and display the results.

## Features
- Scrapes the top 5 trending topics from Twitter's homepage.
- Uses ProxyMesh to rotate IP addresses for each request.
- Stores the results in a MongoDB database.
- Provides a user-friendly HTML interface to trigger the scraping process and view results.

## Requirements
- Python 3.x
- Selenium
- ProxyMesh account
- MongoDB
- Flask (for the web interface)
- A Twitter account for scraping

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/twitter-trending-topics-scraper.git
   cd twitter-trending-topics-scraper
Install Dependencies Ensure you have Python and pip installed. Then, install the required packages:

bash

Verify

Open In Editor
Run
Copy code
pip install selenium pymongo flask python-dotenv
Set Up Environment Variables Create a .env file in the root directory and add your ProxyMesh credentials and MongoDB connection string:

plaintext

Verify

Open In Editor
Run
Copy code
PROXYMESH_USERNAME=your_username
PROXYMESH_PASSWORD=your_password
MONGODB_URI=mongodb://your_mongo_uri
Run the Application Start the Flask web server:

bash

Verify

Open In Editor
Run
Copy code
python app.py
Access the Web Interface Open your web browser and navigate to http://127.0.0.1:5000 to access the application.

Usage
Click the button on the web page to run the Selenium script.
The top 5 trending topics will be displayed along with the IP address used for the query and a JSON extract of the record from MongoDB.
Expected Output
When the script is executed, the output will show:

The date and time of the query.
The names of the top 5 trending topics.
The IP address used for the query.
A JSON representation of the stored record in MongoDB.
Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Special thanks to the open-source community for the tools and libraries utilized in this project.

Verify

Open In Editor
Run
Copy code

### Notes:
- Replace `yourusername`, `your_mongo_uri`, and other placeholders with actual values relevant to your project.
- Feel free to modify any sections to better fit your project's specifics or 
