import re

knowledge_base = {
    "subjects": "We offer Mathematics, English, Science, and History.",
    "admission": "Admissions open in August and close in October each year.",
    "hours": "School operates from 8:00 AM to 3:00 PM, Monday through Friday.",
    "uniform": "Students wear navy blue and white uniforms from Monday to Thursday, and sportswear on Friday.",
    "location": "The school is located in the downtown academic district.",
    "default": "I'm not sure about that — could you ask something about school activities, programs, or admissions?"
}

keyword_map = {
    "subjects": ["subject", "subjects", "math", "mathematics", "english", "science", "history"],
    "admission": ["admission", "admissions", "apply", "apply", "application", "register", "enroll", "enrollment"],
    "hours": ["hour", "hours", "open", "close", "time", "schedule", "operates", "operation"],
    "uniform": ["uniform", "uniforms", "dress", "clothing", "attire", "sportswear", "sports"],
    "location": ["location", "located", "where", "address", "campus", "district"]
}

def preprocess_text(text):
    return re.findall(r"\b\w+\b", text.lower())


def classify_intent(tokens):
    scores = {k: 0 for k in knowledge_base}
    for token in tokens:
        for intent, keywords in keyword_map.items():
            if token in keywords:
                scores[intent] += 1
    best_intent = max(scores, key=scores.get)
    return best_intent if scores[best_intent] > 0 else "default"


def generate_response(user_input):
    tokens = preprocess_text(user_input)
    intent = classify_intent(tokens)
    return knowledge_base[intent]
