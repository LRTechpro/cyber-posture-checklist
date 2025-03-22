from flask import Flask, render_template, request, make_response, url_for
from flask_mail import Mail, Message
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

# ✅ Add the checklist questions
questions = [
    "Do you have recent backups of your critical data?",
    "Are your backups stored off-site or in the cloud?",
    "Are backups tested regularly to ensure they work?",
    "Do you use strong, unique passwords for all accounts?",
    "Is multi-factor authentication (MFA) enabled for key systems?",
    "Are inactive or former user accounts regularly removed?",
    "Do you have a basic incident response plan in writing?",
    "Have key team members been briefed on what to do during a cyber incident?",
    "Do you know who to contact for IT or cybersecurity support during a crisis?",
    "Are your devices protected with up-to-date antivirus or endpoint protection?",
    "Is your Wi-Fi network secured with a strong password and encryption (WPA2 or WPA3)?",
    "Are critical software and systems kept up to date with patches?",
    "Is there a contact list of key personnel and emergency contacts?",
    "Do you have a plan to keep services running if your main office/location is unavailable?",
    "Are responsibilities documented for who does what during a crisis?",
    "Have team members received any cybersecurity awareness training?",
    "Do employees know how to recognize phishing emails or suspicious links?",
    "Is there a point person or resource for reporting suspicious activity?"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answers = request.form
        score = sum(1 for q in questions if answers.get(q) == 'yes')

        if score >= 16:
            level = "LOW – Good posture and planning!"
        elif score >= 10:
            level = "MODERATE – Some gaps to close."
        else:
            level = "HIGH – Needs immediate attention!"

        return render_template('result.html', score=score, total=len(questions), level=level, answers=answers, questions=questions)

    return render_template('index.html', questions=questions)

@app.route('/download', methods=['POST'])
def download():
    answers = request.form
    score = sum(1 for q in questions if answers.get(q) == 'yes')

    if score >= 16:
        level = "LOW – Good posture and planning!"
    elif score >= 10:
        level = "MODERATE – Some gaps to close."
    else:
        level = "HIGH – Needs immediate attention!"

    rendered = render_template("pdf_template.html", answers=answers, questions=questions, score=score, level=level)
    
    from io import BytesIO
    from xhtml2pdf import pisa
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cyber_posture_report.pdf'
    return response


