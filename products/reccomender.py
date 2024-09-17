# recommender.py
from .models import Product, ProductRecommendation


class Recommender:
    """Recommender class to handle product recommendations using the database."""

    def products_bought(self, products):
        """Register products bought together in the database."""
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    recommendation, created = ProductRecommendation.objects.get_or_create(
                        product_id=product_id,
                        recommended_product_id=with_id
                    )
                    recommendation.score += 1
                    recommendation.save()

    def suggest_products_for(self, products, max_results=6):
        """Suggest products based on the provided list of products."""
        product_ids = [p.id for p in products]
        recommendations = ProductRecommendation.objects.filter(product_id__in=product_ids).exclude(
            recommended_product_id__in=product_ids
        ).order_by('-score')[:max_results]

        recommended_product_ids = list(recommendations.values_list('recommended_product_id', flat=True))
        suggested_products = list(Product.objects.filter(id__in=recommended_product_ids))
        suggested_products.sort(key=lambda x: recommended_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        """Clear all product purchase data from the database."""
        ProductRecommendation.objects.all().delete()