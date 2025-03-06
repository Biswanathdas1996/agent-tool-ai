from flask import Flask, request, jsonify
from faker import Faker
from datetime import datetime, timedelta
from joblib import Parallel, delayed
import random
import json
from DataGenerator.helper import  get_random_bank, get_currency_code, generate_transaction_reference, generate_address, generate_name

app = Flask(__name__)

def load_banks_data():
    try:
        with open('DataGenerator/banks.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

banks_data = load_banks_data()

def generate_base_data(source_country, destination_country):
    transaction_reference_number = generate_transaction_reference()
    value_date = (datetime.now() - timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
    currency = get_currency_code(destination_country)
    currency_pair = f"{get_currency_code(destination_country)}/{get_currency_code(source_country)}"
    amount = round(random.uniform(1000, 100000), 2)
    sender_bank = get_random_bank(source_country)
    sender_bank_code = Faker().bothify(text='??????##XXX').upper()
    receiver_bank = get_random_bank(destination_country)
    receiver_bank_code = Faker().bothify(text='??????##XXX').upper()
    sender = {
        "name": generate_name(source_country),
        "address": generate_address(source_country)
    }
    receiver = {
        "name": generate_name(destination_country),
        "address": generate_address(destination_country)
    }
    return {
        "transaction_reference_number": transaction_reference_number,
        "value_date": value_date,
        "currency": currency,
        "currency_pair": currency_pair,
        "amount": amount,
        "sender_bank": sender_bank,
        "receiver_bank": receiver_bank,
        "sender": sender,
        "receiver": receiver,
        "sender_bank_code": sender_bank_code,
        "receiver_bank_code": receiver_bank_code
    }

def create_swift_message(message_type, base_data, additional_fields):
    swift_message = {
        "swift": {
            "messageType": message_type,
            "sender": base_data["sender_bank_code"],
            "receiver": base_data["receiver_bank_code"],
            "transactionReferenceNumber": base_data["transaction_reference_number"],
            "valueDate": base_data["value_date"],
            "currency": base_data["currency"],
            "amount": base_data["amount"],
            "orderingInstitution": {
                "name": base_data["sender_bank"],
                "bic": base_data["sender_bank_code"]
            },
            "beneficiaryInstitution": {
                "name": base_data["receiver_bank"],
                "bic": base_data["receiver_bank_code"]
            }
        }
    }
    swift_message["swift"].update(additional_fields)
    return swift_message

def MT103(source_country, destination_country):
    base_data = generate_base_data(source_country, destination_country)
    additional_fields = {
        "category": "Customer Payments and Cheques",
        "orderingCustomer": {
            "name": base_data["sender"],
            "accountNumber": base_data["sender_bank_code"]
        },
        "beneficiaryCustomer": {
            "name": base_data["receiver"],
            "accountNumber": base_data["receiver_bank_code"]
        },
        "detailsOfCharges": "SHA"
    }
    return create_swift_message("MT103", base_data, additional_fields)

def MT202(source_country, destination_country):
    base_data = generate_base_data(source_country, destination_country)
    additional_fields = {
        "category": "Financial Institution Transfers",
        "detailsOfCharges": "OUR"
    }
    return create_swift_message("MT202", base_data, additional_fields)

def MT300(source_country, destination_country):
    base_data = generate_base_data(source_country, destination_country)
    additional_fields = {
        "category": "Foreign Exchange and Money Market",
        "tradeDate": base_data["value_date"],
        "currencyPair": base_data["currency_pair"],
        "amountBought": base_data["amount"],
        "amountSold": base_data["amount"],
        "exchangeRate": "80"
    }
    return create_swift_message("MT300", base_data, additional_fields)

def MT540(source_country, destination_country):
    base_data = generate_base_data(source_country, destination_country)
    additional_fields = {
        "category": "Securities and Investment Transactions",
        "tradeDate": base_data["value_date"],
        "settlementDate": base_data["value_date"],
        "financialInstrument": {
            "isin": base_data["transaction_reference_number"],
            "quantity": 1,
            "price": base_data["amount"]
        }
    }
    return create_swift_message("MT540", base_data, additional_fields)

def MT700(source_country, destination_country):
    base_data = generate_base_data(source_country, destination_country)
    additional_fields = {
        "category": "Bill of Exchange and Guarantees",
        "sequenceOfTotal": "1/1",
        "formOfDocumentaryCredit": Faker().bothify(text='??????##XXX').upper(),
        "documentaryCreditNumber": Faker().bothify(text='??????##XXX').upper(),
        "dateOfIssue": base_data["value_date"],
        "applicableRules": Faker().bothify(text='??????##XXX').upper(),
        "dateAndPlaceOfExpiry": {
            "date": base_data["value_date"],
            "place": "New York, USA"
        },
        "applicant": {
            "name": base_data["sender"]["name"],
            "address": base_data["sender"]["address"]
        },
        "beneficiary": {
            "name": base_data["receiver"]["name"],
            "address": base_data["receiver"]["address"]
        },
        "currencyCodeAmount": {
            "currency": base_data["currency"],
            "amount": base_data["amount"]
        },
        "availableWithBy": {
            "bank": base_data["receiver_bank_code"],
            "method": "BY PAYMENT"
        },
        "descriptionOfGoods": "Electronics",
        "documentsRequired": [
            "Commercial Invoice",
            "Packing List",
            "Bill of Lading"
        ],
        "additionalConditions": "None",
        "charges": "ALL BANKING CHARGES OUTSIDE ISSUING BANK'S COUNTRY ARE FOR BENEFICIARY'S ACCOUNT",
        "confirmationInstructions": "WITHOUT"
    }
    return create_swift_message("MT700", base_data, additional_fields)

def generate_data():
    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400

    number_of_records = data.get('Number_Of_Records')
    source_country = data.get("source_country")
    destination_country = data.get("destination_country")
    message_type = data.get("type")

    if not source_country or not destination_country:
        return jsonify({"error": "Source country and destination country are required"}), 400

    if message_type not in ["MT103", "MT202", "MT300", "MT540", "MT700"]:
        return jsonify({"error": "Invalid message type"}), 400

    generated_data = Parallel(n_jobs=-1)(delayed(globals()[message_type])(source_country, destination_country) for _ in range(number_of_records))
    return jsonify(generated_data), 200

def render_data_generator(app):
    app.add_url_rule('/generate', 'generate_mt202_api', generate_data, methods=['POST'])
    return app

if __name__ == "__main__":
    app = render_data_generator(app)
    app.run(debug=True)
