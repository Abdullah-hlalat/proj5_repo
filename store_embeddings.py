from sentence_transformers import SentenceTransformer

from database import (
    engine,
    courses,
    embeddings,
    save_embedding
)


model = SentenceTransformer("all-MiniLM-L6-v2")


with engine.connect() as conn:

    course_rows = conn.execute(
        courses.select()
    ).fetchall()

    existing = conn.execute(
        embeddings.select()
    ).first()


if existing:

    print("Course embeddings already stored")

else:

    for course in course_rows:

        vector = model.encode(
            course.description
        )

        save_embedding(
            course.id,
            vector
        )

    print("Course embeddings stored")