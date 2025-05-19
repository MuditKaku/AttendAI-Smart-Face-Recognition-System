from deepface import DeepFace
from students import STUDENTS
import numpy as np

THRESHOLD = 0.65
MODEL_NAME = "Facenet512"

KNOWN_FACES = {
    "Vatsalya Jain": "known_faces/vatsalya.jpg",
    "Mudit Jain": "known_faces/mudit.jpg",
    "Ronit Raghuwanshi": "known_faces/ronit.jpg",
    "Monishka Paul": "known_faces/monishka.jpg",
    "Tanishk Jain": "known_faces/tanishk.jpg"
}

print("⚙️ Generating embeddings...")
known_embeddings = {}

for name, path in KNOWN_FACES.items():
    try:
        rep = DeepFace.represent(img_path=path, model_name=MODEL_NAME, enforce_detection=False)
        embedding = np.array(rep[0]["embedding"])
        known_embeddings[name] = embedding
        print(f"✅ Embedded: {name}")
    except Exception as e:
        print(f"❌ Failed to embed {name}: {e}")

print("✅ All embeddings ready.\n")


def verify_face(frame):
    try:
        rep = DeepFace.represent(frame, model_name=MODEL_NAME, enforce_detection=False)
        embedding = np.array(rep[0]["embedding"])

        best_match = None
        best_similarity = -1

        for name, known_emb in known_embeddings.items():
            similarity = np.dot(embedding, known_emb) / (np.linalg.norm(embedding) * np.linalg.norm(known_emb))

            if similarity > THRESHOLD and similarity > best_similarity:
                best_match = name
                best_similarity = similarity

        if best_match:
            info = STUDENTS.get(best_match, {})
            return best_match, info
        else:
            return "Unknown", {}

    except Exception as e:
        print(f"❌ Recognition error: {e}")
        return "Unknown", {}
