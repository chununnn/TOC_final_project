from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from time import sleep


def get_driver():
    """初始化 ChromeDriver，適用本機與 Docker"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Docker 環境請取消註解以下三行
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver
    

def run(parameters : list):
    year = parameters[0]
    month = parameters[1]
    date = parameters[2]

    driver = get_driver()
    
    try:
        driver.get(f"https://sheup.org/constellation.php")

        year_select = Select(driver.find_element(By.NAME, "nian"))
        year_select.select_by_visible_text(year)

        # 選擇月份
        month_select = Select(driver.find_element(By.NAME, "yue"))
        month_select.select_by_visible_text(month)

        # 選擇日期
        day_select = Select(driver.find_element(By.NAME, "ri"))
        day_select.select_by_visible_text(date)

        #click submit
        driver.find_element(By.NAME, "xingzuo").click()

        container = driver.find_element(By.CLASS_NAME, "subs_main")

        # 找到所有 <p>
        paragraphs = container.find_elements(By.TAG_NAME, "p")

        # 只回傳文字
        texts = [p.text.strip() for p in paragraphs if p.text.strip()]

        return texts

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()




    

    

