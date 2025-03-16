Feature: Yandex Market Smartphones Search
  
  Scenario: Open yandex market site
    Given I open Chrome browser
    When I navigate to "https://market.yandex.ru"
    Then I should see the main page

  Scenario: Moving to "Smartphones"
    Given I'm on the smarphones page
    When I go to "Каталог"
    And I go to "Электроника"
    And  I click on "Смартфоны"
    Then I should see the title about smarphones

  Scenario: Selecting the required filters
    When I click on "Все фильтры"
    And I apply filters with price up to 20000
    And I apply filter with size from 3 inches
    And I select at lease 5 manufacturers
    And I click on "Показать товары"
    Then I should see the title "Смартфоны"
    And I should see 5 selected checkboxes
    And I should see filled input field with number 3

  Scenario: Selecting the last required product
    When I count the number of smartphones on one page
    And I remember the last smartphone on the page
    And I change the sorting to "Высокий рейтинг"
    And I click to remembered smartphone
    Then I should see the page of the selected smartphone
    And I should see the rating of the selected smartphone
    And I close the browser