def load_data(restaurant_db_obj):
    from app.models.schemas import RestaurantSchema
    restaurant_schema = RestaurantSchema()
    data = restaurant_schema.dump(restaurant_db_obj)
    return data

def load_product_data(product_db_obj):
    #db objelerini schemaya uyarlama
    from app.models.schemas import ProductSchema
    product_schema = ProductSchema()
    data = product_schema.dump(product_db_obj)
    return data

def load_order_data(order_db_obj):
    #db objelerini schemaya uyarlama
    from app.models.schemas import OrderSchema
    order_schema = OrderSchema()
    data = order_schema.dump(order_db_obj)
    return data