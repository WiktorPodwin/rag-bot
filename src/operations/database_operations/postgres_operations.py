import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv('POSTGRES_PORT')
conn = psycopg2.connect(database=)