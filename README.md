# Skills Utilization Platform & Course Recommendation Engine

## Project Overview

This project is an AI-powered course recommendation system that suggests relevant courses based on a user's skills.

The system uses:
- Skill extraction
- Sentence Transformer embeddings
- Average pooling
- Cosine similarity
- SQLAlchemy Core
- SQLite
- Flask API
- LangChain tools
- LangGraph workflow
- Fallback logic
- Recommendation logging

## Project Flow

User ID / User Skills  
→ Get Skills  
→ Generate Skill Embeddings  
→ Build User Profile Vector  
→ Compare With Course Embeddings  
→ Calculate Cosine Similarity  
→ Rank Courses  
→ Return Top 3 Recommendations  

## Day 1 - Core AI Engine

Day 1 focuses on the recommendation logic.

### Skill Extraction

User skills are extracted from text using predefined skills.

Example:

```text
I know Python and machine learning
```

Output:

```text
['python', 'machine learning']
```

### Embeddings

The project uses the Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

User skills and course descriptions are converted into numerical embeddings.

### User Profile Vector

When a user has multiple skills, their embeddings are combined using average pooling.

### Similarity and Ranking

Cosine similarity compares the user profile vector with course embeddings.

Courses are ranked from the highest similarity score to the lowest.

### Recommendation Output

The system returns the Top 3 courses with:
- Course title
- Similarity score
- Short explanation

Example:

```text
Machine Learning Fundamentals - Score: 0.647
Python Basics - Score: 0.543
Data Analysis with Python - Score: 0.442
```

## Day 2 - Database and API

Day 2 connects the recommendation engine to a database and API.

### Database

SQLAlchemy Core and SQLite are used.

Tables:
- users
- skills
- courses
- user_skills
- embeddings
- recommendation_logs

Sample users:
- Abdullah
- Haya

The `user_skills` table connects users with their skills.

Course embeddings are stored in the database.

### Flask API

The API endpoint is:

```text
POST /api/recommend
```

Example request:

```json
{
  "user_id": 1
}
```

Example response:

```json
{
  "user_id": 1,
  "extracted_skills": [
    "python",
    "machine learning"
  ],
  "recommended_courses": [
    {
      "title": "Machine Learning Fundamentals",
      "score": 0.647,
      "explanation": "Recommended based on similarity with your skills"
    }
  ]
}
```

## Day 3 - Agents and Workflow

Day 3 extends the system with LangChain and LangGraph.

### LangChain Tools

Two tools are used:
- Skill Agent
- Recommendation Agent

The Skill Agent gets user skills from the database.

The Recommendation Agent generates course recommendations from the user's skills.

### LangGraph Workflow

The workflow is:

```text
START
  ↓
Get Skills
  ↓
Generate Recommendations
  ↓
Log Recommendations
  ↓
END
```

### Fallback Logic

If a user does not have skills, the system returns no recommendations instead of failing.

Example:

```json
{
  "error": "User has no skills"
}
```

### Logging

Recommended courses and similarity scores are stored in the `recommendation_logs` table.

## Project Files

```text
proj5_repo/
│
├── data/
│   └── courses.csv
│
├── main.py
├── recommender.py
├── database.py
├── store_embeddings.py
├── api.py
├── agents.py
├── workflow.py
├── project5.db
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone git@github.com:Abdullah-hlalat/proj5_repo.git
cd proj5_repo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install requirements

```bash
python3 -m pip install -r requirements.txt
```

### 4. Create the database

```bash
python3 database.py
```

### 5. Store course embeddings

```bash
python3 store_embeddings.py
```

### 6. Run the command-line test

```bash
python3 main.py
```

### 7. Run the Flask API

```bash
python3 api.py
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

## API Testing

Example using curl:

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
-H "Content-Type: application/json" \
-d '{"user_id": 1}'
```

## Technologies

- Python
- Pandas
- NumPy
- Sentence Transformers
- Scikit-learn
- SQLAlchemy Core
- SQLite
- Flask
- LangChain
- LangGraph

## Summary

The project recommends courses based on user skills using semantic similarity.

It combines an AI recommendation engine with a relational database, Flask API, LangChain tools, LangGraph workflow, fallback handling, and recommendation logging.
