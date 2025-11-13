from flask import Flask, request, jsonify
from docx import Document
from groq import Groq

app = Flask(__name__)

# Replace 
#KEY = ""
#client = Groq(KEY)


@app.route("/generate", methods=["POST"])
def generate_resume():
    try:
        data = request.json

        prompt = f"""
        Create a clean, professional resume in plain text format (no HTML or Markdown).
        Use proper indentation, section titles, and spacing.
        The format should look like a real resume.

        Include these details:
        Name: {data['name']}
        Email: {data['email']}
        Phone: {data['phone']}
        LinkedIn: {data['linkedin']}
        GitHub: {data['github']}

        Summary: {data['summary']}
        Education: {data['education']}
        Skills: {data['skills']}
        Technologies & Tools: {data['technologies']}
        Work/Internship Experience: {data['experience']}
        Awards & Certifications: {data['awards']}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        resume_text = response.choices[0].message.content.strip()
        return jsonify({"resume": resume_text})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/save", methods=["POST"])
def save_as_docx():
    data = request.json
    resume_text = data.get("resume", "")
    filename = "resume.docx"

    doc = Document()
    for line in resume_text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)
    return jsonify({"filename": filename})


if __name__ == "__main__":
    app.run(debug=True)
