
from ..models.category_type import CategoryType

def get_category_type_list():
    category_types = CategoryType.query.filter_by(status=1).all()
    return [category.category_type.lower() for category in category_types]