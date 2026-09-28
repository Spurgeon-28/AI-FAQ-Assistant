from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load FAQ data
with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


def find_answer(question):
    question = question.lower()

    best_match = None
    best_score = 0

    for faq in faqs:
        score = 0

        for keyword in faq["keywords"]:
            if keyword.lower() in question:
                score += 1

        if score > best_score:
            best_score = score
            best_match = faq["answer"]

    if best_match:
        return best_match

    return (
        "Sorry, I couldn't find an answer to that question. "
        "Please ask about Naan Mudhalvan courses, registration, "
        "eligibility, training, certificates, or placements."
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question."
        })

    answer = find_answer(question)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)