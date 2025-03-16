import time
import pytest
from pytest_bdd import given, when, then, scenario
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
    

@scenario('../features/yandex_market.feature', 'Open yandex market site')
def test_open_yandex_market():
    pass

@scenario('../features/yandex_market.feature', 'Moving to "Smartphones"')
def test_moving_to_smartphones():
    pass

@scenario('../features/yandex_market.feature', 'Selecting the required filters')
def test_selecting_filters():
    pass

@scenario('../features/yandex_market.feature', 'Selecting the last required product')
def test_selecting_product():
    pass

#Фикстура для инициализации браузера с игнорированием обишок в консоли
@pytest.fixture(scope="module")
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")  
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--allow-running-insecure-content")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service,options = chrome_options)
    
    yield driver


@pytest.fixture(scope="module")
def action(browser):
    actions = ActionChains(browser)
    return actions
    
@given('I open Chrome browser')
def open_browser(browser):
    browser.maximize_window()
    
@when('I navigate to "https://market.yandex.ru"')
def navigate_to_yandex_market(browser,action):
    browser.get("https://market.yandex.ru")
    # Дополнительный клик для снятия всплывающего окна
    WebDriverWait(browser,10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div._2veCe span.ds-text")))
    action.move_by_offset(10, 100).click().perform()
    
    
@then('I should see the main page')
def go_to_site(browser):
    assert browser.find_element(
        By.CSS_SELECTOR, "a.focus-ring span.ds-visuallyHidden").text == "Яндекс"

@given("I'm on the smarphones page")
def on_smartphones_page(browser):
    pass

@when('I go to "Каталог"')
def go_to_catalog(browser,action):
    catalog = browser.find_element(By.CSS_SELECTOR, "button._30-fz")
    catalog.click()
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.iBSez")))

@when('I go to "Электроника"')
def go_to_electronic(browser,action):
    electronics = browser.find_element(By.CSS_SELECTOR, "li[data-zone-data*='97009095']")
    action.move_to_element(electronics).perform()

@when('I click on "Смартфоны"')
def go_to_smartphones(browser):
    smartphones = browser.find_element(By.XPATH, "//a[text()='Смартфоны']")
    smartphones.click()
    
@then('I should see the title about smarphones')
def info_about_smartphones(browser):
    smartphone_page_info = browser.find_element(By.CSS_SELECTOR, "div._38ab0 h1.ds-text")
    assert smartphone_page_info.text == "Смартфоны в Томске"

@when('I click on "Все фильтры"')
def click_filters(browser):
    all_filters = browser.find_element(By.CSS_SELECTOR, "button._3CCE-._1Mcpo._2jQ3e._3ozc8")
    all_filters.click()

@when('I apply filters with price up to 20000')
def apply_filter_price(browser):
    
    price_filter = browser.find_element(By.CSS_SELECTOR, "input._3hHJe._3DAWe")
    price_filter.send_keys("20000")

@when('I apply filter with size from 3 inches')
def apply_filter_inches(browser):
    screen_size_filter = browser.find_element(
        By.XPATH, "//input[@id='range-filter-field-42223410_25565_max']")
    screen_size_filter.send_keys("3")
    

@when('I select at lease 5 manufacturers')
def select_manufacturers(browser):
    WebDriverWait(browser,10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-filter-id='7893318'] div._2XSa_._3EmWg.cia-vs.cia-cs")))
    brands = browser.find_elements(
        By.CSS_SELECTOR, "[data-filter-id='7893318'] div._2XSa_._3EmWg.cia-vs.cia-cs")
    for element in brands[:5]:
        element.click()
        

@when('I click on "Показать товары"')
def click_show(browser):
    show_button = browser.find_element(By.CSS_SELECTOR, "[aria-label='Показать товары']")
    show_button.click()
    
    
@then('I should see the title "Смартфоны"')
def smarthpoes_title(browser):
    try:
        smart_page = WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((
                By.CSS_SELECTOR, "div._38ab0 h1.ds-text"), "Смартфоны в Томске"))
        assert smart_page, "Страница 'Смартфоны' не была открыта"
    except:
        assert False

