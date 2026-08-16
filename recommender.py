import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database import get_courses_with_embeddings


model = SentenceTransformer("all-MiniLM-L6-v2")


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

    course_data = get_courses_with_embeddings()

    skill_embeddings = model.encode(skills)

    user_vector = np.mean(
        skill_embeddings,
        axis=0
    )

    results = []

    for course in course_data:

        score = cosine_similarity(
            [user_vector],
            [course["embedding"]]
        )[0][0]

        results.append({
            "id": course["id"],
            "title": course["title"],
            "score": score
        })

    results = pd.DataFrame(results)

    results = results.sort_values(
        by="score",
        ascending=False
    ).head(top_n)

    results["explanation"] = (
        "Recommended based on similarity with your skills"
    )

    return results