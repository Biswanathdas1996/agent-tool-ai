from flask import Flask, request, jsonify
from faker import Faker
from datetime import datetime
import random
import pycountry
import json
import logging

logging.basicConfig(level=logging.INFO)

def load_banks_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading banks data: {e}")
        return {}

banks_data = load_banks_data('DataGenerator/banks.json')

def get_closest_country_name(input_name):
    """ Find the closest matching country name in the dataset. """
    try:
        return pycountry.countries.lookup(input_name).name
    except LookupError:
        for country in banks_data.keys():
            if input_name.lower() in country.lower():
                return country
        return None

def generate_bank_name(country_name):
    """ Generates a default international bank name if the country is not found in banks.json """
    with open("missedcountry.txt", "a") as f:
        f.write(country_name + "\n")
    fake = Faker()
    return f"{fake.company()} International Bank"

def get_random_bank(country_name):
    """ Fetch a random bank name from the given country. If not found, generate one. """
    closest_country = get_closest_country_name(country_name)
    if closest_country and closest_country in banks_data:
        bank_list = banks_data[closest_country]
        if bank_list:
            return random.SystemRandom().choice(bank_list)
        else:
            return f"Bank of {closest_country}"
    return generate_bank_name(country_name)

def generate_bank_account_number():
    """ Generate a random bank account number based on the bank name """
    # Removed seeding to ensure the pseudorandom number generator is safe
    return ''.join([str(random.SystemRandom().randint(0, 9)) for _ in range(10)])

def get_locale(country_name):
    """ Map country names to Faker locales for realistic data generation. """
    locale_map = {
        "United States": "en_US",
        "United Kingdom": "en_GB",
        "France": "fr_FR",
        "Germany": "de_DE",
        "Italy": "it_IT",
        "Spain": "es_ES",
        "Canada": "en_CA",
        "India": "en_IN",
        "China": "zh_CN",
        "Japan": "ja_JP",
        "Brazil": "pt_BR",
        "Russia": "ru_RU",
        "Mexico": "es_MX",
        "Australia": "en_AU",
        "Netherlands": "nl_NL",
        "Sweden": "sv_SE",
        "Switzerland": "de_CH",
        "South Korea": "ko_KR",
        "South Africa": "en_ZA",
        "Argentina": "es_AR",
        "Turkey": "tr_TR",
        "Poland": "pl_PL",
        "Thailand": "th_TH"
    }
    return locale_map.get(country_name, "en_US")

def get_currency_code(country_name):
    """ Get the currency code for a given country name. """
    try:
        country = pycountry.countries.lookup(country_name)
        currency = pycountry.currencies.get(numeric=country.numeric)
        return currency.alpha_3
    except LookupError:
        return "USD"

def generate_transaction_reference():
    """ Generate a transaction reference as YYYYMMDDXXX### """
    today = datetime.now().strftime('%Y%m%d')
    random_letters = Faker().bothify(text='???').upper()
    random_number = random.SystemRandom().randint(100, 999)
    return f"{today}{random_letters}{random_number}"

def generate_address(country):
    """ Generate a realistic address following ISO 20022 format. """
    locale = get_locale(country)
    fake = Faker(locale)
    return {
        "StreetName": fake.street_name(),
        "BuildingNumber": fake.building_number(),
        "PostCode": fake.postcode(),
        "TownName": fake.city(),
        "CountrySubDivision": fake.state() if hasattr(fake, "state") else "",
        "Country": pycountry.countries.lookup(country).alpha_2
    }

def generate_name(country):
    """ Generate a realistic name based on the given country. """
    locale = get_locale(country)
    fake = Faker(locale)
    return fake.name()
