from flask import Flask, request, jsonify
from flask_cors import CORS
from crawler.dispatcher import selectWeb

app = Flask(__name__)
CORS(app)  # 🔥 這行一定要有，且要放在 app = Flask() 後面

@app.post("/api/run")

def run_crawler():
    data = request.json
    user_text = data.get("text")
    #user_text 是 input 欄位的內容
    print("收到前端文字:", user_text)

    # 現在先寫死
    result = selectWeb("name", ["王", "小民"])
    #要output的結果放在result

    return jsonify({"result": result})


if __name__ == "__main__":
    print("=== Flask 啟動 ===")
    app.run(debug=True)