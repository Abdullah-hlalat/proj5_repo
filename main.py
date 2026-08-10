from recommender import extract_skills, recommend_courses


user_input = input("Enter your interests and skills: ")

skills = extract_skills(user_input)

print("\nExtracted Skills:")
print(skills)

if skills:

    recommendations = recommend_courses(skills)

    print("\nRecommended Courses:")

    for _, course in recommendations.iterrows():
        print(
           course["title"],
           "- Score:",
           round(course["score"], 3),
           "-",
           course["explanation"]
    )

else:

    print("No skills found.")