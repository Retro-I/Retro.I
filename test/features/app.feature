Feature: Counter
  Scenario: Increment the counter
    Given the app is running
    When I click the "Increment" button
    Then I should see the counter increase to "1"