AHTX - AI-Powered Competitive Programming Tags & Methods Predictor
A robust, full-stack machine learning system designed to automate multi-label classification for competitive programming problem descriptions, predicting relevant tags and solution methods instantly.

🚀 Key Features
🛠️ Backend (server.py)
FastAPI Powered: Built with FastAPI and Uvicorn with auto-reload enabled for a seamless development and testing workflow.

Machine Learning Core: Utilizes a baseline dataset (problems_dataset.csv) processed through TF-IDF Vectorization and Logistic Regression via MultiOutputClassifier, optimized with a probability threshold of 0.40 for high precision.

Active Learning Loop: Features an automated feedback pipeline that dynamically accepts user corrections, applies data oversampling (3x repetition), and instantly triggers model retraining on the fly.

📱 Frontend (frontend/)
Flutter Framework: Developed using Flutter with Hot Reload support, featuring a sleek, responsive, and modern dark user interface.

Smart UI Components: Organizes master lists of tags and methods using case-insensitively sorted alphabetical keys for efficient navigation.

Interactive Control: Leverages interactive FilterChips and custom text inputs, allowing users to toggle, add, or remove predictions effortlessly during the feedback and review workflow.

📂 Project Structure
Plaintext
├── frontend/             # Flutter application source code
├── server.py             # FastAPI backend server & ML logic
├── problems_dataset.csv  # Base training dataset for problems
├── vectorizer.pkl        # Serialized TF-IDF vectorizer
├── mlb_tags.pkl          # MultiLabelBinarizer for tags
├── mlb_methods.pkl       # MultiLabelBinarizer for methods
├── problem_model.pkl     # Trained Logistic Regression multi-output model
└── .gitignore            # Git ignore rules for Python & Flutter caches
⚙️ Getting Started & Installation
1. Clone the Repository
Bash
git clone https://github.com/YOUR_USERNAME/AHTX-Tags-Predictor.git
cd AHTX-Tags-Predictor
2. Run the FastAPI Backend
Make sure you have Python installed, then install dependencies and run the server:

Bash
pip install fastapi uvicorn scikit-learn pandas joblib
uvicorn server:app --reload
3. Run the Flutter Frontend
Navigate to the frontend directory, get dependencies, and run the app:

Bash
cd frontend
flutter pub get
flutter run
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

👤 Author
AHTX
