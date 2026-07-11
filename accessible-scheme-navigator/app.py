import os
import re
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from rag import get_schemes

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")


def parse_schemes(raw_text: str) -> list[dict]:
    """
    Parses get_schemes() output into a list of scheme dicts.
    Expected block format, separated by '---':

    SCHEME: ...
    WHAT YOU GET: ...
    MALAYALAM: ...
    DO YOU QUALIFY: ...
    DOCUMENTS NEEDED:
    1. ...
    2. ...
    NEXT STEP: ...
    """
    blocks = [b.strip() for b in raw_text.split("---") if b.strip()]
    schemes = []

    field_order = [
        ("SCHEME", "scheme"),
        ("WHAT YOU GET", "what_you_get"),
        ("MALAYALAM", "malayalam"),
        ("DO YOU QUALIFY", "qualify"),
        ("DOCUMENTS NEEDED", "documents_raw"),
        ("NEXT STEP", "next_step"),
    ]
    labels = [f[0] for f in field_order]

    for idx, block in enumerate(blocks):
        pattern = "|".join(re.escape(l) + r":" for l in labels)
        parts = re.split(f"({pattern})", block)

        data = {}
        current_key = None
        for part in parts:
            part_stripped = part.strip()
            if not part_stripped:
                continue
            matched_label = next(
                (label for label, key in field_order if part_stripped == f"{label}:"),
                None
            )
            if matched_label:
                current_key = dict(field_order)[matched_label]
            elif current_key:
                data[current_key] = data.get(current_key, "") + part_stripped + " "

        if "scheme" not in data:
            continue

        documents = []
        if "documents_raw" in data:
            for line in data["documents_raw"].splitlines():
                line = line.strip()
                line = re.sub(r"^\d+\.\s*", "", line)
                if line:
                    documents.append(line)

        schemes.append({
            "id": idx,
            "scheme": data.get("scheme", "").strip(),
            "what_you_get": data.get("what_you_get", "").strip(),
            "malayalam": data.get("malayalam", "").strip(),
            "qualify": data.get("qualify", "").strip(),
            "documents": documents,
            "next_step": data.get("next_step", "").strip(),
        })

    return schemes


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/results", methods=["POST"])
def results():
    disability = request.form.get("disability", "").strip()
    age = request.form.get("age", "").strip()
    district = request.form.get("district", "").strip()

    if not disability or not age or not district:
        return render_template("index.html", error="Please fill in all fields.")

    raw_output = get_schemes(disability, age, district)
    schemes = parse_schemes(raw_output)

    session["schemes"] = schemes
    session["profile"] = {"disability": disability, "age": age, "district": district}

    return render_template("results.html", schemes=schemes)


@app.route("/detail/<int:scheme_id>", methods=["GET"])
def detail(scheme_id):
    schemes = session.get("schemes", [])
    scheme = next((s for s in schemes if s["id"] == scheme_id), None)

    if scheme is None:
        return redirect(url_for("index"))

    return render_template("detail.html", scheme=scheme)


if __name__ == "__main__":
    app.run(debug=True)