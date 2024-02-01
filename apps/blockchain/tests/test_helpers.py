from django.test import TestCase

from apps.blockchain.ethereum.EthereumHelper import EthereumHelper
from apps.blockchain.tron.TronHelper import TronHelper


class EthereumHelperTest(TestCase):

    def setUp(self):
        self.eth_helper = EthereumHelper()
        self.test_private_k1 = "0x44ed27cfc2e8e12f96270fca546c952b76ff123a9776007059393a04bef4ec02"
        self.test_public_k1 = "0x5c6dc8813Eb822761866DcB868b122a6F58eC22A"
        self.test_private_k2 = "0x05147f5144f011c8b914063c73758eba158a1b057620a5b950d00d8f8b374f52"
        self.test_public_k2 = "0x1f82Cc755Ad63e7Fdf3FFAc4F5c2d1D633105108"

    def test_creation_address(self):
        ret = self.eth_helper.create_ethereum_account()
        self.assertTrue('address' in ret)
        self.assertTrue('private_key' in ret)

        # if correct address value
        self.assertEqual(len(ret['address']), 42)

        # if correct private_key value
        self.assertEqual(len(ret['private_key']), 66)

    def test_sending_eth(self):
        ret = self.eth_helper.send_eth(self.test_private_k2, "0.00000000001", self.test_public_k1)
        self.assertTrue(ret)

    def test_sending_erc20(self):
        ret = self.eth_helper.send_erc20(self.test_private_k2, "0.00000000001", self.test_public_k1)
        self.assertTrue(ret)


class TronHelperTest(TestCase):

    def setUp(self):
        self.trn = TronHelper()

    def test_creation_address(self):
        ret = self.trn.create_tron_wallet()
        self.assertTrue('address' in ret)
        self.assertTrue('private_key' in ret)

        # if correct address value
        self.assertEqual(len(ret['address']), 34)

        # if correct private_key value
        self.assertEqual(len(ret['private_key']), 64)



