from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def index():
    not_following_back = []

    if request.method == "POST":
        followers_file = request.files.get("followers")
        following_file = request.files.get("following")

        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        followers = set(entry["string_list_data"][0]["value"] for entry in followers_data)
        following = set(entry["title"] for entry in following_data["relationships_following"])

        not_following_back = sorted(following - followers)

    return render_template("index.html", not_following_back=not_following_back)


def handler(event, context):
    return app(event, context)
