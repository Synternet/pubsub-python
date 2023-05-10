from datetime import datetime
import random
import json
import nkeys


def generate_jti():
    """
    Generates a unique identifier composed of timestamp and random numbers.

    Returns:
        str: A unique identifier.
    """
    timestamp = round(datetime.now().timestamp())
    random_number = str(random.random())[2:-1]
    return f"{timestamp}{random_number}"


def generate_iat():
    """
    Generates a timestamp.

    Returns:
        int: A timestamp.
    """
    return round(datetime.now().timestamp())


def get_nats_config():
    """
    Generates default NATS configuration.

    Returns:
        dict: A dictionary with the NATS configuration.
    """
    return {'pub': {}, 'sub': {}, 'subs': -1, 'data': -1, 'payload': -1, 'type': 'user', 'version': 2}


def sign_jwt(payload, account):
    """
    Signs a JWT with the provided account.

    Args:
        payload (dict): A dictionary with the payload data.
        account (nkeys.KeyPair): An account object.

    Returns:
        str: A signed JWT.
    """
    header = {"typ": "JWT", "alg": "ed25519-nkey"}
    header_encoded = nkeys.base64.urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode()).decode().strip(
        '=')
    payload_encoded = nkeys.base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode()).decode().strip('=')

    jwtbase = header_encoded + '.' + payload_encoded
    signature = nkeys.base64.b64encode(bytearray(account.sign(jwtbase.encode()))).decode().strip('=').replace("+",
                                                                                                              "-").replace(
        "/", "_")

    return jwtbase + '.' + signature


def create_app_jwt(seed):
    """
    Creates an application JWT.

    Args:
        seed (str): A string with the seed for the account.

    Returns:
        str: A JWT.
    """
    encoded_acc_seed = bytearray(seed.encode())
    account = nkeys.from_seed(encoded_acc_seed)
    acc_pubkey = account.public_key

    payload = {
        'jti': generate_jti(),
        'iat': generate_iat(),
        'iss': acc_pubkey.decode(),
        'name': 'developer',
        'sub': acc_pubkey.decode(),
        'nats': get_nats_config()
    }

    jwt = sign_jwt(payload, account)

    creds = f"-----BEGIN NATS USER JWT-----\n{jwt}\n------END NATS USER JWT------\n\n************************* IMPORTANT *************************\nNKEY Seed printed below can be used to sign and prove identity.\nNKEYs are sensitive and should be treated as secrets. \n\n-----BEGIN USER NKEY SEED-----\n{seed}\n------END USER NKEY SEED------\n\n*************************************************************"
    return creds
