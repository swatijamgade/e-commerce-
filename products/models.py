from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    """
    Product categories
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Product model to store shop products, having category as a foreign key
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)  # abc-xyz-sdfsdfsadf-sdfgadf234-sdfsdfr34
    image = models.ImageField(upload_to='products/images/%Y/%m/%d', blank=True)
    image_url = models.URLField(blank=True)
    video = models.FileField(upload_to='products/videos/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])


class ProductRecommendation(models.Model):
    product = models.ForeignKey(Product, related_name='recommendations', on_delete=models.CASCADE)
    recommended_product = models.ForeignKey(Product, related_name='recommended_by', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'recommended_product')