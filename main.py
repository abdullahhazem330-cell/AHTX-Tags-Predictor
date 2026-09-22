import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# 1. قراءة الداتا
df = pd.read_csv('problems_dataset.csv')
print("--- تم قراءة الداتا من الملف بنجاح! ---")
print(df)
print("\n" + "="*50 + "\n")

X_text = df['problem_text']
y = df['tag']

# 2. تحويل النصوص لـ TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_text)

# 3. تدريب الموديل
model = LogisticRegression()
model.fit(X, y)
print("تم تدريب الموديل على الملف الخارجي بنجاح! 🚀")

# 4. حفظ الموديل والـ Vectorizer
joblib.dump(model, 'problem_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("تم حفظ الموديل وأداة التحويل في ملفات على اللاب بنجاح! 💾")