@then('I should see 5 selected checkboxes')
def count_smartphones(browser):
    brands = browser.find_elements(
        By.CSS_SELECTOR, "[data-filter-id='7893318'] div._2XSa_._3EmWg.cia-vs.cia-cs")
    checked_elements = 0
    for element in brands:
        checkbox = element.find_element(By.CSS_SELECTOR, "label._3Mi7V")
        if checkbox.get_attribute('aria-checked') == 'true':
            checked_elements += 1
    
    assert checked_elements == 5, "Не совпадает количество необходимых элементов"

@then('I should see filled input field with number 3')
def input_field(browser):
    try:
        input_element = browser.find_element(
            By.CSS_SELECTOR, 'div[data-filter-id="42223410"] div.OutVl div.QOuVk input._3hHJe._3DAWe')
        value = input_element.get_attribute("value")
        assert value == '3', f"Ожидалось значение '3', но получено '{value}'"
    except NoSuchElementException:
        assert False, "Выбраное поле не найдено"    
    except:
        assert False
    
    

@when('I count the number of smartphones on one page')
def smartphone_count(browser):
    smartphones = browser.find_elements(
        By.CSS_SELECTOR, "a.EQlfk span.ds-text.ds-text_lineClamp_2.ds-text_weight_med")
    count = len(smartphones)
    print(f"Количество элементов: {count}")

@when('I remember the last smartphone on the page')
def remember_last_smartphone(browser,request):
    smartphones = browser.find_elements(By.CSS_SELECTOR, 'div._2rw4E div.m4M-1.sYeRG > div > a > span')
    if len(smartphones) > 1:
        last_smartphone = smartphones[-1]
        last_smartphone = last_smartphone.get_attribute("title")
        request.config.cache.set('last_smartphone', last_smartphone)
    elif len == 1:
        request.config.cache.set('last_smartphone', smartphones)
    

@when('I change the sorting to "Высокий рейтинг"')
def change_sorting(browser,action):
    try:
        sorting = browser.find_element(By.CSS_SELECTOR, "button._3ooNj")
        action.move_to_element(sorting).click().perform()
        sorting_high_rating = browser.find_element(By.XPATH, '//span[text()="Высокий рейтинг"]')
        action.move_to_element(sorting_high_rating).click().perform()
    #Если после применения фильтров не был показан ни один смартфон
    except NoSuchElementException:
        pytest.xfail("Кнопка сортировки не найдена на странице")

    
@when('I click to remembered smartphone')
def click_remembered_smartphone(browser,request,action):
    last_smartphone = request.config.cache.get('last_smartphone', None)
    smartphones = browser.find_elements(By.CSS_SELECTOR, 'div._2rw4E div.m4M-1.sYeRG > div > a > span')
    for smartphone in smartphones:
        smartphone_id = smartphone.get_attribute("title")
        if last_smartphone in smartphone_id and smartphone.is_displayed():
            action.move_to_element(smartphone).click().perform()
            break


@then('I should see the page of the selected smartphone')
def page_of_selected_smartphone(browser,request):
    last_smartphone = request.config.cache.get('last_smartphone', None)
    if last_smartphone is None:
        pytest.xfail("Элемент последнего смартфона не был сохранен в кэше")
    try:
        selected_page = browser.find_element(
            By.CSS_SELECTOR, 'div._3f8Sy div[id="/content/page/fancyPage/defaultPage/productTitle"]')
        assert selected_page is not None
    
    except NoSuchElementException:
        pytest.xfail("Запомненный последний смартфон не найден при изменении сортировки")

@then('I should see the rating of the selected smartphone')
def check_rating(browser):
    try:
        rating = browser.find_element(By.CSS_SELECTOR, "span.W1kRr")
        assert rating.text, "Элемент найден, но нету рейтинга"
    except NoSuchElementException:
        pytest.xfail("Запомненный смартфон не найден")    

@then('I close the browser')
def close_browser(browser):
    browser.quit()
    assert not browser.service.is_connectable(), "Браузер не был закрыт"