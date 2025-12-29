import sys
import warnings
# 隱藏 SSL 警告，讓畫面乾淨
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

from User.User_Interface import User
from crawler.dispatcher import selectWeb

def main():
    print("🚀 啟動測試流程...")
    u = User()

    # 1. 測試 AI 資料解析
    print("📍 步驟 1: 測試 AI 回覆與解析")
    reply = u.get_info("我叫詹伯雄，生日是1984/5/13.")
    print(f"   - AI 回應: {reply}")
    
    # 手動補齊剩餘資料 (確保字典裡有資料)
    u.user_info["Birth_year"] = "1984"
    u.user_info["Birth_month"] = "5"
    u.user_info["Birth_day"] = "13"
    u.user_info["Last_name"] = "詹"
    u.user_info["First_name"] = "伯雄"
    print(f"   - 目前存下的個資: {u.user_info}")

    # 2. 測試星座爬蟲
    print("\n📍 步驟 2: 執行星座爬蟲 (這會花一點時間)...")
    result1 = selectWeb("constellation", [u.user_info["Birth_year"], u.user_info["Birth_month"], u.user_info["Birth_day"]])
    
    if result1:
        print("   ✅ 星座結果抓取成功！")
        # 這裡一定要 print，否則你什麼都看不到
        for line in result1[:3]: # 先印前三行看看
            print(f"      > {line}")
    else:
        print("   ❌ 星座結果為空！請檢查爬蟲 selector。")

    # 3. 測試姓名爬蟲
    print("\n📍 步驟 3: 執行姓名爬蟲...")
    result2 = selectWeb("name", [u.user_info["Last_name"], u.user_info["First_name"]])
    
    if result2:
        print("   ✅ 姓名結果抓取成功！")
        print(f"      > {result2[0] if isinstance(result2, list) else result2}")
    else:
        print("   ❌ 姓名結果為空！")

    print("\n--- 測試結束 ---")

if __name__ == "__main__":
    main()