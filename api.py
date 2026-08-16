from flask import Flask, request, jsonify, render_template

from database import get_user_skills
from recommender import recommend_courses, extract_skills


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    user_id = data.get("user_id")
    user_text = data.get("user_text")


    if user_id:
        skills = get_user_skills(user_id)

    elif user_text:
        skills = extract_skills(user_text)

    else:
        return jsonify({"error": "Enter user id or text"}), 400


    if not skills:
      return jsonify({
        " error": "No known skills found. Try Python, SQL, machine learning, or deep learning."
    }), 404


    recommendations = recommend_courses(skills)

    courses = []

    for _, course in recommendations.iterrows():

        courses.append({
            "title": course["title"],
            "score": round(float(course["score"]), 3),
            "explanation": course["explanation"]
        })


    return jsonify({
        "extracted_skills": skills,
        "recommended_courses": courses
    })


if __name__ == "__main__":
    app.run(debug=True)