# Workshop_03 - Machine Learning Prediction and streaming data 
Autor: [@ManuelaMayorga](https://github.com/ManuelaMayorga)

---

## Welcome
Given the 5 CSV files which have information about happiness score in different countries, train a regression machine learning model to predict the happiness score.

Throughout this process, specific technologies were used including:

- _Python_ <img src="https://cdn-icons-png.flaticon.com/128/3098/3098090.png" alt="Python" width="21px" height="21px"> 
- _Jupyter Notebook_  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" alt="Jupyer" width="21px" height="21px">
- _PostgreSQL_ as the relational database management system (this was chosen by personal preference). <img src="https://cdn-icons-png.flaticon.com/128/5968/5968342.png" alt="Postgres" width="21px" height="21px">
- _Apache Kafka_  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Apache_kafka.svg/1200px-Apache_kafka.svg.png" width="21px" height="25px">

## Objectives

- EDA and ETL: Perform exploratory data analysis and prepare data for modeling by cleaning, preprocessing, and selecting relevant features.
- Regression Model Training: Develop a regression model using a 70-30 split of data for training and testing, optimizing its performance.
- Data Streaming with Kafka: Implement a streaming architecture with Kafka to process real-time data from EDA/ETL to model prediction.
- Prediction and Storage: Use the trained model to predict happiness scores in real time and store the predictions along with the corresponding features in a database.

## Workflow



## Data Source

These are the soruce of the datasets used in this project: 

- [World Happiness Report](https://www.kaggle.com/datasets/unsdsn/world-happiness)

## Folders Path

```
Workshop3
├── data                           # Contains CSV data files
├── notebooks                      # Contains Jupyter notebooks for data analysis
│   ├── 001-EDA.ipynb              # Notebook for Exploratory Data Analysis
│   └── 002-model_metrics.ipynb    # Notebook for model metrics evaluation
│   └── model.pkl                  # Pickle file with the trained model
├── src                            # Contains the project's source code
│   ├── database                   # Modules related to the database
│   │   ├── __init__.py
│   │   ├── connection.py          # Script for database connection
│   │   └── db_settings.json       # Database configuration file
│   ├── models                     # Modules related to machine learning models
│   │   ├── __init__.py
│   │   └── models.py              # Script for sql table model
│   └── utils                      # Utility modules
│       ├── __init__.py
│       └── feature_selection.py   # Script for feature selection
├── .env                           # Environment configuration file
├── .gitignore                     # File for ignoring files in version control
├── consumer.py                    # Script for the consumer in a microservices architecture
├── docker-compose.yml             # Docker Compose configuration file
├── producer.py                    # Script for the producer in a microservices architecture
└── requirements.txt               # Requirements file for installing Python dependencies
```

## How to run this project

First of all here is the requierements

Install Python : [Python Downloads](https://www.python.org/downloads/)  
Install PostgreSQL : [PostgreSQL Downloads](https://www.postgresql.org/download/)  
Install Docker : [Docker Downloads](https://www.docker.com/get-started/)

1. Clone this repository:
```bash
   git clone https://github.com/ManuelaMayorga/Workshop-3.git
 ```

2. Go to the project directory  
```bash
   cd Workshop-3
```

3. Create a virtual enviroment  
```bash
  python -m venv venv
```

4. Start the virtual enviroment  
  ```bash  
  ./venv/Scripts/activate
  ```

5. Create into src/database a json file named `db_settings.json` and add the following keys to the file:  
```json
   {
    "user": "Your PostgreSQL database username."
    "password": "Your PostgreSQL database password."
    "host": "The host address or IP where your PostgreSQL database is running."
    "port": "The port on which PostgreSQL is listening."
    "database": "The name of your PostgreSQL database."
   }
```

6. Install necesary libreries:  
```bash
  pip install -r requirements.txt
```

7. Create a `.env` file and add this variable:
   ```
   WORK_PATH <- Sets the working directory for the application, indicating the base path for performing operations and managing files.
   ```

8. Create a database in PostgreSQL (Make sure is the same name as your 'database' name in the json file)

9. Start with the notebook:
- 001-EDA.ipynb
  
10. Run the streaming
  10.1 Make sure tha you have docker running, open a terminal and run:
    
  ```bash
  docker compose up
  ```
    
  10.2 Open a new terminal and get into container terminal running:
  ```bash
    docker exec -it kafka-test bash
  ```
     
  10.3 Create a new topic:
  
  ```bash
    kafka-topics --bootstrap-server kafka-test:9092 --create --topic predict-happiness
  ```

  10.4 Run producer and consumer:

  - **producer**
    
    ```bash
    python producer.py
    ```
    
  - **consumer**
    
    ```bash
    python consumer.py
    ```

  Check your database on Postgresql and you should have a new table created.

  Now go to:
  - 002-model_metrics.ipynb

  and run all the notebooks to see the performance of the model

## Thank you for visiting this repository, remember to rate if it was helpful ⭐🐮
    
  
  
