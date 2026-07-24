from flask import Flask, render_template, request, session, redirect, url_for
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

@app.route("/certificate-guide")
def certificate_guide():
    return render_template("certificate_guide.html")

def parse_schemes(raw_text: str) -> list:
    schemes = []
    blocks = raw_text.split("---")
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        scheme = {"id": i}
        lines = block.split("\n")
        line_idx = 0
        
        field_labels = ["SCHEME:", "WHAT YOU GET:", "MALAYALAM:", "DO YOU QUALIFY:", "DOCUMENTS NEEDED:", "NEXT STEP:"]
        
        while line_idx < len(lines):
            line = lines[line_idx]
            
            if line.startswith("SCHEME:"):
                scheme["scheme"] = line.replace("SCHEME:", "").strip()
            elif line.startswith("WHAT YOU GET:"):
                scheme["what_you_get"] = line.replace("WHAT YOU GET:", "").strip()
            elif line.startswith("MALAYALAM:"):
                scheme["benefit_ml"] = line.replace("MALAYALAM:", "").strip()
            elif line.startswith("DO YOU QUALIFY:"):
                scheme["qualify"] = line.replace("DO YOU QUALIFY:", "").strip()
            elif line.startswith("DOCUMENTS NEEDED:"):
                content_lines = []
                first_line = line.replace("DOCUMENTS NEEDED:", "").strip()
                if first_line:
                    content_lines.append(first_line)
                line_idx += 1
                # Collect subsequent lines until we hit another field label
                while line_idx < len(lines):
                    next_line = lines[line_idx]
                    if any(next_line.startswith(label) for label in field_labels):
                        break
                    content_lines.append(next_line.rstrip())
                    line_idx += 1
                scheme["documents"] = "\n".join(content_lines).strip()
                continue
            elif line.startswith("NEXT STEP:"):
                content_lines = []
                first_line = line.replace("NEXT STEP:", "").strip()
                if first_line:
                    content_lines.append(first_line)
                line_idx += 1
                # Collect subsequent lines until we hit another field label
                while line_idx < len(lines):
                    next_line = lines[line_idx]
                    if any(next_line.startswith(label) for label in field_labels):
                        break
                    content_lines.append(next_line.rstrip())
                    line_idx += 1
                scheme["next_step"] = "\n".join(content_lines).strip()
                continue
            
            line_idx += 1
        
        if scheme.get("scheme"):
            schemes.append(scheme)
    return schemes

if __name__ == "__main__":
    app.run(debug=True)