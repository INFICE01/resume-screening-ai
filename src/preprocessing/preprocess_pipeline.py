import os
from parser import load_text_files
from text_cleaner import clean_text

# Define paths
RESUME_RAW_PATH = "../../data/raw/resumes/"
JD_RAW_PATH = "../../data/raw/job_descriptions/"
PROCESSED_RESUME_PATH = "../../data/processed/resumes/"
PROCESSED_JD_PATH = "../../data/processed/job_descriptions/"

# Ensure processed folders exist
os.makedirs(PROCESSED_RESUME_PATH, exist_ok=True)
os.makedirs(PROCESSED_JD_PATH, exist_ok=True)

def preprocess_and_save(data_dict, save_path):
    """
    Cleans text data and saves each file as cleaned .txt
    """
    for filename, content in data_dict.items():
        cleaned_text = clean_text(content)
        save_file = os.path.join(save_path, filename)
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

def main():
    # Load raw resumes and job descriptions
    resumes = load_text_files(RESUME_RAW_PATH)
    job_descriptions = load_text_files(JD_RAW_PATH)
    
    # Preprocess and save
    preprocess_and_save(resumes, PROCESSED_RESUME_PATH)
    preprocess_and_save(job_descriptions, PROCESSED_JD_PATH)
    
    print(f"Processed {len(resumes)} resumes -> {PROCESSED_RESUME_PATH}")
    print(f"Processed {len(job_descriptions)} job descriptions -> {PROCESSED_JD_PATH}")

if __name__ == "__main__":
    main()
