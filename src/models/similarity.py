import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Paths to processed data
PROCESSED_RESUME_PATH = "../../data/processed/resumes/"
PROCESSED_JD_PATH = "../../data/processed/job_descriptions/"
OUTPUT_PATH = "../../data/sample_outputs/"

os.makedirs(OUTPUT_PATH, exist_ok=True)

def load_processed_text(folder_path):
    """
    Loads cleaned text files from processed folder
    Returns a dict: {filename: text}
    """
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data[filename] = f.read()
    return data

def compute_similarity(resumes_dict, jds_dict):
    """
    Computes cosine similarity between resumes and job descriptions
    Returns a pandas DataFrame with resume scores for each JD
    """
    vectorizer = TfidfVectorizer()

    # Flatten data for vectorization
    all_texts = list(resumes_dict.values()) + list(jds_dict.values())
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    resume_matrix = tfidf_matrix[:len(resumes_dict)]
    jd_matrix = tfidf_matrix[len(resumes_dict):]

    results = {}

    for i, jd_name in enumerate(jds_dict.keys()):
        jd_vector = jd_matrix[i]
        # Compute cosine similarity with all resumes
        cos_scores = cosine_similarity(resume_matrix, jd_vector)
        # Flatten and store as dict: {resume_name: score}
        scores_dict = {resume_name: float(score) for resume_name, score in zip(resumes_dict.keys(), cos_scores.flatten())}
        # Sort by score descending
        sorted_scores = dict(sorted(scores_dict.items(), key=lambda item: item[1], reverse=True))
        results[jd_name] = sorted_scores

    return results

def save_results(results):
    """
    Saves ranking results to CSV files in sample_outputs/
    """
    for jd_name, scores_dict in results.items():
        df = pd.DataFrame(list(scores_dict.items()), columns=['Resume', 'Similarity_Score'])
        output_file = os.path.join(OUTPUT_PATH, f"ranking_{jd_name}")
        # Remove .txt from JD name if exists
        if output_file.endswith(".txt"):
            output_file = output_file.replace(".txt", "")
        df.to_csv(output_file + ".csv", index=False)
    print(f"Ranking results saved to {OUTPUT_PATH}")

def main():
    resumes = load_processed_text(PROCESSED_RESUME_PATH)
    jds = load_processed_text(PROCESSED_JD_PATH)
    results = compute_similarity(resumes, jds)
    save_results(results)

if __name__ == "__main__":
    main()
