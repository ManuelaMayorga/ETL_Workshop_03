# Description: This script consumes messages from the Kafka topic 'predict-happiness' and predicts the happiness score of the data received. The predictions are stored in a table in the database.

# Add the path to the sys
import sys
import os
from dotenv import load_dotenv

load_dotenv()
work_path = os.getenv('WORK_PATH')
sys.path.append(work_path)


# Import the necessary libraries
import pandas as pd
import json
import joblib
import logging
from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
from src.database.connection import config_loader
from src.models.models import Model_Prediction


consumer = KafkaConsumer('predict-happiness', bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: m.decode('utf-8'),
                         consumer_timeout_ms=5000,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True)


# Create a list to store the messages
list_of_messages = []
for message in consumer:
    data = message.value
    list_of_messages.append(data)  
    logging.info(f"Received message {data}")


list_of_messages = [json.loads(data) for data in list_of_messages]
df = pd.json_normalize(list_of_messages)


# Load the model
model = joblib.load('notebooks/model.pkl')


# Make the predictions
df2 = df.drop(columns=['happiness_score'], axis=1)
predictions = model.predict(df2)
df['prediction_happiness_score'] = predictions


# Connection to the database is established
connection = config_loader()
Session = sessionmaker(bind=config_loader)
session = Session()


# Create the table in the database
try:
    Model_Prediction.__table__.create(connection)
    logging.info("Table created successfully.")
except Exception as e:
    logging.error(f"Error creating table: {e}")


# Insert the data into the table
try:
    df.insert(0, 'id', range(1, 1 + len(df)))
    df.to_sql('model_predict', connection, if_exists='replace', index=False)
    logging.info("Data uploaded")

except Exception as e:
    logging.error(f"Error uploading data: {e}")

finally:
    session.close()