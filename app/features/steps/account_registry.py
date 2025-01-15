import requests
from behave import given, when, then
import unittest

URL = "http://localhost:5000"

@given('Number of accounts in registry equals: "{expected_count}"')
@then('Number of accounts in registry equals: "{expected_count}"')
def account_count(context, expected_count):
    response = requests.get(URL + "/api/accounts/count")
    unittest.TestCase().assertEqual(response.status_code, 200)
    actual_count = response.json()["count"]
    unittest.TestCase().assertEqual(actual_count, int(expected_count))

@when('I create an account using imie: "{imie}", nazwisko: "{nazwisko}", pesel: "{pesel}"')
def create_account(context, imie, nazwisko, pesel):
    if not hasattr(context, 'sender_pesel'):
        context.sender_pesel = pesel
        json_body = {
            "imie": imie,
            "nazwisko": nazwisko,
            "pesel": pesel,
            "promo": "PROM_123"
        }
    else:
        json_body = {
            "imie": imie,
            "nazwisko": nazwisko,
            "pesel": pesel
        }
    
    response = requests.post(URL + "/api/accounts", json=json_body)
    unittest.TestCase().assertEqual(response.status_code, 201)
    
    verify_response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(verify_response.status_code, 200)
    account_data = verify_response.json()
    unittest.TestCase().assertEqual(account_data["pesel"], pesel)

@then('Account with pesel "{pesel}" exists in registry')
def account_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 200)
    account_data = response.json()
    unittest.TestCase().assertEqual(account_data["pesel"], pesel)

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertIn(response.status_code, [200, 404])

@then('Account with pesel "{pesel}" does not exist in registry')
def account_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 404)

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["imie", "nazwisko"]:
        raise ValueError(f"Invalid field: {field}. Must be 'imie' or 'nazwisko'")
    
    json_body = {field: value}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    unittest.TestCase().assertEqual(response.status_code, 200)
    
    verify_response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(verify_response.status_code, 200)
    account_data = verify_response.json()
    unittest.TestCase().assertEqual(account_data[field], value)

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def account_field_equals(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 200)
    account_data = response.json()
    unittest.TestCase().assertEqual(account_data[field], value)

@given('Account with pesel "{pesel}" exists in registry')
def step_impl(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    unittest.TestCase().assertEqual(response.status_code, 200)
    account_data = response.json()
    unittest.TestCase().assertEqual(account_data["pesel"], pesel)