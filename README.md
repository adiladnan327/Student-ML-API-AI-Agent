# Student ML API + Simple AI Agent

This is a baby-step project to understand how an ML API and an AI agent work together.

## What this project does

The ML API predicts a student's exam score based on study hours.

The agent accepts normal English, extracts the study hours, calls the ML API, and explains the result.

Example:

```text
You: My son studied 5 hours. How much score can he get?

Agent:
Based on 5.0 study hours, the ML model predicts a score of around 65.0.

Recommendation: This is a decent score, but there is room to improve.
```

## Project flow

```text
User question
↓
Student Agent
↓
Extract study hours
↓
Call ML API
↓
ML model predicts score
↓
Agent explains result
```

## Files

```text
students.csv       - Training data
train.py           - Trains the ML model
model_api.py       - FastAPI prediction API
student_agent.py   - Simple agent that calls the API
requirements.txt   - Python packages
Dockerfile         - Optional Docker deployment
```

## Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Train the model

```bash
python train.py
```

This creates:

```text
student_model.pkl
```

## Step 3: Start the ML API

```bash
uvicorn model_api:app --reload
```

Open this in your browser:

```text
http://127.0.0.1:8000
```

Test prediction:

```text
http://127.0.0.1:8000/predict?hours=5
```

## Step 4: Run the agent

Open another terminal and run:

```bash
python student_agent.py
```

Then ask:

```text
My son studied 5 hours. How much score can he get?
```

## Optional: Run with Docker

```bash
docker build -t student-ml-api .
docker run -p 8000:8000 student-ml-api
```

Then run the agent separately:

```bash
python student_agent.py
```

## Important note

This is a simple learning project. The "agent" here is a rule-based agent.

A real LLM-based agent can later be added with tools like LangChain, LangGraph, Semantic Kernel, or OpenAI function calling.

## Author

Adil Mohammed