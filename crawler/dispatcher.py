from .constellation import run as constellation_run
from .name import run as name_run
import os
import random
def selectWeb(site, params):
    if site == "constellation":
        return constellation_run(params)
    elif site == "name":
        return name_run(params)
    return {"error": "unknown site"}

# constellation parameters: [year, month, date]
# example: ["2023", "03", "15"]

def fortune_cookie():
    # 取得 dispatcher.py 所在的資料夾路徑
    base_dir = os.path.dirname(__file__)
    cookie_path = os.path.join(base_dir, "cookie.txt")

    with open(cookie_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 避免空行
    lines = [line.strip() for line in lines if line.strip()]

    # 隨機選一句
    return [random.choice(lines)]
