from flask import Flask, render_template, request, session
from rag import get_schemes
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        schemes = session.get("schemes")
        if schemes is None:
            return redirect(url_for("index"))
        return render_template("results.html", schemes=schemes, profile=session.get("profile"))

    disability = request.form.get("disability", "").strip()
    age = request.form.get("age", "").strip()
    district = request.form.get("district", "").strip()

    if not disability or not age or not district:
        return render_template("index.html", error="Please fill in all fields.")

    raw_output = get_schemes(disability, age, district)
    schemes = parse_schemes(raw_output)

    session["schemes"] = schemes
    session["profile"] = {"disability": disability, "age": age, "district": district}

    return render_template("results.html", schemes=schemes, profile=session["profile"])

@app.route("/detail/<int:scheme_id>")
def detail(scheme_id):
    schemes = session.get("schemes", [])
    match = next((s for s in schemes if s.get("id") == scheme_id), None)
    if match:
        return render_template("detail.html", scheme=match)
    return "Scheme not found", 404

def parse_schemes(raw_text: str) -> list:
    schemes = []
    blocks = raw_text.split("---")
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        scheme = {"id": i}
        for line in block.split("\n"):
            if line.startswith("SCHEME:"):
                scheme["scheme"] = line.replace("SCHEME:", "").strip()
            elif line.startswith("WHAT YOU GET:"):
                scheme["what_you_get"] = line.replace("WHAT YOU GET:", "").strip()
            elif line.startswith("MALAYALAM:"):
                scheme["benefit_ml"] = line.replace("MALAYALAM:", "").strip()
            elif line.startswith("DO YOU QUALIFY:"):
                scheme["qualify"] = line.replace("DO YOU QUALIFY:", "").strip()
            elif line.startswith("DOCUMENTS NEEDED:"):
                scheme["documents"] = line.replace("DOCUMENTS NEEDED:", "").strip()
            elif line.startswith("NEXT STEP:"):
                scheme["next_step"] = line.replace("NEXT STEP:", "").strip()
        if scheme.get("scheme"):
            schemes.append(scheme)
    return schemes

if __name__ == "__main__":
    app.run(debug=True)