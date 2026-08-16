from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from database import get_user_skills, log_recommendation
from recommender import recommend_courses


class State(TypedDict):
    user_id: int
    skills: list[str]
    recommendations: list


def get_skills(state):

    skills = get_user_skills(
        state["user_id"]
    )

    return {
        "skills": skills
    }


def get_recommendations(state):

    if not state["skills"]:

        return {
            "recommendations": []
        }


    results = recommend_courses(
        state["skills"]
    )

    recommendations = []


    for _, course in results.iterrows():

        score = round(
            float(course["score"]),
            3
        )

        recommendations.append({
            "id": int(course["id"]),
            "title": course["title"],
            "score": score
        })


        log_recommendation(
            state["user_id"],
            int(course["id"]),
            score
        )


    return {
        "recommendations": recommendations
    }


builder = StateGraph(State)

builder.add_node(
    "get_skills",
    get_skills
)

builder.add_node(
    "recommend",
    get_recommendations
)


builder.add_edge(
    START,
    "get_skills"
)

builder.add_edge(
    "get_skills",
    "recommend"
)

builder.add_edge(
    "recommend",
    END
)


workflow = builder.compile()