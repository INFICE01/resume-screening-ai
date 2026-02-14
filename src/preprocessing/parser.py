import os

def load_text_files(folder_path):
    """
    Loads all .txt files from the given folder
    Returns a dictionary: {filename: file_content}
    """
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                data[filename] = text
    return data

# Example usage
if __name__ == "__main__":
    resumes = load_text_files("../../data/raw/resumes/")
    for fname, content in resumes.items():
        print(fname, ":", content[:100], "...")
