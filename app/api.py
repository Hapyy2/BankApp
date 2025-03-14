from flask import Flask, request, jsonify
from app.Accounts_Registry import Accounts_Registry
from app.Konto_osobiste import Konto_osobiste

app = Flask(__name__)

#curl -X POST -H 'Content-Type: application/json' -d '{"imie":"Adam","nazwisko":"Kowalski","pesel":"03409878610"}' localhost:5000/api/accounts

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    if Accounts_Registry.SearchAccount(data["pesel"]) == False:
        if "promo" in data: konto = Konto_osobiste(data["imie"], data["nazwisko"], data["pesel"], data["promo"])
        else: konto = Konto_osobiste(data["imie"], data["nazwisko"], data["pesel"])
        Accounts_Registry.AddAccount(konto)
        return jsonify({"message": "Account created"}), 201
    return jsonify({"message": "Cannot create an account beacuse given pesel is already used"}), 409

#curl -X GET localhost:5000/api/accounts/03409878610
@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    print(f"Search account request: {pesel}")
    person = Accounts_Registry.SearchAccount(pesel)
    if person:
        return jsonify({"imie": person.imie, "nazwisko": person.nazwisko, "pesel": person.pesel, "saldo": person.saldo}), 200
    return jsonify({"message": "Could not find the account"}), 404

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print(f"Accounts count request")
    count = Accounts_Registry.CountAccount()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    print(f"Update account request: {pesel}")
    flag = Accounts_Registry.UpdateAccount(pesel, data)
    if flag:
        return jsonify({"message": "Account updated"}), 200
    return jsonify({"message": "Could not update the account"}), 404

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print(f"Delete account request: {pesel}")
    flag = Accounts_Registry.DeleteAccount(pesel)
    if flag:
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Could not delete the account"}), 404

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transers(pesel):
    data = request.get_json()
    sender = Accounts_Registry.SearchAccount(pesel)
    receiver = Accounts_Registry.SearchAccount(data["receiver"])

    if sender == False: return jsonify({"message": "Sending account does not exist"}), 404
    elif receiver == False: return jsonify({"message": "Receiving account does not exist"}), 404

    print(f'Transfer request from: {pesel} to {data["receiver"]}')
    def return_handle(flag):
        if flag: 
            return jsonify({"message": "Zlecenie przyjeto do realizacji"}), 200
        else: 
            return jsonify({"message": "Nie mozna wykonac przelewu z niedostepnych srodkow"}), 422

    if data["type"] == "normal":
        return return_handle(sender.przelew(receiver, int(data["amount"])))
    elif data["type"] == "express":
        return return_handle(sender.ekspres(receiver, int(data["amount"])))
    return jsonify({"message": "Nieznany typ przelewu"}), 404
