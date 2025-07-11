from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Bouquet, Order

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="pass")
        self.bouquet = Bouquet.objects.create(name="Тестовый букет", price=999.99)

    def test_order_creation(self):
        order = Order.objects.create(user=self.user)
        order.bouquets.add(self.bouquet)
        self.assertEqual(order.user.username, "testuser")
        self.assertEqual(order.bouquets.first().name, "Тестовый букет")
