import json

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, ForeignKey, select
)

engine = create_engine("sqlite:///project5.db")
metadata = MetaData()


users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)

skills = Table(
    "skills", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)

courses = Table(
    "courses", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String)
)

user_skills = Table(
    "user_skills", metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("skill_id", ForeignKey("skills.id"))
)

embeddings = Table(
    "embeddings", metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", ForeignKey("courses.id")),
    Column("embedding", String)
)

recommendation_logs = Table(
    "recommendation_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("course_id", ForeignKey("courses.id")),
    Column("score", Float)
)

metadata.create_all(engine)


with engine.begin() as conn:
    if not conn.execute(users.select()).first():

        conn.execute(users.insert(), [
            {"id": 1, "name": "Abdullah"},
            {"id": 2, "name": "Haya"}
        ])

        conn.execute(skills.insert(), [
            {"id": 1, "name": "python"},
            {"id": 2, "name": "machine learning"},
            {"id": 3, "name": "data analysis"},
            {"id": 4, "name": "sql"},
            {"id": 5, "name": "deep learning"},
            {"id": 6, "name": "web development"},
            {"id": 7, "name": "backend"}
        ])

        conn.execute(courses.insert(), [
            {"id": 1, "title": "Python Basics",
             "description": "Learn basic Python programming"},

            {"id": 2, "title": "Data Analysis with Python",
             "description": "Learn data analysis using Python and pandas"},

            {"id": 3, "title": "Machine Learning Fundamentals",
             "description": "Learn machine learning concepts using Python"},

            {"id": 4, "title": "SQL Basics",
             "description": "Learn SQL and relational databases"},

            {"id": 5, "title": "Deep Learning Basics",
             "description": "Learn neural networks and deep learning"},

            {"id": 6, "title": "Web Development Basics",
             "description": "Learn HTML CSS JavaScript and backend development"}
        ])

        conn.execute(user_skills.insert(), [
            {"user_id": 1, "skill_id": 1},
            {"user_id": 1, "skill_id": 2},
            {"user_id": 2, "skill_id": 3},
            {"user_id": 2, "skill_id": 4}
        ])


def get_user_skills(user_id):
    with engine.connect() as conn:
        query = (
            select(skills.c.name)
            .join(user_skills)
            .where(user_skills.c.user_id == user_id)
        )

        return [row.name for row in conn.execute(query)]


def save_embedding(course_id, vector):
    with engine.begin() as conn:
        conn.execute(
            embeddings.insert(),
            {
                "course_id": course_id,
                "embedding": json.dumps(vector.tolist())
            }
        )


def get_courses_with_embeddings():
    with engine.connect() as conn:
        query = select(
            courses.c.id,
            courses.c.title,
            courses.c.description,
            embeddings.c.embedding
        ).join(embeddings)

        rows = conn.execute(query)

        return [
            {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "embedding": json.loads(row.embedding)
            }
            for row in rows
        ]
    

def log_recommendation(user_id, course_id, score):
    with engine.begin() as conn:
        conn.execute(
            recommendation_logs.insert(),
            {
                "user_id": user_id,
                "course_id": course_id,
                "score": score
            }
        )