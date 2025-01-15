Feature: Account registry

  Background:
    When I delete account with pesel: "12345678901"
    And I delete account with pesel: "98765432109"
    And I delete account with pesel: "89092909876"
    And I delete account with pesel: "77010112345"
    Given Number of accounts in registry equals: "0"

  Scenario: User is able to create a new account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "kurt", nazwisko: "cobain", pesel: "89092909876"
    Then Number of accounts in registry equals: "1"
    And Account with pesel "89092909876" exists in registry

  Scenario: User is able to create a second account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "dave", nazwisko: "grohl", pesel: "77010112345"
    Then Number of accounts in registry equals: "1"
    And Account with pesel "77010112345" exists in registry

  Scenario: User is able to update imie of already created account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "kurt", nazwisko: "cobain", pesel: "89092909876"
    Given Account with pesel "89092909876" exists in registry
    When I update "imie" of account with pesel: "89092909876" to "russell"
    Then Account with pesel "89092909876" has "imie" equal to "russell"

  Scenario: User is able to update nazwisko of already created account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "kurt", nazwisko: "cobain", pesel: "89092909876"
    Given Account with pesel "89092909876" exists in registry
    When I update "nazwisko" of account with pesel: "89092909876" to "reed"
    Then Account with pesel "89092909876" has "nazwisko" equal to "reed"

  Scenario: User is able to delete already created account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "kurt", nazwisko: "cobain", pesel: "89092909876"
    Given Account with pesel "89092909876" exists in registry
    When I delete account with pesel: "89092909876"
    Then Account with pesel "89092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: User is able to delete last account
    Given Number of accounts in registry equals: "0"
    When I create an account using imie: "dave", nazwisko: "grohl", pesel: "77010112345"
    Given Account with pesel "77010112345" exists in registry
    When I delete account with pesel: "77010112345"
    Then Account with pesel "77010112345" does not exist in registry
    And Number of accounts in registry equals: "0"