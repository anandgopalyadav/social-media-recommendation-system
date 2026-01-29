from flask import Flask, render_template, request
from recommendation_logic import (
    load_data,
    data_clean,
    friend_suggestions_with_names,
    page_suggestions_with_names
) 

app = Flask(__name__)

# Load & clean data ONCE
data = load_data()
data = data_clean(data)

@app.route("/", methods=["GET", "POST"])
def index():
    friends = []
    pages = []
    user_id = None

    if request.method == "POST":
        user_id = request.form.get("user_id")

        if user_id and user_id.isdigit():
            user_id = int(user_id)
            friends = friend_suggestions_with_names(user_id, data)
            pages = page_suggestions_with_names(user_id, data)

    return render_template(
        "index.html",
        friends=friends,
        pages=pages,
        user_id=user_id
    )

if __name__ == "__main__":
    app.run(debug=True)
