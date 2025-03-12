from flask import Flask, render_template, request
from jinja2 import Template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def function_route():
    if request.method == "POST":
        emailpre = request.form.get("emailpre", "")
        template = Template(emailpre)
        result = template.render()
        return render_template("result.html", result=result)
    return render_template("email_template.html")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
