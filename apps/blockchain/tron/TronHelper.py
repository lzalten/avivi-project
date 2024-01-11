import codecs
from hexbytes import HexBytes
from tronpy import Tron
from tronpy.providers import HTTPProvider


class TronHelper:
    def __init__(self):
        self.API_URL_BASE = 'https://nile.trongrid.io'
        self.full_node = HTTPProvider(self.API_URL_BASE)
        self.tron = Tron(self.full_node)
        self.trc20_abi = '{"entrys":[{"inputs":[{"name":"name_","type":"string"},{"name":"symbol_","type":"string"}],"stateMutability":"Nonpayable","type":"Constructor"},{"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"name":"value","type":"uint256"}],"name":"Approval","type":"Event"},{"inputs":[{"name":"userAddress","type":"address"},{"name":"relayerAddress","type":"address"},{"name":"functionSignature","type":"bytes"}],"name":"MetaTransactionExecuted","type":"Event"},{"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"Event"},{"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"Transfer","type":"Event"},{"outputs":[{"type":"string"}],"name":"ERC712_VERSION","stateMutability":"view","type":"function"},{"outputs":[{"type":"uint256"}],"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","stateMutability":"view","type":"function"},{"outputs":[{"type":"bool"}],"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","stateMutability":"nonpayable","type":"function"},{"outputs":[{"type":"uint256"}],"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","stateMutability":"view","type":"function"},{"outputs":[{"type":"uint8"}],"name":"decimals","stateMutability":"view","type":"function"},{"outputs":[{"type":"bool"}],"inputs":[{"name":"spender","type":"address"},{"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","stateMutability":"nonpayable","type":"function"},{"outputs":[{"type":"bytes"}],"inputs":[{"name":"userAddress","type":"address"},{"name":"functionSignature","type":"bytes"},{"name":"sigR","type":"bytes32"},{"name":"sigS","type":"bytes32"},{"name":"sigV","type":"uint8"}],"name":"executeMetaTransaction","stateMutability":"payable","type":"function"},{"outputs":[{"type":"uint256"}],"name":"getChainId","stateMutability":"pure","type":"function"},{"outputs":[{"type":"bytes32"}],"name":"getDomainSeperator","stateMutability":"view","type":"function"},{"outputs":[{"name":"nonce","type":"uint256"}],"inputs":[{"name":"user","type":"address"}],"name":"getNonce","stateMutability":"view","type":"function"},{"outputs":[{"type":"bool"}],"inputs":[{"name":"spender","type":"address"},{"name":"addedValue","type":"uint256"}],"name":"increaseAllowance","stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"amount","type":"uint256"}],"name":"mint","stateMutability":"nonpayable","type":"function"},{"outputs":[{"type":"string"}],"name":"name","stateMutability":"view","type":"function"},{"outputs":[{"type":"address"}],"name":"owner","stateMutability":"view","type":"function"},{"name":"renounceOwnership","stateMutability":"nonpayable","type":"function"},{"outputs":[{"type":"string"}],"name":"symbol","stateMutability":"view","type":"function"},{"outputs":[{"type":"uint256"}],"name":"totalSupply","stateMutability":"view","type":"function"},{"outputs":[{"type":"bool"}],"inputs":[{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","stateMutability":"nonpayable","type":"function"},{"outputs":[{"type":"bool"}],"inputs":[{"name":"sender","type":"address"},{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transferFrom","stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","stateMutability":"nonpayable","type":"function"}]}'
        self.usdt_token_address = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'

    def create_tron_wallet(self):
        wallet = self.tron.generate_address()
        return {
            'address': wallet['base58check_address'],
            'private_key': wallet['private_key'],
        }

    def send_trx(self, private_key: str, amount: str, wallet: str):
        try:
            sender_address = private_key.public_key.to_base58check_address()
            txn = (
                self.tron.trx.transfer(sender_address, str(wallet), int(amount))
                .memo("Testnet transaction")
                .build()
                .inspect()
                .sign(private_key)
                .broadcast()
            )
            return txn.wait()

        except Exception as ex:
            return ex

    def send_trc20(self, private_key, amount, recipient_address, token_address=None):
        if token_address is None:
            token_address = self.usdt_token_address
        try:
            address = private_key.public_key.to_base58check_address()
            amount_in_wei = int(amount * 10 ** 6)
            token_contract = self.tron.get_contract(token_address)
            token_contract.abi = self.trc20_abi
            tx = (
                token_contract.functions.transfer(
                    recipient_address,
                    amount_in_wei)
                .with_owner(address)
                .fee_limit(5_000_000)
                .build()
                .sign(private_key)
            )
            broadcasted_tx = tx.broadcast().wait()

            return HexBytes(codecs.decode(broadcasted_tx['id'], 'hex_codec'))

        except Exception as ex:
            return ex

