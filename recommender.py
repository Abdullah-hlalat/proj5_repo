import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")

courses = pd.read_csv("data/courses.csv")

course_embeddings = model.encode(
    courses["description"].tolist()
)

def extract_skills(text):

    known_skills = [
        "python",
        "machine learning",
        "data analysis",
        "sql",
        "deep learning",
        "web development",
        "backend"
    ]

    skills = []

    for skill in known_skills:
        if skill in text.lower():
            skills.append(skill)

    return skills


def recommend_courses(skills, top_n=3):

    skill_embeddings = model.encode(skills)

    user_vector = np.mean(skill_embeddings, axis=0)

    scores = cosine_similarity(
        [user_vector],
        course_embeddings
    )[0]

    results = courses.copy()
    results["score"] = scores

    results = results.sort_values(
        by="score",
        ascending=False
    ).head(top_n)

    results["explanation"] = "Recommended based on similarity with your skills"

    return results