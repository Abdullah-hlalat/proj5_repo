from database import get_user_skills
from recommender import recommend_courses


user_id = int(input("Enter user ID: "))

skills = get_user_skills(user_id)

print("\nUser Skills:")
print(skills)

if skills:
    recommendations = recommend_courses(skills)

    print("\nRecommended Courses:")

    for _, course in recommendations.iterrows():
        print(
            course["title"],
            "- Score:",
            round(course["score"], 3)
        )
else:
    print("User has no skills.")