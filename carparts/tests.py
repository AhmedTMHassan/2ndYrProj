from django.test import TestCase
from django.urls import reverse
from .models import Part, Brand, Category
import uuid

class CategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Oil'
        )

    def test_category_listing(self):
        self.assertEqual(f'{self.category.name}', 'Oil')

    def test_category_list_view(self):
        response = self.client.get(reverse('carparts:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oil')
        self.assertTemplateUsed(response, 'shop/category.html')

    def test_category_str_representation(self):
        expected_str = "Oil"
        self.assertEqual(str(self.category), expected_str)


class BrandTests(TestCase):
    def setUp(self):
        
        self.category = Category.objects.create(name='Oil')
        
        
        self.brand = Brand.objects.create(
            id=uuid.uuid4(),
            name='Castrol'
        )
        self.brand.category.add(self.category)

    def test_brand_listing(self):
        self.assertEqual(f'{self.brand.name}', 'Castrol')

    def test_brand_list_view(self):
        response = self.client.get(reverse('carparts:brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Castrol')
        self.assertTemplateUsed(response, 'shop/brand.html')

    def test_brand_str_representation(self):
        expected_str = "Castrol"
        self.assertEqual(str(self.brand), expected_str)



class PartTests(TestCase):
    def setUp(self):
        self.part = Part.objects.create(
            title='Castrol Edge',
            
            price='73.99',
            stock='10',
            description='Advances in engine technology have led to increased power and efficiency, meaning engines work harder and under higher pressures than ever before.',
            
        )

    def test_part_listing(self):
        self.assertEqual(f'{self.part.title}', 'Castrol Edge')
        self.assertEqual(f'{self.part.price}', '73.99')
        self.assertEqual(f'{self.part.stock}', '10')
        self.assertEqual(f'{self.part.description}', 'Advances in engine technology have led to increased power and efficiency, meaning engines work harder and under higher pressures than ever before.')


    def test_part_list_view(self):
        response = self.client.get(reverse('carparts:part_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Castrol Edge')
        self.assertTemplateUsed(response, 'shop/part.html')

    def test_part_detail_view(self):
     
        response = self.client.get(reverse('carparts:part_detail', args=[self.part.id]))
        no_response = self.client.get('/part/12345/')  

        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Castrol Edge')
        self.assertTemplateUsed(response, 'part_detail.html')


    def test_part_str_representation(self):
        expected_str = "Castrol Edge"
        self.assertEqual(str(self.part), expected_str)
