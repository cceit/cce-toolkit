Feature: Tasks

  Scenario: Add Task
    Given I am logged in as mwilcoxen
    And I have a board
    When I visit add_task
    And I submit valid task information
    Then I should see the new task

  Scenario: Edit Task
    Given I am logged in as mwilcoxen
    And I have a board
    And I have a task
    When I visit browse_tasks
    And I click the edit task button
    And I submit updated task information
    Then I should see the updated task

  Scenario: Delete Task
    Given I am logged in as mwilcoxen
    And I have a board
    And I have a task
    When I visit browse_tasks
    And I click the delete task button
    And I delete the task
    Then I shouldnt see the task

  Scenario: Use Task Advanced Search
    Given I am logged in as mwilcoxen
    And I have a board
    And I have a task
    When I visit browse_tasks
    And I use the task advanced search
    Then I should see the task

  Scenario: Update Status (Started)
    Given I am logged in as mwilcoxen
    And I have a board
    And I have a task
    When I visit browse_tasks
    And I click the view task button
    And I click the update status button
    And I update the status to started
    Then The task status should be started

  Scenario: Update Status (Completed)
    Given I am logged in as mwilcoxen
    And I have a board
    And I have a task
    When I visit browse_tasks
    And I click the view task button
    And I click the update status button
    And I update the status to complete
    Then The task status should be complete