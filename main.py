import os
import nltk
from src.utils.skill_extractor import calculate_skill_match
from src.preprocessing.parser import load_text_files
from src.preprocessing.text_cleaner import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')


RESUME_RAW_PATH = "data/raw/resumes/"
JD_RAW_PATH = "data/raw/job_descriptions/"
PROCESSED_RESUME_PATH = "data/processed/resumes/"
PROCESSED_JD_PATH = "data/processed/job_descriptions/"
OUTPUT_PATH = "data/sample_outputs/"

os.makedirs(PROCESSED_RESUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_JD_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)


def preprocess_and_save(data_dict, save_path):
    for filename, content in data_dict.items():
        cleaned_text = clean_text(content)
        save_file = os.path.join(save_path, filename)
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)


# Load raw data
resumes_raw = load_text_files(RESUME_RAW_PATH)
jds_raw = load_text_files(JD_RAW_PATH)

# Preprocess and save
preprocess_and_save(resumes_raw, PROCESSED_RESUME_PATH)
preprocess_and_save(jds_raw, PROCESSED_JD_PATH)

# Load processed data
resumes_processed = load_text_files(PROCESSED_RESUME_PATH)
jds_processed = load_text_files(PROCESSED_JD_PATH)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
all_texts = list(resumes_processed.values()) + list(jds_processed.values())
tfidf_matrix = vectorizer.fit_transform(all_texts)

resume_matrix = tfidf_matrix[:len(resumes_processed)]
jd_matrix = tfidf_matrix[len(resumes_processed):]

resume_names = list(resumes_processed.keys())
resume_texts = list(resumes_processed.values())

# Hybrid Ranking for Each JD
for i, jd_name in enumerate(jds_processed.keys()):
    jd_vector = jd_matrix[i]
    jd_text = list(jds_processed.values())[i]

    cos_scores = cosine_similarity(resume_matrix, jd_vector).flatten()

    results = []

    for idx, resume_name in enumerate(resume_names):
        semantic_score = float(cos_scores[idx])

        # Skill-based scoring
        skill_score, matched, missing = calculate_skill_match(
            resume_texts[idx],
            jd_text
        )

        # Hybrid Final Score
        final_score = 0.6 * skill_score + 0.4 * semantic_score

        results.append({
            "Resume": resume_name,
            "Semantic_Score": round(semantic_score, 3),
            "Skill_Match_Score": round(skill_score, 3),
            "Final_Score": round(final_score, 3),
            "Matched_Skills": ", ".join(matched),
            "Missing_Skills": ", ".join(missing)
        })

    # Sort by Final Score
    results = sorted(results, key=lambda x: x["Final_Score"], reverse=True)

    df = pd.DataFrame(results)

    output_file = os.path.join(
        OUTPUT_PATH,
        f"ranking_{jd_name.replace('.txt','')}.csv"
    )

    df.to_csv(output_file, index=False)

print("Hybrid ranking completed. Check data/sample_outputs/")
