from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# MongoDB settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/trendtopic')
DATABASE_NAME = 'x_trends'
COLLECTION_NAME = 'trends'

# Twitter credentials
X_USERNAME = os.getenv('X_USERNAME')
X_PASSWORD = os.getenv('X_PASSWORD')

# ProxyMesh settings
PROXYMESH_HOST = os.getenv('PROXYMESH_HOST')
PROXYMESH_PORT = int(os.getenv('PROXYMESH_PORT', '31280'))
PROXYMESH_USERNAME = os.getenv('PROXYMESH_USERNAME')
PROXYMESH_PASSWORD = os.getenv('PROXYMESH_PASSWORD')