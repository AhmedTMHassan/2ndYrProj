from django.test import TestCase
from django.urls import reverse
from .models import Category, Brand, Part

class CategoryModelTest(TestCase):
    
    def setUp(self):
        self.categories = [
            "Car Parts",
            "Car Accessories",
            "Cleaning",
            "Oil",
            "Number Plates"
        ]
        for category in self.categories:
            Category.objects.create(name=category)

    def test_category_creation(self):
        for category in self.categories:
            self.assertTrue(Category.objects.filter(name=category).exists())

    def test_category_str_method(self):
        category = Category.objects.get(name="Car Parts")
        self.assertEqual(str(category), "Car Parts")


class BrandModelTest(TestCase):
    
    def setUp(self):
        self.brands = [
            "Autoglym", "Koch Chemie", "AutoSmart", "Stjarnagloss",
            "Flex", "Designer Fragances", "Castrol", "Total", "Mobil",
            "Shell", "Petronas", "Valvoline", "Team Heko", "Thule",
            "Noco", "BlackVue", "Foliatec", "MST Performance",
            "Akrapovic", "Maxton Design", "Mountune", "Michelin"
        ]
        for brand in self.brands:
            Brand.objects.create(name=brand)

    def test_brand_creation(self):
        for brand in self.brands:
            self.assertTrue(Brand.objects.filter(name=brand).exists())

    def test_brand_str_method(self):
        brand = Brand.objects.get(name="Autoglym")
        self.assertEqual(str(brand), "Autoglym")


class PartModelTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Car Parts")
        self.brand = Brand.objects.create(name="Akrapovic")
        self.part = Part.objects.create(
            title="Evolution Line (Titanium) RS3",
            price=2999.99,
            stock=5,
            description="High-performance titanium exhaust system for Audi RS3."
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)

    def test_part_creation(self):
        self.assertEqual(self.part.title, "Evolution Line (Titanium) RS3")
        self.assertEqual(self.part.price, 2999.99)
        self.assertEqual(self.part.stock, 5)
        self.assertEqual(self.part.description, "High-performance titanium exhaust system for Audi RS3.")

    def test_part_category_association(self):
        self.assertIn(self.category, self.part.category.all())

    def test_part_brand_association(self):
        self.assertIn(self.brand, self.part.brand.all())

    def test_part_str_method(self):
        self.assertEqual(str(self.part), "Evolution Line (Titanium) RS3")


class ShopViewsTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Oil")
        self.brand = Brand.objects.create(name="Castrol")
        self.part = Part.objects.create(
            title="Castrol Edge 5W-30",
            price=45.99,
            stock=20,
            description="High-performance synthetic engine oil."
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oil")
        self.assertTemplateUsed(response, 'shop/category.html')

    def test_brand_list_view(self):
        response = self.client.get(reverse('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Castrol")
        self.assertTemplateUsed(response, 'shop/brand.html')

    def test_part_list_view(self):
        response = self.client.get(reverse('part_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Castrol Edge 5W-30")
        self.assertTemplateUsed(response, 'shop/part.html')

    def test_part_detail_view(self):
        response = self.client.get(reverse('part_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Castrol Edge 5W-30")


class ShopUrlsTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Car Accessories")
        self.brand = Brand.objects.create(name="Thule")
        self.part = Part.objects.create(
            title="Complete Thule Car Roof Rack System",
            price=249.99,
            stock=10,
            description="Durable and high-quality roof rack system."
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)

    def test_category_list_url(self):
        url = reverse('category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_brand_list_url(self):
        url = reverse('brand_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_part_list_url(self):
        url = reverse('part_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
