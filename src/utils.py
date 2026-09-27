import random
import numpy as np

from faker import Faker

from src.config import RANDOM_SEED

fake = Faker("en_IN")

random.seed(RANDOM_SEED)

np.random.seed(RANDOM_SEED)


def random_phone():

    return fake.phone_number()


def random_email(name):

    return (
        name.lower()
        .replace(" ", "")
        + "@gmail.com"
    )


def random_gender():

    return random.choice(
        [
            "Male",
            "Female"
        ]
    )


def random_segment():

    return random.choice(
        [
            "Consumer",
            "Corporate",
            "Home Office"
        ]
    )


def random_payment():

    return random.choice(
        [
            "UPI",
            "COD",
            "Credit Card",
            "Debit Card",
            "EMI",
            "Net Banking"
        ]
    )


def random_discount():

    return random.choice(
        [
            0,
            5,
            10,
            15,
            20,
            25,
            30
        ]
    )