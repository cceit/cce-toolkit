Feature: Board Testing

  Scenario: Register
    When I visit registration
    And I submit valid registration information
    Then I should be registered

  Scenario: Add Board
    Given I am logged in as mwilcoxen
    When I visit add_board
    And I submit valid board information
    Then I should see the board