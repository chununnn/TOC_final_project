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
    last_name = parameters[0]
    first_name = parameters[1]
    

    driver = get_driver()
    
    try:
        driver.get(f"https://www.sheup.org/xingming.php")

        driver.find_element(By.NAME, "xingx").send_keys(last_name)

        # 輸入名
        driver.find_element(By.NAME, "mingx").send_keys(first_name)

        # 點擊送出按鈕
        driver.find_element(By.NAME, "cemingzi").click()
        
        
        # 等待新的 c_1 區塊出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c_1"))
        )

        # 重新抓所有 c_1，取最後一個
        blocks = driver.find_elements(By.CLASS_NAME, "c_1")
        second_block = blocks[1]

        
        children = second_block.find_elements(By.XPATH, "./div")

        result = []

        for child in children:
            cls = child.get_attribute("class")
            if cls in ["c1_text", "c1_title"]:
                result.append(child.text)


  
        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()




    

    

