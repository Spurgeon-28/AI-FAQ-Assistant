```python
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ---------------------------------------------------
# Load FAQ Knowledge Base
# ---------------------------------------------------

try:
    with open("faqs.json", "r", encoding="utf-8") as file:
        faqs = json.load(file)

except FileNotFoundError:
    faqs = []
    print("Warning: faqs.json was not found.")


# ---------------------------------------------------
# FAQ Matching Function
# ---------------------------------------------------

def find_answer(question):

    # Convert question to lowercase
    question = question.lower().strip()

    # Remove common punctuation
    punctuation = ".,!?;:'\"()[]{}"

    for char in punctuation:
        question = question.replace(char, " ")

    # Convert question into words
    question_words = set(question.split())

    best_match = None
    best_score = 0

    # Check every FAQ
    for faq in faqs:

        score = 0

        for keyword in faq.get("keywords", []):

            keyword = keyword.lower().strip()

            # -----------------------------------------
            # Exact phrase matching
            # -----------------------------------------

            if keyword in question:
                score += 3

            # -----------------------------------------
            # Individual word matching
            # -----------------------------------------

            keyword_words = set(keyword.split())

            matching_words = question_words.intersection(keyword_words)

            score += len(matching_words)

        # -----------------------------------------
        # Store the best FAQ match
        # -----------------------------------------

        if score > best_score:
            best_score = score
            best_match = faq.get("answer")


    # ------------------------------------------------
    # Return the best answer
    # ------------------------------------------------

    if best_match and best_score >= 2:
        return best_match


    # ------------------------------------------------
    # Fallback response
    # ------------------------------------------------

    return (
        "Sorry, I couldn't find a suitable answer to that question. "
        "Please try asking about Naan Mudhalvan courses, registration, "
        "eligibility, training, certificates, internships, placements, "
        "or career opportunities."
    )


# ---------------------------------------------------
# Home Page
# ---------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------------------------------------------
# Ask API
# ---------------------------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:

        # Get JSON data from the frontend
        data = request.get_json()

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

        print("Error:", error)

        return jsonify({
            "answer": "Sorry, something went wrong. Please try again."
        }), 500


# ---------------------------------------------------
# Run Flask Application
# ---------------------------------------------------

if __name__ == "__main__":

    print("---------------------------------------------")
    print(" Naan Mudhalvan AI FAQ Assistant")
    print("---------------------------------------------")
    print("Server running at: http://127.0.0.1:5000")
    print("---------------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
```
