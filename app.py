from flask import Flask, render_template, request
from jinja2 import Template
import os  # Used for additional security warnings

app = Flask(__name__)

malicious_patterns = ["__", ".__"]

@app.route("/", methods=["GET", "POST"])
def function_route():
    if request.method == "POST":
        emailpre = request.form.get("emailpre")  # 🚨 User-controlled input
        
        if any(pattern in emailpre for pattern in malicious_patterns):
            result = "This is a malicious string"
        else:
            # 🚨 Vulnerable SSTI: Passing user input directly to Jinja2 Template
            template = Template(emailpre)  # 🚨 Bandit should flag this
            result = template.render()  # 🚨 This executes user input as template code!

        return render_template("result.html", result=result)
    
    return render_template("email_template.html")


@app.route("/ssti_test", methods=["POST"])
def ssti_test():
    user_input = request.form.get("template")  # 🚨 User-controlled input
    template = Template(user_input)  # 🚨 Vulnerability Here
    return template.render()  # 🚨 Bandit should flag this


if __name__ == "__main__":
    # 🚨 Insecure Flask app exposure warning (Bandit should flag this)
    app.run(debug=False, host="0.0.0.0", port=8000)
