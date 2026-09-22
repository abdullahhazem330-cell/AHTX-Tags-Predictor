import joblib

# تحميل الموديل والأداة
loaded_model = joblib.load('problem_model.pkl')
loaded_vectorizer = joblib.load('vectorizer.pkl')

# تجربة مسألة جديدة
new_problem = ["Given a weighted graph with negative edge weights, find the shortest path from the source using Bellman-Ford algorithm."]

print("--- نص المسألة الجديدة ---")
print(new_problem[0])

X_new = loaded_vectorizer.transform(new_problem)
prediction = loaded_model.predict(X_new)

print("\nالـ Tag المتوقع من الموديل: 🎯", prediction[0])