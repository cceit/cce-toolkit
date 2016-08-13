Feature: Board Testing

  Scenario: Add Board
    Given I am logged in as mwilcoxen
    When I visit add_board
    And I submit valid board information
    Then I should see the new board

  Scenario: Edit Board
    Given I am logged in as mwilcoxen
    And I have a board
    When I visit browse_boards
    And I click the edit board button
    And I submit updated board information
    Then I should see the updated board

  Scenario: Delete Board
    Given I am logged in as mwilcoxen
    And I have a board
    When I visit browse_boards
    And I click the delete board button
    And I delete the board
    Then I shouldnt see the board

  Scenario:  Use Board Advanced Search
    Given I am logged in as mwilcoxen
    And I have a board
    When I visit browse_boards
    And I use the board advanced search
    Then I should see the board