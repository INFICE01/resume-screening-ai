 Resume Screening AI – Hybrid ATS Ranking System

An intelligent resume screening system that ranks resumes against job descriptions using a hybrid scoring approach combining NLP-based semantic similarity and skill-based weighted matching.




This project simulates an Applicant Tracking System (ATS) used by companies to automatically rank resumes based on their relevance to a job description.

The system uses:

- TF-IDF Vectorization for semantic text representation
- Cosine Similarity for ranking resumes
- Skill Extraction for domain-specific matching
- Hybrid Weighted Scoring for improved relevance

Final Score Formula:

Final Score = 0.6 × Skill Match Score + 0.4 × Semantic Similarity Score


- Resume preprocessing (tokenization, stopword removal, lemmatization)
- TF-IDF based text vectorization
- Cosine similarity ranking
- Skill extraction from resumes and job descriptions
- Explainable ranking output:
  - Semantic Score
  - Skill Match Score
  - Final Score
  - Matched Skills
  - Missing Skills
- CSV-based ranked output for each job description

---



resume-screening-ai/
│
├── main.py
├── data/
│ ├── raw/
│ ├── processed/
│ └── sample_outputs/
│
└── src/
├── preprocessing/
│ ├── parser.py
│ └── text_cleaner.py
├── models/
│ └── similarity.py
└── utils/
└── skill_extractor.py

Make sure you have Python 3.8+ installed.

Install dependencies using:
pip install -r requirements.txt

if you are installing manually, required libraries are:

- scikit-learn
- nltk
- pandas
- The following NLTK resources are required:

- punkt
- punkt_tab
- stopwords
- wordnet

They are automatically downloaded when running the project.

# IMP HOW TO RUN

1. Place resumes in:
data/raw/resumes/

2. Place job descriptions in:
data/raw/job_descriptions/

3. Run the project:
python main.py

4. Output CSV files will be generated in:
data/sample_outputs/


Each ranking CSV contains:

- Resume
- Semantic_Score
- Skill_Match_Score
- Final_Score
- Matched_Skills
- Missing_Skills
