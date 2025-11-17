from flask import Flask, render_template, request
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
            # Parsing followers
            followers_data = json.load(followers_file)
            followers = set()

            for entry in followers_data:
                try:
                    username = entry["string_list_data"][0]["value"]
                    followers.add(username)
                except:
                    pass

            # Parsing following
            following_data = json.load(following_file)
            following = set()

            for entry in following_data["relationships_following"]:
                try:
                    username = entry["title"]
                    following.add(username)
                except:
                    pass

            # Hitung yang tidak follow balik
            not_following_back = sorted(following - followers)

        except Exception as e:
            return f"JSON ERROR: {str(e)}", 400

    return render_template("index.html", not_following_back=not_following_back)


if __name__ == "__main__":
    app.run(debug=True)
