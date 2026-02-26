import os

def load_documents(folder_path):
    documents = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".txt", ".py", ".md")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        documents.append({
                            "content": content,
                            "source": file_path
                        })
                except:
                    continue

    return documents