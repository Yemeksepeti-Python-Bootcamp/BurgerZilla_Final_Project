def load_data(user_db_obj):

    from app.models.schemas import UserSchema #BURASI from app.api.user.dto olabilir

    user_schema = UserSchema()
    data = user_schema.dump(user_db_obj)
    return data
    