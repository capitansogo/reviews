from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main.test_gpt import gpt_request


def question_generation(adress, name):
    reviews_global = []

    url = 'https://yandex.ru/maps/16/yaroslavl/'
    org = f'{name}, {adress}'

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)
    sleep(3)

    driver.find_element(By.CLASS_NAME, 'input__control').send_keys(org)
    driver.find_element(By.CLASS_NAME, 'input__control').send_keys(Keys.ENTER)

    driver.implicitly_wait(5)
    sleep(10)
    try:
        driver.find_element(By.CLASS_NAME, 'search-snippet-view').click()
        driver.implicitly_wait(10)
    except:
        print('одно заведение')

    url = driver.current_url
    url = url.split('?')
    url = url[0] + 'reviews/'
    driver.get(url)

    driver.implicitly_wait(5)
    sleep(3)

    reviews_container = driver.find_element(By.CLASS_NAME, 'scroll__container')
    reviews_all = []
    scrolls = 5
    for _ in range(scrolls):
        print("Scrolling...", _)
        ActionChains(driver).move_to_element(reviews_container).send_keys(Keys.PAGE_DOWN).perform()
        reviews = driver.find_elements(By.CLASS_NAME, 'business-review-view__body-text')
        for review in reviews:
            reviews_all.append(review.text)
        sleep(1)

    copy = list(set(reviews_all))
    for i in range(len(copy)):
        reviews_global.append(copy[i])

    text = '\n'.join(copy)

    url = 'https://2gis.ru/yaroslavl'
    org = f'{name}, {adress}'
    input_path = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[2]/form/div/input'

    print("start_0")
    driver.get(url)
    driver.implicitly_wait(5)
    print("start")
    driver.find_element(By.XPATH, input_path).send_keys(org)
    driver.find_element(By.XPATH, input_path).send_keys(Keys.ENTER)
    driver.implicitly_wait(5)
    sleep(5)
    driver.find_element(By.CLASS_NAME, '_zjunba').click()
    driver.implicitly_wait(10)
    sleep(5)

    # поиск ссылки с текстом "Отзывы"
    reviews_links = driver.find_elements(By.XPATH, '//*[contains(text(), "Отзывы")]')
    # переход по ссылке
    for link in reviews_links:
        try:
            link.click()
            break
        except:
            print('не найдено')

    driver.implicitly_wait(5)
    sleep(3)
    print("start scroll")
    reviews_container = driver.find_element(By.CLASS_NAME, '_guxkefv')
    reviews_all = []
    scrolls = 5
    for _ in range(scrolls):
        print("Scrolling...", _)
        ActionChains(driver).move_to_element(reviews_container).send_keys(Keys.PAGE_DOWN).perform()
        reviews = driver.find_elements(By.CLASS_NAME, '_1it5ivp')
        reviews_long = driver.find_elements(By.CLASS_NAME, '_ayej9u3')
        print(len(reviews))
        for review in reviews:
            reviews_all.append(review.text)
        for review in reviews_long:
            reviews_all.append(review.text)

        sleep(1)

    print("end scroll")
    copy = list(set(reviews_all))
    for i in range(len(copy)):
        reviews_global.append(copy[i])

    text.join('\n'.join(copy))
    print(text)
    driver.close()
    if len(text) > 5000:
        text = text[:6000]
    return gpt_request(text), reviews_global


