from flask import Flask, request, jsonify
from flask_cors import CORS

from crawler.dispatcher import selectWeb, fortune_cookie
from User.User_Interface import User

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

u = User()

@app.route('/api/run', methods = ['POST'])
def chat():
    try:
        data = request.json
        input = data.get("text", "").strip()

        if input == "給我一個幸運餅乾":
            cookie = fortune_cookie()
            return jsonify({"result": [cookie]})
        
        reply = u.get_info(input)
        info = u.user_info

        fields = ["Birth_year", "Birth_month", "Birth_day", "First_name", "Last_name"]
        is_ready = all(info.get(k) is not None and str(info.get(k)).lower() != "null" for k in fields)

        if is_ready:
            result1 = selectWeb("constellation", [str(info["Birth_year"]), str(info["Birth_month"]), str(info["Birth_day"])])
            result2 = selectWeb("name", [str(info["Last_name"]), str(info["First_name"])])

            summary = u.summarize_fortune(" ".join(result1), " ".join(result2))
            final_output = [
                f"{reply}",
                "--------------------------------",
                "🔮 【大師開示與總結】 🔮\n",
                "",
                f"{summary}", 
                "",
                "--------------------------------",
                "🕯️ 占卜結束，天機已定。\n",
                "👋 「下一位緣主請進！」\n",
                "💡 (現在您可以直接輸入新的名字與生日，為下一位進行占卜)"
            ]
            
            u.reset_info()

            return jsonify({"result": [final_output]})
        
        else:
            return jsonify({"result": [reply]})
        
    except Exception as e:
        return jsonify({"result": [f"Error: {str(e)}"]})
    
if __name__ == "__main__":
    print("=" * 30)
    print("🔮 算命機器人後端伺服器已啟動")
    print("🔗 API 位址: http://127.0.0.1:5000/api/run")
    print("=" * 30)
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)