import locale
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main.test_gpt import gpt_request
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def question_generation(adress, name):
    url = 'https://2gis.ru/yaroslavl'
    text = f'{name}, {adress}'
    input_path = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[2]/form/div/input'
    reviews_path = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div/a'
    reviews_path_class = '_2lcm958'

    # Specify the URL of your remote WebDriver
    # remote_url = 'http://localhost:4444/wd/hub'

    print("start_0")
    # Create a WebDriver with the specified options
    options = Options()
    # options.add_argument('--headless')


    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    print("start")
    driver.find_element(By.XPATH, input_path).send_keys(text)
    driver.find_element(By.XPATH, input_path).send_keys(Keys.ENTER)
    driver.implicitly_wait(5)
    sleep(3)
    print("start_2")
    # driver.find_element(By.XPATH, reviews_path).click()

    # получение адреса страницы
    url = driver.current_url
    url = url.split('?m=')
    print(url[0])
    print(url[1])
    url = url[0] + '/tab/reviews/' + url[1]

    driver.get(url)
    sleep(5)

    print(driver.current_url)

    # # поиск всех reviews_path_class и клик по второму
    # reviews_path_class = driver.find_elements(By.CLASS_NAME, reviews_path_class)
    # reviews_path_class[1].click()
    # driver.implicitly_wait(5)
    # sleep(3)

    print("start scroll")
    reviews_all = []
    reviews_container = driver.find_element(By.CLASS_NAME, '_guxkefv')

    # получение кода страницы и сохранение в файл
    print(driver.page_source)

    scrolls = 20
    for _ in range(scrolls):
        print("Scrolling...", _)
        ActionChains(driver).move_to_element(reviews_container).send_keys(Keys.PAGE_DOWN).perform()
        reviews = driver.find_elements(By.CLASS_NAME, '_1it5ivp')
        print(len(reviews))
        for review in reviews:
            reviews_all.append(review.text)
            print(review.text)

        sleep(1)

    print(reviews_all)
    print("end scroll")
    reviews = list(set(reviews_all))

    text = '\n'.join(reviews).encode('windows-1251', errors='ignore').decode('windows-1251')
    print(text)
    driver.close()
    return gpt_request(text), reviews


# question_generation('Свободы 55', 'True Gamers')