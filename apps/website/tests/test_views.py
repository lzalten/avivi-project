from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.website.models import Product, Room


class RegisterViewTest(SimpleTestCase):
    def setUpTestData(self):
        self.a = 0

    def test_view_url_exist_at_desired_location(self):
        resp = self.client.get("/website/register/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("register"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'register.html')


class LoginViewTest(SimpleTestCase):

    def test_view_url_exist_at_desired_location(self):
        resp = self.client.get("/website/login/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'login.html')


class LogoutViewTest(TestCase):
    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()

    def test_view_redirect_unauthorized_users(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/website/login/?next=/website/logout/")

    def test_view_redirect_authorized_users(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/website/login/")


class ProductListTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/products/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("product_list"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('product_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'product_list.html')

    def test_view_list_of_products(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('product_list'))

        # check if logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # check if we got list of books
        self.assertTrue('products' in resp.context)

    def test_view_access_without_login(self):
        resp = self.client.get(reverse('product_list'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse('product_list'))
        self.assertRedirects(resp, "/website/login/?next=/website/products/")


class CreateOrderTest(TestCase):
    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_authorized_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_authorized_user2.save()
        test_product = Product(id=1, user=test_authorized_user, name="test", price=1, description="test")
        test_product.save()
        test_product2 = Product(id=2, user=test_authorized_user, name="test2", price=2, description="test2")
        test_product2.save()
        test_product3 = Product(id=3, user=test_authorized_user2, name="test3", price=3, description="test3")
        test_product3.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/create_order/3/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("create_order", kwargs={"product_id": 3}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("create_order", kwargs={"product_id": 3}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'create_order.html')

    def test_view_access_without_login(self):
        resp = self.client.get(reverse("create_order", kwargs={"product_id": 3}))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse("create_order", kwargs={"product_id": 3}))
        self.assertRedirects(resp, "/website/login/?next=/website/create_order/3/")


class OrderListTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()

    def test_vew_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/orders/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("order_list"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('order_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'order_list.html')

    def test_view_list_of_orders(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('order_list'))

        # check if logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # check if we got list of books
        self.assertTrue('orders' in resp.context)

    def test_view_access_without_login(self):
        resp = self.client.get(reverse('order_list'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse('order_list'))
        self.assertRedirects(resp, "/website/login/?next=/website/orders/")


class AddProductTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/add_product/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("add_product"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("add_product"))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'add_product.html')

    def test_view_access_without_login(self):
        resp = self.client.get(reverse("add_product"))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse("add_product"))
        self.assertRedirects(resp, "/website/login/?next=/website/add_product/")

    def test_view_post_request(self):
        test_name = "Dub"
        false_price = "ffr"
        test_price = 5
        test_description = "test"
        self.client.login(username='testuser1', password='12345')
        resp = self.client.post(reverse('add_product'), {'name': test_name,
                                                         'price': test_price,
                                                         'description': test_description})
        self.assertRedirects(resp, "/website/products/")
        false_resp = self.client.post(reverse('add_product'), {'name': test_name,
                                                               'price': false_price,
                                                               'description': test_description})
        self.assertEqual(false_resp.status_code, 200)


class EditProductTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_authorized_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_authorized_user2.save()

        test_product_user1 = Product(id=1, user=test_authorized_user, name="Baclazhan", price=1, description="test")
        test_product_user1.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/edit_product/1/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("edit_product", kwargs={"product_id": 1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("edit_product", kwargs={"product_id": 1}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'edit_product.html')

    def test_view_access_without_login(self):
        resp = self.client.get(reverse("add_product"))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse("edit_product", kwargs={"product_id": 1}))
        self.assertRedirects(resp, "/website/login/?next=/website/edit_product/1/")

    def test_view_post_request(self):

        test_name = "Dub"
        false_price = "ffr"
        test_price = 5
        test_description = "test"
        self.client.login(username='testuser1', password='12345')
        resp = self.client.post(reverse("edit_product", kwargs={"product_id": 1}), {'name': test_name,
                                                                                    'price': test_price,
                                                                                    'description': test_description})
        self.assertRedirects(resp, reverse('user_products'))
        false_resp = self.client.post(reverse("edit_product", kwargs={"product_id": 1}), {'name': test_name,
                                                                                          'price': false_price,
                                                                                          'description': test_description})
        self.assertEqual(false_resp.status_code, 200)


class UserProductsTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()

    def test_vew_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/user_products/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("user_products"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('user_products'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'user_products.html')

    def test_view_list_of_orders(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('user_products'))

        # check if logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # check if we got list of books
        self.assertTrue('products' in resp.context)

    def test_view_access_without_login(self):
        resp = self.client.get(reverse('user_products'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse('user_products'))
        self.assertRedirects(resp, "/website/login/?next=/website/user_products/")


class RoomsTest(TestCase):
    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_authorized_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_authorized_user.save()
        test_room = Room(name='test', slug='dsdfdsfddsf', client=test_authorized_user, manager=test_authorized_user2)
        test_room.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/chat/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("rooms"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('rooms'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'rooms.html')

    def test_view_list_of_rooms(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('rooms'))

        # check if logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # check if we got list of books
        self.assertTrue('rooms' in resp.context)

    def test_view_access_without_login(self):
        resp = self.client.get(reverse('rooms'))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse('rooms'))
        self.assertRedirects(resp, "/website/login/?next=/website/chat/")


class RoomTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_authorized_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_authorized_user.save()
        test_room = Room(name='test', slug='kKwkiVIulWZprJpQcbBx', client=test_authorized_user, manager=test_authorized_user2)
        test_room.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/chat/kKwkiVIulWZprJpQcbBx")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("room", kwargs={"slug": 'kKwkiVIulWZprJpQcbBx'}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("room", kwargs={"slug": 'kKwkiVIulWZprJpQcbBx'}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'room.html')

    def test_view_list_of_room(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("room", kwargs={"slug": 'kKwkiVIulWZprJpQcbBx'}))

        # check if logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # check if we got list of books
        self.assertTrue('room' in resp.context and 'slug' in resp.context and 'messages' in resp.context)

    def test_view_access_without_login(self):
        resp = self.client.get(reverse("room", kwargs={"slug": 'kKwkiVIulWZprJpQcbBx'}))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse("room", kwargs={"slug": 'kKwkiVIulWZprJpQcbBx'}))
        self.assertRedirects(resp, "/website/login/?next=/website/chat/kKwkiVIulWZprJpQcbBx")


class CreateRoomTest(TestCase):

    def setUp(self):
        test_authorized_user = User.objects.create_user(username='testuser1', password='12345')
        test_authorized_user.save()
        test_authorized_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_authorized_user.save()
        test_room = Room(name='test', slug='kKwkiVIulWZprJpQcbBx', client=test_authorized_user,
                         manager=test_authorized_user2)
        test_room.save()

    def test_view_url_exist_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get("/website/chat/create/")
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("create"))
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse("create"))

        self.assertRedirects(resp, reverse("rooms"))

    def test_view_access_without_login(self):
        resp = self.client.get(reverse("create"))
        self.assertEqual(resp.status_code, 302)

    def test_view_redirect_login(self):
        resp = self.client.get(reverse("create"))
        self.assertRedirects(resp, "/website/login/?next=/website/chat/create/")





