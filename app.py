from flask import Flask, request, jsonify
from flask_cors import CORS   # 🔥 確保你有 import 這個

from crawler.dispatcher import selectWeb, fortune_cookie
app = Flask(__name__)

# 🔥 允許所有來源（最簡單、最不會出錯）
CORS(app, resources={r"/*": {"origins": "*"}})



@app.post("/api/run")
def run_crawler():
    data = request.json
    user_text = data.get("text")
    print("收到前端文字:", user_text)

    # 🔥 幸運餅乾邏輯
    if user_text == "給我一個幸運餅乾":
        return jsonify({"result": fortune_cookie()})

    # 🔥 原本邏輯
    result = selectWeb("name", ["王", "小民"])
    return jsonify({"result": result})

if __name__ == "__main__":
    print("=== Flask 啟動 ===")
    app.run(debug=True)