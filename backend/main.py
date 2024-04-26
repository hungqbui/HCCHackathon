from flask import Flask, request, jsonify
from flask_cors import CORS
from googlesearch import search
import json
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

import model

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    print(data)

    if (not data["url"].startswith("http")):
        return jsonify({
            "ok": False,
            "error": "Invalid URL"
        })
    caption = model.get_image_caption(data['url'])
    description = model.describe_image(caption)
    more_info = json.loads(model.generate_query(description))

    print(more_info)
    search_res = [i for i in search(more_info["query"][0], num=5, stop=5, pause=2)]

    return jsonify({
        "ok": True,
        "image": data['url'],
        "caption": caption,
        "description": description,
        "search_res": search_res,
        "query": more_info
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")