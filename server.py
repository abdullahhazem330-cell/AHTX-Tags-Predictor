from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import os

app = FastAPI()

MASTER_TAGS = [
    "Arrays", "Graphs", "Dynamic Programming", "Greedy", "Sorting", 
    "Math", "Shortest Path", "Trees", "Network Flow", "Strings", 
    "Binary Search", "Number Theory", "Combinatorics", "Geometry", 
    "Bit Manipulation", "Two Pointers", "Stack", "Queue", "Heap",
    "Brute Force", "Backtracking", "Hashing", "Intervals", "Matrix",
    "Simulation", "Game Theory", "String Algorithms", "Disjoint Set",
    "Segment Tree", "Fenwick Tree", "Trie", "Suffix Array"
]

MASTER_METHODS = [
    "Kadane Algorithm", "Memoization", "Prefix Sum", "BFS", "DFS", 
    "Dijkstra", "Bellman-Ford", "Floyd-Warshall", "Binary Search", 
    "DP", "Greedy Choice", "Sorting", "Matrix Exponentiation", 
    "Recursion", "Traversal", "Tarjan", "Ford-Fulkerson", 
    "Priority Queue", "Negative Cycles", "Two Pointers", "Sliding Window",
    "Backtracking", "Brute Force Search", "Bitmasking", "Hashing",
    "Disjoint Set Union", "Union-Find", "Segment Tree Range Update",
    "KMP Algorithm", "Rabin-Karp", "Eulerian Path", "Topological Sort",
    "Prime Sieve", "Modular Arithmetic", "GCD/LCM", "Game Theory Grundy"
]

def get_all_unique_labels():
    file_path = 'problems_dataset.csv'
    if not os.path.exists(file_path):
        return sorted(list(MASTER_TAGS), key=str.lower), sorted(list(MASTER_METHODS), key=str.lower)
    
    df = pd.read_csv(file_path)
    
    all_tags = set(MASTER_TAGS)
    for tags_str in df['tags'].dropna():
        for t in str(tags_str).split(','):
            if t.strip():
                all_tags.add(t.strip())
                
    all_methods = set(MASTER_METHODS)
    for methods_str in df['methods'].dropna():
        for m in str(methods_str).split(','):
            if m.strip():
                all_methods.add(m.strip())
                
    return sorted(list(all_tags), key=str.lower), sorted(list(all_methods), key=str.lower)

def train_and_save_model():
    file_path = 'problems_dataset.csv'
    if not os.path.exists(file_path):
        df_init = pd.DataFrame({
            'problem_text': ["Given an array of integers, find the maximum sum of a contiguous subarray using dynamic programming."],
            'tags': ["Dynamic Programming, Arrays"],
            'methods': ["Kadane Algorithm, Memoization"]
        })
        df_init.to_csv(file_path, index=False)

    df = pd.read_csv(file_path)
    df.dropna(subset=['problem_text', 'tags', 'methods'], inplace=True)
    df.drop_duplicates(subset=['problem_text'], keep='last', inplace=True)
    df.to_csv(file_path, index=False)
    
    X_text = df['problem_text'].fillna('')
    
    y_tags_raw = df['tags'].apply(lambda x: [t.strip() for t in str(x).split(',') if t.strip()])
    mlb_tags = MultiLabelBinarizer()
    y_tags = mlb_tags.fit_transform(y_tags_raw)
    
    y_methods_raw = df['methods'].apply(lambda x: [m.strip() for m in str(x).split(',') if m.strip()])
    mlb_methods = MultiLabelBinarizer()
    y_methods = mlb_methods.fit_transform(y_methods_raw)
    
    y_combined = np.hstack((y_tags, y_methods))
    
    vectorizer = TfidfVectorizer(min_df=1, stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(X_text)
    
    base_model = LogisticRegression(C=5.0, max_iter=1000)
    model = MultiOutputClassifier(base_model)
    model.fit(X, y_combined)
    
    joblib.dump(model, 'problem_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(mlb_tags, 'mlb_tags.pkl')
    joblib.dump(mlb_methods, 'mlb_methods.pkl')
    
    return model, vectorizer, mlb_tags, mlb_methods

model, vectorizer, mlb_tags, mlb_methods = train_and_save_model()

class ProblemRequest(BaseModel):
    text: str

class FeedbackRequest(BaseModel):
    text: str
    true_tags: str = ""
    true_methods: str = ""

@app.post("/predict")
def predict_problem(item: ProblemRequest):
    X_new = vectorizer.transform([item.text])
    probas = model.predict_proba(X_new)
    
    n_tags = len(mlb_tags.classes_)
    predicted_tags = []
    threshold = 0.40
    
    for i, class_proba in enumerate(probas[:n_tags]):
        if class_proba[0][1] >= threshold:
            predicted_tags.append(mlb_tags.classes_[i])
            
    predicted_methods = []
    for i, class_proba in enumerate(probas[n_tags:]):
        if class_proba[0][1] >= threshold:
            predicted_methods.append(mlb_methods.classes_[i])
            
    all_t, all_m = get_all_unique_labels()
            
    return {
        "predicted_tags": predicted_tags,
        "predicted_methods": predicted_methods,
        "can_solve": len(predicted_tags) > 0 or len(predicted_methods) > 0,
        "all_tags": all_t,
        "all_methods": all_m
    }

@app.post("/feedback")
def save_feedback(item: FeedbackRequest):
    global model, vectorizer, mlb_tags, mlb_methods
    
    file_path = 'problems_dataset.csv'
    
    clean_text = item.text.strip().replace('"', '""')
    clean_tags = item.true_tags.strip().replace('"', '""')
    clean_methods = item.true_methods.strip().replace('"', '""')
    
    # لو المستخدم نسى يبعت حاجة في خانة، بنحط افتراضي عشان ما يعلقش
    if not clean_tags:
        clean_tags = "Arrays"
    if not clean_methods:
        clean_methods = "Brute Force"
    
    with open(file_path, 'a', encoding='utf-8') as f:
        for _ in range(3):
            f.write(f'"{clean_text}","{clean_tags}","{clean_methods}"\n')
    
    model, vectorizer, mlb_tags, mlb_methods = train_and_save_model()
    
    return {"status": "success", "message": "Feedback integrated securely!"}