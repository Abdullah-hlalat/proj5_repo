from flask import Flask, request, jsonify

from database import get_user_skills
from recommender import recommend_courses


app = Flask(__name__)


@app.route("/api/recommend", methods=["POST"])
def recommend():

    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    skills = get_user_skills(user_id)

    if not skills:
        return jsonify({"error": "User has no skills"}), 404

    recommendations = recommend_courses(skills)

    courses = []

    for _, course in recommendations.iterrows():
        courses.append({
            "title": course["title"],
            "score": round(float(course["score"]), 3),
            "explanation": course["explanation"]
        })

    return jsonify({
        "user_id": user_id,
        "extracted_skills": skills,
        "recommended_courses": courses
    })


if __name__ == "__main__":
    app.run(debug=True)