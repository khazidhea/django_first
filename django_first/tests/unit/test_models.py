from django_first.models import Category


def test_category(db, data):
    category = Category.objects.first()
    assert str(category) == 'fruits'
