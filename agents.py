from langchain.tools import tool

from database import get_user_skills
from recommender import recommend_courses


@tool
def skill_agent(user_id: int):
    """Get user skills from the database."""

    return get_user_skills(user_id)


@tool
def recommendation_agent(skills: list[str]):
    """Recommend courses based on user skills."""

    results = recommend_courses(skills)

    courses = []

    for _, course in results.iterrows():

        courses.append({
            "title": course["title"],
            "score": round(float(course["score"]), 3)
        })

    return courses