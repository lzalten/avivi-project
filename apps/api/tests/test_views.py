from django.test import TestCase
from django.urls import reverse


class CreateEthWalletViewTest(TestCase):

    def test_creation_address_url(self):
        resp = self.client.get("/api/create_eth_wallet/")
        self.assertEqual(resp.status_code, 200)

    def test_creation_address_url_by_name(self):
        resp = self.client.get(reverse("create_eth_wallet"))
        self.assertEqual(resp.status_code, 200)

    def test_check_response(self):
        resp = self.client.get(reverse("create_eth_wallet"))
        self.assertTrue("address" in resp.json() and "private_key" in resp.json())


class CreateTronWalletTest(TestCase):
    def test_creation_address_url(self):
        resp = self.client.get("/api/create_tron_wallet/")
        self.assertEqual(resp.status_code, 200)

    def test_creation_address_url_by_name(self):
        resp = self.client.get(reverse("create_tron_wallet"))
        self.assertEqual(resp.status_code, 200)

    def test_check_response(self):
        resp = self.client.get(reverse("create_tron_wallet"))
        self.assertTrue("address" in resp.json() and "private_key" in resp.json())


class CreateEthTransactionTest(TestCase):
    def setUp(self):
        self.test_private_k1 = "0x44ed27cfc2e8e12f96270fca546c952b76ff123a9776007059393a04bef4ec02"
        self.test_public_k1 = "0x5c6dc8813Eb822761866DcB868b122a6F58eC22A"
        self.test_private_k2 = "0x05147f5144f011c8b914063c73758eba158a1b057620a5b950d00d8f8b374f52"
        self.test_public_k2 = "0x1f82Cc755Ad63e7Fdf3FFAc4F5c2d1D633105108"

    def test_view_by_url(self):
        resp = self.client.get("/api/send_eth/"+self.test_private_k2+"/0.0000000001/"+self.test_public_k1)
        self.assertEqual(resp.status_code, 200)

    def test_view_by_name(self):
        resp = self.client.get(reverse("send_eth", kwargs={"pk": self.test_private_k2,
                                                           "amount": "0.0000000000001",
                                                           "rec_address": self.test_public_k1}))
        self.assertEqual(resp.status_code, 200)


class CreateErc20TransactionTest(TestCase):
    def setUp(self):
        self.test_private_k1 = "0x44ed27cfc2e8e12f96270fca546c952b76ff123a9776007059393a04bef4ec02"
        self.test_public_k1 = "0x5c6dc8813Eb822761866DcB868b122a6F58eC22A"
        self.test_private_k2 = "0x05147f5144f011c8b914063c73758eba158a1b057620a5b950d00d8f8b374f52"
        self.test_public_k2 = "0x1f82Cc755Ad63e7Fdf3FFAc4F5c2d1D633105108"

    def test_view_by_url(self):
        resp = self.client.get("/api/send_erc20/"+self.test_private_k2+"/0.0000000001/"+self.test_public_k1)
        self.assertEqual(resp.status_code, 200)

    def test_view_by_name(self):
        resp = self.client.get(reverse("send_erc20", kwargs={"pk": self.test_private_k2,
                                                             "amount": "0.0000000000001",
                                                             "rec_address": self.test_public_k1}))
        self.assertEqual(resp.status_code, 200)