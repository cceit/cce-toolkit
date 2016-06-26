Feature: Base Applications App

  Scenario: Activity Log Hook
    When I create a log item
    Then that log item should exist