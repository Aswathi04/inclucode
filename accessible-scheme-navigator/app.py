from flask import Flask, render_template, request, session
from rag import get_schemes
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    disability = request.form.get("disability")
    age = request.form.get("age")
    district = request.form.get("district")

    session["disability"] = disability
    session["age"] = age
    session["district"] = district

    raw_result = get_schemes(disability, age, district)
    schemes = parse_schemes(raw_result)
    session["schemes"] = schemes

    return render_template("results.html",
                           schemes=schemes,
                           disability=disability,
                           age=age,
                           district=district)

@app.route("/detail/<int:scheme_id>")
def detail(scheme_id):
    schemes = session.get("schemes", [])
    if scheme_id < len(schemes):
        return render_template("detail.html", scheme=schemes[scheme_id])
    return "Scheme not found", 404

def parse_schemes(raw_text: str) -> list:
    schemes = []
    blocks = raw_text.split("---")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        scheme = {}
        for line in block.split("\n"):
            if line.startswith("SCHEME:"):
                scheme["name"] = line.replace("SCHEME:", "").strip()
            elif line.startswith("WHAT YOU GET:"):
                scheme["benefit"] = line.replace("WHAT YOU GET:", "").strip()
            elif line.startswith("MALAYALAM:"):
                scheme["benefit_ml"] = line.replace("MALAYALAM:", "").strip()
            elif line.startswith("DO YOU QUALIFY:"):
                val = line.replace("DO YOU QUALIFY:", "").strip().lower()
                scheme["status"] = "qualify" if val.startswith("yes") else "check"
                scheme["status_reason"] = val
            elif line.startswith("DOCUMENTS NEEDED:"):
                scheme["documents"] = line.replace("DOCUMENTS NEEDED:", "").strip()
            elif line.startswith("NEXT STEP:"):
                scheme["next_step"] = line.replace("NEXT STEP:", "").strip()
        if scheme.get("name"):
            schemes.append(scheme)
    return schemes

if __name__ == "__main__":
    app.run(debug=True)