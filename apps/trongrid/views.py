import base58
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


API_URL_BASE = 'https://api.shasta.trongrid.io'


full_node = HTTPProvider(API_URL_BASE)
tron = Tron(full_node)


def create_tron_account():
    address = tron.generate_address()
    return {
        'address': address['base58check_address'],
        'private_key': address['private_key'],
    }


def send_trx(private_key, amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key))
        sender_address = private_key.public_key.to_base58check_address()
        txn = (
            tron.trx.transfer(sender_address, str(wallet), int(amount))
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        return txn.wait()

    except Exception as ex:
        return ex


def send_trc20(private_k, amou, recipient_add):
    try:
        private_key = PrivateKey(bytes.fromhex(private_k))
        address = private_key.public_key.to_base58check_address()
        token_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        recipient_address = recipient_add
        amount = amou
        amount_in_wei = int(amount * 10 ** 6)
        token_contract = tron.get_contract(token_address)
        transaction = token_contract.functions.transfer(recipient_address, amount_in_wei).build_transaction(
            owner_address=address
        )
        signed_txn = tron.trx.sign(transaction, private_key)
        response = tron.trx.broadcast(signed_txn)
        return response

    except Exception as ex:
        return ex
