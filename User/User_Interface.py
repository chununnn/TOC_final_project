import requests
import json
import re

class User:
    def __init__(self):
        self.URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/chat"
        self.KEY = "2c934b2f39d3003832fa6972cc95c2455c186b58812a1c0157b266a358dce7f0"
        self.user_info = {"Birth_year": None, "Birth_month": None, "Birth_day": None, "First_name": None, "Last_name": None}
        self.history = [{
                            "role": "system", 
                            "content": """你是一個占卜助手。目標是獲取使用者的：姓名（拆分為姓氏與名字）、出生年、月、日。

                            運作邏輯：
                            1. 請溫柔引導使用者提供資訊，不要一次問太多問題。
                            2. **姓名處理規則**：
                            - 當使用者提供中文全名（如「詹伯雄」）時：
                                - 姓氏 (Last_name) 為第一個字（如「詹」）。
                                - 名字 (First_name) 為後面的字（如「伯雄」）。
                            - 請務必區分清楚，不可顛倒。
                            3. **格式規範**：請在回覆最末端固定加上 JSON：
                            DATA:{"Birth_year": 年, "Birth_month": 月, "Birth_day": 日, "First_name": "名", "Last_name": "姓"}
                            (若資訊未知則填 null，不加引號)
                            4. 一但獲得相關資訊，請立即更新 JSON 內容。
                            5. 若使用者糾正資訊，請立即更新 JSON 內容。
                            6. 禁止占卜，你只負責收集這五項資料。
                            7. 非常重要！！！若已獲得全部資料，無需確認，只需要感謝使用者提供資訊。"""
                        }]

    def get_info(self, user_input):
        self.history.append({
            "role": "user", 
            "content": user_input
        })

        payload = {
            "model": "gemma3:4b",
            "messages": self.history, 
            "stream": False
        }

        headers = {"Authorization": f"Bearer {self.KEY}"}

        try:
            response = requests.post(self.URL, json = payload, headers = headers)

            if response.status_code == 200:
                result = response.json()

                self.history.append({
                    "role": "assistant", 
                    "content": result['message']['content']
                })
                
                self.update_info(result['message']['content'])

            else:
                return f"error: {response.status_code}, {response.text}"

        except Exception as e:
            return f"Exception: {str(e)}"

        return result['message']['content'].split('DATA:')[0].strip()

    def update_info(self, str):
        match = re.search(r'DATA:(\{.*\})', str)
        if match:
            try:
                data = json.loads(match.group(1))

                First_name = data.get("First_name")
                self.user_info["First_name"] = First_name

                Last_name = data.get("Last_name")
                self.user_info["Last_name"] = Last_name

                year = data.get("Birth_year")
                try:
                    if int(year) > 1800:
                        self.user_info["Birth_year"] = year
                except(ValueError, TypeError):
                    pass

                month = data.get("Birth_month")
                try:
                    if int(month) > 0 and int(month) <= 12:
                        self.user_info["Birth_month"] = month
                except(ValueError, TypeError):
                    pass

                day = data.get("Birth_day")
                try:
                    if int(day) > 0:
                        #The day's validtaion has not done yet
                        self.user_info["Birth_day"] = day
                except(ValueError, TypeError):
                    pass

            except json.JSONDecodeError:
                pass

    def reset_info(self):
        self.user_info = {
            "Birth_year": None, "Birth_month": None, "Birth_day": None, 
            "First_name": None, "Last_name": None
        }
        self.history = [self.history[0]]

    def summarize_fortune(self, constellation_data, name_data):
        summary_prompt = f"""
        使用者資料如下：
        姓名：{self.user_info['Last_name']}{self.user_info['First_name']}
        生日：{self.user_info['Birth_year']}/{self.user_info['Birth_month']}/{self.user_info['Birth_day']}

        我們從網路上抓取到了以下占卜資訊：
        1. 星座運勢內容：{constellation_data}
        2. 姓名命理分析：{name_data}

        請你扮演一位資深的命理大師，根據以上這兩份資訊進行總結。
        要求：
        - 語氣溫柔且專業。
        - 結合星座與姓名的特點，給使用者一段鼓勵的話。
        - 不要直接條列原文，請用你自己的話重新統整。
        - 說話要有禪意。
        """

        payload = {
            "model": "gemma3:4b",
            "messages": [{"role": "user", "content": summary_prompt}],
            "stream": False,
            "options": {
            "temperature": 0.8,
            "top_p": 0.9
            }
        }
        headers = {"Authorization": f"Bearer {self.KEY}"}
        
        try:
            response = requests.post(self.URL, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            return "大師目前累了，請直接參考原文。"
        except:
            return "統整失敗，請參考原文。"