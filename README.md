
## Manufacturing Prediction API

This project provides a machine learning-based API to predict machine downtime or product defects in a manufacturing environment. The API is built with **Flask** and uses a **Decision Tree** model trained on data such as machine temperature, runtime, and downtime flag.

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [API Endpoints](#api-endpoints)
3. [Conclusion](#conclusion)

## Setup Instructions

Follow these steps to set up and run the API locally:

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- cURL (for testing API requests)

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd manufacturing_prediction
```
### Step 2: Install Dependencies
Create a virtual environment (optional but recommended) and install the required libraries:

### Create virtual environment (optional)
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
### Install required libraries
```bash
pip install -r requirements.txt
```
### Step 3: Start the FastAPI Application
Run the FastAPI application:
```bash
uvicorn app:app --reload
```
## API Endpoints
### 1. Upload Endpoint (/upload)
#### Method: POST
Description: Accepts a CSV file containing machine data (e.g., Machine_ID, Temperature, Run_Time, Downtime_Flag) and trains the model on the data.
Request Body: multipart/form-data with a CSV file.

#### Example cURL Request:
```bash
curl -X POST -F "file=@data.csv" http://127.0.0.1:5000/upload
```
#### Response:
```json
{
  "accuracy": 0.85,
  "f1_score": 0.83
}
```
### 2. Train Endpoint (/train)
#### Method: POST
Description: Trains the model with the uploaded data and returns performance metrics like accuracy and F1-score.
Request Body: None (requires data to be uploaded via /upload).

#### Example cURL Request:
```bash
curl -X POST http://127.0.0.1:5000/train
```
#### Response:
```json
{
  "accuracy": 0.85,
  "f1_score": 0.83
}
```
### 3. Predict Endpoint (/predict)
#### Method: POST
Description: Accepts JSON input with Temperature and Run_Time, and returns a prediction (Downtime: Yes/No) and confidence score.
Request Body: JSON with the features Temperature and Run_Time.
#### Example cURL Request:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"Temperature": 75, "Run_Time": 150}' http://127.0.0.1:5000/predict
```
#### Response:
```json
{
  "Downtime": "No",
  "Confidence": 0.85
}
```


## Conclusion
This API helps you predict machine downtime or product defects using basic machine learning models. It includes endpoints to upload data, train the model, and make predictions. You can use cURL or Postman to interact with the API.