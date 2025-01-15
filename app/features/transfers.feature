Feature: Bank transfers between accounts

  Background:
    # Clean up any existing accounts from previous tests
    When I delete account with pesel: "12345678901"
    And I delete account with pesel: "98765432109"
    And I delete account with pesel: "89092909876"
    And I delete account with pesel: "77010112345"
    Given Number of accounts in registry equals: "0"
    # Create test accounts
    When I create an account using imie: "John", nazwisko: "Doe", pesel: "12345678901"
    And I create an account using imie: "Jane", nazwisko: "Smith", pesel: "98765432109"
    Then Account with pesel "12345678901" exists in registry
    And Account with pesel "98765432109" exists in registry

  Scenario: Successful normal transfer between accounts
    Given I set initial balance "50" for account with pesel "12345678901"
    When I transfer "20" from account "12345678901" to "98765432109" using "normal" type
    Then The transfer should be successful
    And Account with pesel "12345678901" should have balance "30"
    And Account with pesel "98765432109" should have balance "20"

  Scenario: Failed normal transfer due to insufficient funds
    Given I set initial balance "50" for account with pesel "12345678901"
    When I transfer "1000000" from account "12345678901" to "98765432109" using "normal" type
    Then The transfer should fail with message "Nie mozna wykonac przelewu z niedostepnych srodkow"
    And Account with pesel "12345678901" should have balance "50"
    And Account with pesel "98765432109" should have balance "0"

  Scenario: Successful express transfer between accounts
    Given I set initial balance "50" for account with pesel "12345678901"
    When I transfer "20" from account "12345678901" to "98765432109" using "express" type
    Then The transfer should be successful
    And Account with pesel "12345678901" should have balance "29"
    And Account with pesel "98765432109" should have balance "20"

  Scenario: Failed transfer due to non-existent sender
    When I transfer "100" from account "99999999999" to "98765432109" using "normal" type
    Then The transfer should fail with message "Sending account does not exist"

  Scenario: Failed transfer due to non-existent receiver
    Given I set initial balance "50" for account with pesel "12345678901"
    When I transfer "20" from account "12345678901" to "99999999999" using "normal" type
    Then The transfer should fail with message "Receiving account does not exist"

  Scenario: Failed transfer due to invalid transfer type
    Given I set initial balance "50" for account with pesel "12345678901"
    When I transfer "20" from account "12345678901" to "98765432109" using "invalid" type
    Then The transfer should fail with message "Nieznany typ przelewu"