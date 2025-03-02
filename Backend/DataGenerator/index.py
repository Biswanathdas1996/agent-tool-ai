from flask import Flask, request, jsonify
from faker import Faker
from datetime import datetime, timedelta
import random
import pycountry
import json
from DataGenerator.helper import generate_bank_account_number, Generate_Bank_Name, get_random_bank, get_locale, get_currency_code, generate_transaction_reference, generate_address, generate_name




try:
    with open('DataGenerator/banks.json', 'r', encoding='utf-8') as file:
        banks_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    banks_data = {}


def generate_base_data(source_country, destination_country):
    transaction_reference_number = generate_transaction_reference()
    value_date = (datetime.now() - timedelta(days=random.randint(1, 100))).strftime('%Y-%m-%d')
    currency = get_currency_code(destination_country)
    currencyPair = f"{get_currency_code(destination_country)}/{get_currency_code(source_country)}"
    amount = round(random.uniform(1000, 100000), 2)
    sender_bank = get_random_bank(source_country)
    sender_bank_code = Faker().bothify(text='??????##XXX').upper()
    # "swift_bic": Faker().bothify(text='??????##XXX').upper()
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
    return transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code


def MT103(source_country, destination_country):
    transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code = generate_base_data(source_country, destination_country)
    return {
        "swift": {
            "category": "Customer Payments and Cheques",
            "messageType": "MT103",
            "category": "Customer Payments and Cheques",
            "sender": sender_bank_code,
            "receiver": receiver_bank_code,
            "transactionReferenceNumber": transaction_reference_number,
            "valueDate": value_date,
            "currency": currency,
            "amount": amount,
            "orderingCustomer": {
                "name": sender,
                "accountNumber": sender_bank_code
            },
            "beneficiaryCustomer": {
                "name": receiver,
                "accountNumber": receiver_bank_code
            },
            "detailsOfCharges": "SHA"
        }
    }

def MT202(source_country, destination_country):
    transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code = generate_base_data(source_country, destination_country)
    return {
        "swift": {
            "category": "Financial Institution Transfers",
            "messageType": "MT202",
            "sender": sender_bank_code,
            "receiver": receiver_bank_code,
            "transactionReferenceNumber": transaction_reference_number,
            "valueDate": value_date,
            "currency": currency,
            "amount": amount,
            "orderingInstitution": {
                "name": sender_bank,
                "bic": sender_bank_code
            },
            "beneficiaryInstitution": {
                "name": receiver_bank,
                "bic": receiver_bank_code
            },
            "detailsOfCharges": "OUR"
        }
    }
     
def MT300(source_country, destination_country):
    transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code = generate_base_data(source_country, destination_country)
    return {
        "swift": {
            "category": "Foreign Exchange and Money Market",
            "messageType": "MT300",
            "sender": sender_bank_code,
            "receiver": receiver_bank_code,
            "transactionReferenceNumber": transaction_reference_number,
            "tradeDate": value_date,
            "valueDate": value_date,
            "currencyPair": currencyPair,
            "amountBought": amount,
            "amountSold": amount,
            "exchangeRate": "80",
            "orderingInstitution": {
                "name": sender_bank,
                "bic": sender_bank_code
            },
            "beneficiaryInstitution": {
                "name": receiver_bank,
                "bic": receiver_bank_code
            }
        }
    }

def MT540(source_country, destination_country):
    transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code = generate_base_data(source_country, destination_country)
    return {
            "swift": {
                "category": "Securities and Investment Transactions",
                "messageType": "MT540",
                "sender": sender_bank_code,
                "receiver": receiver_bank_code,
                "transactionReferenceNumber": transaction_reference_number,
                "tradeDate": value_date,
                "settlementDate": value_date,
                "financialInstrument": {
                    "isin": transaction_reference_number,
                    "quantity": 1,
                    "price": amount
                },
                "orderingInstitution": {
                    "name": sender_bank,
                    "bic": sender_bank_code
                },
                "beneficiaryInstitution": {
                    "name": receiver_bank,
                    "bic": receiver_bank_code
                }
            }
    }

def MT700(source_country, destination_country):
    transaction_reference_number, value_date, currency, currencyPair, amount, sender_bank, receiver_bank, sender, receiver, sender_bank_code, receiver_bank_code = generate_base_data(source_country, destination_country)
    return {
            "swift": {
                "messageType": "MT700",
                "category": "Bill of Exchange and Guarantees",
                "sender": sender_bank_code,
                "receiver": receiver_bank_code,
                "transactionReferenceNumber": transaction_reference_number,
                "sequenceOfTotal": "1/1",
                "formOfDocumentaryCredit": Faker().bothify(text='??????##XXX').upper(),
                "documentaryCreditNumber": Faker().bothify(text='??????##XXX').upper(),
                "dateOfIssue": value_date,
                "applicableRules": Faker().bothify(text='??????##XXX').upper(),
                "dateAndPlaceOfExpiry": {
                    "date": value_date,
                    "place": "New York, USA"
                },
                "applicant": {
                    "name": sender["name"],
                    "address": sender["address"]
                },
                "beneficiary": {
                    "name": receiver["name"],
                    "address": receiver["address"]
                },
                "currencyCodeAmount": {
                    "currency": currency,
                    "amount": amount
                },
                "availableWithBy": {
                    "bank": receiver_bank_code,
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
    }



def generate_data():
    # Validate request body
    data = request.json
    Number_Of_Records = data.get('Number_Of_Records')
    if not data:
        return jsonify({"error": "Request body is missing"}), 400
    
    
    source_country = data.get("source_country")
    destination_country = data.get("destination_country")
    
    if not source_country or not destination_country:
        return jsonify({"error": "Source country and destination country are required"}), 400
    
    # Generate and return the MT202 data
    message_type = data.get("type")
    if message_type not in ["MT103", "MT202", "MT300", "MT540", "MT700"]:
        return jsonify({"error": "Invalid message type"}), 400

    generated_data = [globals()[message_type](source_country, destination_country) for i in range(Number_Of_Records)]
    return jsonify(generated_data), 200



# Function to add the validation endpoint to the Flask app
def render_data_generator(app):
    app.add_url_rule('/generate', 'generate_mt202_api', generate_data, methods=['POST'])
    return app
