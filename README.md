# Student ML API + Scripted Agent + Real LLM Agent

This project shows three things:

1. A machine learning model
2. A FastAPI prediction API
3. Two agents:
   - `student_agent.py` = scripted agent
   - `llm_agent.py` = real LLM agent

## Project flow

```text
User question
↓
LLM Agent
↓
LLM decides whether to call API
↓
FastAPI /predict endpoint
↓
ML model predicts score
↓
LLM explains result
```

## Files

```text
students.csv       - training data
train.py           - trains the ML model
model_api.py       - FastAPI ML prediction API
student_agent.py   - scripted/rule-based agent
llm_agent.py       - real LLM agent with tool calling
requirements.txt   - Python dependencies
.env.example       - sample environment variables
```

## Step 1: Install packages

```bash
pip install -r requirements.txt
```

## Step 2: Train the ML model

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

Test in browser:

```text
http://127.0.0.1:8000/predict?hours=5
```

## Step 4: Run scripted agent

Open another terminal:

```bash
python student_agent.py
```

This agent uses regex and if/else logic.

## Step 5: Run real LLM agent

Create `.env` from `.env.example`.

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```text
OPENAI_API_KEY=your_real_key_here
OPENAI_MODEL=llama-3.3-70b-versatile
PREDICT_API_URL=http://127.0.0.1:8000/predict
```

Then run:

```bash
python llm_agent.py
```

Ask:

```text
My son studied 5 hours. How much score can he get?
```

## Important concept

The LLM does not directly predict the score.

The ML model predicts the score.

The LLM understands the question, calls the API, reads the API result, and explains it.
