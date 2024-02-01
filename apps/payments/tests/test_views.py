from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.website.models import Product, Order


class CreateCheckoutSessionViewTest(TestCase):
    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_product = test_product_user1 = Product(id=1, user=test_authorized_user, name="Baclazhan", price=1, description="test")
        test_product_user1.save()
        test_product.save()
        test_order = Order(user=test_authorized_user, item=test_product, count=1, total_price=1, paid=0)
        test_order.save()
        self.prik = test_order.pk

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.post("/website/create_checkout_session/"+str(self.prik)+"/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.post(reverse("create_checkout_session", kwargs={"order_id": str(self.prik)}))
        self.assertEqual(resp.status_code, 200)

    def test_view_access_without_login(self):
        resp = self.client.post(reverse("create_checkout_session", kwargs={"order_id": str(self.prik)}))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.post(reverse("create_checkout_session", kwargs={"order_id": str(self.prik)}))
        self.assertRedirects(resp, "/website/login/?next=/website/create_checkout_session/"+str(self.prik)+"/")

