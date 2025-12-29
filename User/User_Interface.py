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
                            "content": """你是一個占卜助手。你的目標是取得使用者的出生年、月、日、名字、姓氏。
                                1. 每次對話都要檢查是否已獲得這五個資訊。
                                2. 如果缺少任何一項，請在對話中溫柔的引導使用者提供。
                                3. **重要格式**：請在回覆的最末端，固定加上這行 JSON 標記：
                                DATA:{"Birth_year": 年, "Birth_month": 月, "Birth_day": 日, "First_name": 名字, "Last_name": 姓氏} 
                                (若無則填null)
                                4.若使用者最後的回覆表明任意資訊有誤, 當即將「3.」的標示修改為null
                                5.絕對不要進行占卜, 你只需要取得使用者的出生年、月、日、名字、姓氏
                                6.檢查出生日期的合理性, 1, 3, 5, 7, 8, 10, 12月有31天; 4, 6, 9, 11月有30天; 2月通常為28天, 但若年份為閏年則有29天, 若使用者的輸入不合理, 請提醒他"""
                        }]

    def get_info(self):
        ask_again = True

        while ask_again:
            user_input = input("你: ")

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

                    print("AI 回覆：", result['message']['content'].split('DATA:')[0].strip())
                    print(f"姓名：{self.user_info['Last_name']}{self.user_info['First_name']}")
                    print(f"生日：{self.user_info['Birth_year']}/{self.user_info['Birth_month']}/{self.user_info['Birth_day']}")

                    incomplete = (None in self.user_info.values()) or ("null" in self.user_info.values())
                    if incomplete:
                        ask_again = True
                    else:
                        ask_again = False

                else:
                    return f"error: {response.status_code}, {response.text}"

            except Exception as e:
                return f"Exception: {str(e)}"

        return self.user_info

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
                        self.user_info["Birth_year"] = int(year)
                except(ValueError, TypeError):
                    pass

                month = data.get("Birth_month")
                try:
                    if int(month) > 0 and int(month) <= 12:
                        self.user_info["Birth_month"] = int(month)
                except(ValueError, TypeError):
                    pass

                day = data.get("Birth_day")
                try:
                    if int(day) > 0:
                        #The day's validtaion has not done yet
                        self.user_info["Birth_day"] = int(day)
                except(ValueError, TypeError):
                    pass

            except json.JSONDecodeError:
                pass