from behave import given, when, then
import requests
import unittest
import time

URL = "http://localhost:5000"

@given('I set initial balance "{amount}" for account with pesel "{pesel}"')
def set_initial_balance(context, amount, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 200, f"Account {pesel} does not exist")
    account_data = response.json()
    expected_balance = 50 if pesel == context.sender_pesel else 0
    unittest.TestCase().assertEqual(account_data["saldo"], expected_balance, f"Account should have balance of {expected_balance}")

@when('I transfer "{amount}" from account "{sender}" to "{receiver}" using "{transfer_type}" type')
def transfer_money(context, amount, sender, receiver, transfer_type):
    json_body = {
        "receiver": receiver,
        "amount": int(amount),
        "type": transfer_type
    }
    response = requests.post(URL + f"/api/accounts/{sender}/transfer", json=json_body)
    context.response = response

@then('The transfer should be successful')
def check_transfer_success(context):
    if context.response.status_code != 200:
        error_data = context.response.json()
        print(f"Transfer failed with status {context.response.status_code} and message: {error_data.get('message', 'No message')}")
    unittest.TestCase().assertEqual(context.response.status_code, 200)
    response_data = context.response.json()
    unittest.TestCase().assertEqual(response_data["message"], "Zlecenie przyjeto do realizacji")

@then('The transfer should fail with message "{message}"')
def check_transfer_failure(context, message):
    expected_code = 404 if message in [
        "Sending account does not exist", 
        "Receiving account does not exist",
        "Nieznany typ przelewu"
    ] else 422
    
    actual_code = context.response.status_code
    if actual_code != expected_code:
        error_data = context.response.json()
        print(f"Expected code {expected_code} but got {actual_code}. Message: {error_data.get('message', 'No message')}")
    
    unittest.TestCase().assertEqual(actual_code, expected_code, f"Expected status code {expected_code}, got {actual_code}")
    response_data = context.response.json()
    unittest.TestCase().assertEqual(response_data["message"], message, f"Expected message '{message}', got '{response_data['message']}'")

@then('Account with pesel "{pesel}" should have balance "{amount}"')
def check_account_balance(context, pesel, amount):
    time.sleep(0.1)
    
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 200)
    account_data = response.json()
    expected_balance = int(amount)
    actual_balance = account_data["saldo"]
    unittest.TestCase().assertEqual(actual_balance, expected_balance, f"Expected balance {expected_balance}, got {actual_balance}")