from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    not_following_back = []
    if request.method == "POST":
        followers_file = request.files.get("followers")
        following_file = request.files.get("following")
        
        if not followers_file or not following_file:
            return "Harap unggah kedua file JSON!", 400

        try:
            followers_data = json.load(followers_file)
            followers = set(
                user["value"]
                for entry in followers_data
                for user in entry["string_list_data"]
            )
            following_data = json.load(following_file)
            following = set(
                user["value"]
                for entry in following_data["relationships_following"]
                for user in entry["string_list_data"]
            )
            not_following_back = sorted(following - followers)

        except json.JSONDecodeError:
            return "File JSON SALAHHH!!!.", 400

    return render_template("index.html", not_following_back=not_following_back)


if __name__ == "__main__":
    app.run(debug=True)
