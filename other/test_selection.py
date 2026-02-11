from flask import Flask, render_template, request

app = Flask(__name__)

# Sample data for the dropdown
options = ["Apple", "Banana", "Cherry", "Date"]

@app.route("/", methods=["GET", "POST"])
def selection():
    selected_option = None
    if request.method == "POST":
        selected_option = request.form.get("fruit")
    return render_template("selection.html", options=options, selected_option=selected_option)

if __name__ == "__main__":
    app.run(debug=True)
