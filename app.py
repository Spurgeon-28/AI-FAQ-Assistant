from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


# =========================================================
# LOAD FAQ KNOWLEDGE BASE
# =========================================================

try:
    with open("faqs.json", "r", encoding="utf-8") as file:
        faqs = json.load(file)

    print(f"Loaded {len(faqs)} FAQ entries successfully.")

except FileNotFoundError:
    faqs = []
    print("WARNING: faqs.json was not found.")

except json.JSONDecodeError:
    faqs = []
    print("WARNING: faqs.json contains invalid JSON.")


# =========================================================
# FAQ MATCHING FUNCTION
# =========================================================

def find_answer(question):

    # Convert question to lowercase
    question = question.lower().strip()

    # Remove punctuation
    punctuation = ".,!?;:'\"()[]{}"

    for char in punctuation:
        question = question.replace(char, " ")

    # Convert question into individual words
    question_words = set(question.split())

    best_match = None
    best_score = 0

    # Check every FAQ
    for faq in faqs:

        score = 0

        keywords = faq.get("keywords", [])

        for keyword in keywords:

            keyword = keyword.lower().strip()

            # ---------------------------------------------
            # Exact phrase matching
            # ---------------------------------------------

            if keyword in question:
                score += 3

            # ---------------------------------------------
            # Individual word matching
            # ---------------------------------------------

            keyword_words = set(keyword.split())

            matching_words = (
                question_words.intersection(keyword_words)
            )

            score += len(matching_words)

        # ---------------------------------------------
        # Store best matching FAQ
        # ---------------------------------------------

        if score > best_score:

            best_score = score

            best_match = faq.get("answer")


    # =====================================================
    # RETURN BEST ANSWER
    # =====================================================

    if best_match and best_score >= 2:
        return best_match


    # =====================================================
    # FALLBACK RESPONSE
    # =====================================================

    return (
        "Sorry, I couldn't find a suitable answer to that "
        "question. Please try asking about Naan Mudhalvan "
        "courses, registration, eligibility, training, "
        "certificates, internships, placements, or "
        "career opportunities."
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# ASK API
# =========================================================

@app.route("/ask", methods=["POST"])
def ask():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        # Handle missing JSON
        if not data:
            return jsonify({
                "answer": "Please enter a question."
            })

        # Get user's question
        question = data.get("question", "").strip()


        # ---------------------------------------------
        # Empty question check
        # ---------------------------------------------

        if not question:

            return jsonify({
                "answer": "Please enter a question."
            })


        # ---------------------------------------------
        # Find FAQ answer
        # ---------------------------------------------

        answer = find_answer(question)


        # ---------------------------------------------
        # Send response to frontend
        # ---------------------------------------------

        return jsonify({
            "question": question,
            "answer": answer
        })


    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "answer": (
                "Sorry, something went wrong. "
                "Please try again."
            )
        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("     NAAN MUDHALVAN AI FAQ ASSISTANT")
    print("==============================================")
    print("Server: http://127.0.0.1:5000")
    print("==============================================")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )