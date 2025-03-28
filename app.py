from flask import Flask, render_template, request, make_response, url_for
from flask_mail import Mail, Message
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

# ✅ Add the checklist questions
questions = [
    # Data Protection & Confidentiality
    "Do you regularly back up client records and scheduling data?",
    "Are backups stored in a secure, HIPAA-compliant location?",
    "Are backups tested regularly to ensure they can be restored?",

    # Access Control
    "Are strong passwords required for all systems accessing client data?",
    "Is multi-factor authentication (MFA) used for systems like EHRs or cloud storage?",
    "Are accounts for former staff disabled or removed promptly?",

    # Incident Response Readiness
    "Do you have a written incident response plan in place (e.g., for ransomware or data breaches)?",
    "Have staff been briefed on what to do in case of a data breach?",
    "Do you know who to contact if there's a cybersecurity incident affecting client care?",

    # System Security
    "Are staff computers and mobile devices protected with up-to-date security software?",
    "Is your Wi-Fi secured with strong encryption (WPA2 or WPA3)?",
    "Is your mental health EHR or client management software updated regularly?",

    # Continuity of Care Planning
    "Do you have a way to maintain access to key client info during an outage?",
    "Is there a secure contact list of staff and emergency contacts available offline?",
    "Have roles and responsibilities been defined for crisis situations?",

    # Staff Training & Awareness
    "Have staff received cybersecurity and HIPAA compliance training in the last year?",
    "Are staff trained to recognize phishing attempts or social engineering?",
    "Is there a clear way for staff to report suspicious emails or activity?"
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


