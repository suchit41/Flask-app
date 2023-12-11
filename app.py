import datetime

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# The URL of the database API (note that the endpoint in the example may not work)
DB_API_URL = "https://app.ylytic.com/ylytic/test"


def fetch_comments():
    response = requests.get(DB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def filter_comments(comments, search_params):
    filtered_comments = []

    for comment in comments:
        if (
            "search_author" in search_params
            and search_params["search_author"] not in comment["author"]
        ):
            continue

        comment_date = datetime.datetime.strptime(
            comment["at"], "%a, %d %b %Y %H:%M:%S GMT"
        )
        at_from = (
            datetime.datetime.strptime(search_params["at_from"], "%d-%m-%Y")
            if "at_from" in search_params
            else None
        )
        at_to = (
            datetime.datetime.strptime(search_params["at_to"], "%d-%m-%Y")
            if "at_to" in search_params
            else None
        )

        if at_from and comment_date < at_from:
            continue
        if at_to and comment_date > at_to:
            continue

        like_from = (
            int(search_params["like_from"]) if "like_from" in search_params else None
        )
        like_to = int(search_params["like_to"]) if "like_to" in search_params else None

        if like_from and comment["like"] < like_from:
            continue
        if like_to and comment["like"] > like_to:
            continue

        reply_from = (
            int(search_params["reply_from"]) if "reply_from" in search_params else None
        )
        reply_to = (
            int(search_params["reply_to"]) if "reply_to" in search_params else None
        )

        if reply_from and comment["reply"] < reply_from:
            continue
        if reply_to and comment["reply"] > reply_to:
            continue

        if (
            "seach_text" in search_params
            and search_params["seach_text"].lower() not in comment["text"].lower()
        ):
            continue

        filtered_comments.append(comment)

    return filtered_comments


@app.route("/search", methods=["GET"])
def search_comments():
    search_params = request.args.to_dict()
    comments = fetch_comments()["comments"]
    return jsonify(filter_comments(comments, search_params))


if __name__ == "__main__":
    app.run()









    #http://127.0.0.1:5000/search?search_author=Fredrick&at_from=01-01-2023&at_to=01-02-2023&like_from=0&like_to=5&reply_from=0&reply_to=5&seach_text=economic