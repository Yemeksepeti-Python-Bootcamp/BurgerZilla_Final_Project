# Burgerzilla

Burgerzilla REST microservice provides order communication between customers and restaurants.<br /> 
Restaurant owners can add, update and delete products.They can also manage their orders. <br />
In addition, users can access and order the products of the restaurant. They can update and cancel their orders. <br />

# Libs & Modules & Framework
Flask </br>
Flask-RESTX (community driven fork of Flask-RESTPlus) </br>
Flask-SQLAlchemy </br>
psycopg2-binary </br>

## Burgerzilla File Structure 
```
burgerzilla
├─ .gitignore
├─ app
│  ├─ api
│  │  ├─ restaurant
│  │  │  ├─ controller.py
│  │  │  ├─ dto.py
│  │  │  ├─ service.py
│  │  │  ├─ utils.py
│  │  │  └─ __init__.py
│  │  ├─ user
│  │  │  ├─ controller.py
│  │  │  ├─ dto.py
│  │  │  ├─ service.py
│  │  │  ├─ utils.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  ├─ auth
│  │  ├─ controller.py
│  │  ├─ dto.py
│  │  ├─ service.py
│  │  ├─ utils.py
│  │  └─ __init__.py
│  ├─ extensions.py
│  ├─ models
│  │  ├─ order.py
│  │  ├─ product.py
│  │  ├─ restaurant.py
│  │  ├─ schemas.py
│  │  ├─ user.py
│  │  ├─ usertype.py
│  │  └─ __init__.py
│  ├─ utils.py
│  └─ __init__.py
├─ boot.sh
├─ config.py
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
├─ run.py
└─ tests
   ├─ test_auth_api.py
   ├─ test_config.py
   ├─ test_restaurant_api.py
   ├─ test_restaurant_model.py
   ├─ test_user_api.py
   ├─ test_user_model.py
   ├─ utils
   │  ├─ base.py
   │  ├─ common.py
   │  └─ __init__.py
   └─ __init__.py
```

## Run the app
To run the application, these 2 docker commands should be used.

    docker build -t burgerzilla:latest .
    docker compose up --build web
    
boot.sh includes a script which can put some initial data to our database.

After these two commands, application will be running on <strong>localhost:80</strong>

# AUTH ENDPOINTS

Register and Login endpoints is inside 'auth' namespace.

## Register


#### Request to: <strong> 127.0.0.1:5000/auth/register </strong>
#### Request Type: POST



```json
{
    "email":"ilhanmert@alan.com",
    "username":"ilhanmert",
    "name":"ilhan m alan",
    "password":"123",
    "usertype_id":1
}
```
usertype_id=1 if you are Restaurant Owner, </br>
usertype_id=0 if you are Customer </br>
Here, user_type is optional parameter and if not given it's default 0

### Response
```json
{
    "status": "True",
    "message": "Kayıt başarılı",
    "access_token": "eyJ0eX.....JnE",
    "user": {
        "id": 5,
        "email": "ilhanmert@alan.com",
        "usertype_id": 1,
        "name": "ilhan m alan",
        "username": "ilhanmert"
    }
}
```
## Login


#### Request to: <strong> 127.0.0.1:5000/auth/login </strong>
#### Request Type: POST



```json
{
    "email":"ilhanmert@alan.com",
    "password":"123"
}
```
email and password is <strong>required</strong>

### Response
```json
{
    "status": "True",
    "message": "Giriş başarılı",
    "access_token": "eyJ0eX.....JnE",
    "user": {
        "id": 5,
        "email": "ilhanmert@alan.com",
        "usertype_id": 1,
        "name": "ilhan m alan",
        "username": "ilhanmert"
    }
}
```

# USER ENDPOINTS

User(Customer) endpoints is inside 'api/user' namespace.

## Get All Orders of a User

#### Request Type: GET
#### Request to: <strong> 127.0.0.1:5000/api/user/orders </strong>

Response will be the all orders given by the authorized user.

### Response
```json
{
    "status": true,
    "message": "Orders loaded successfully",
    "orders": [
        {
            "product_id": 1,
            "orderdate": "2022-02-13T15:44:37.730014",
            "quantity": 1,
            "orderstatus": "CANCELLED",
            "restaurant_id": 2,
            "userid": 5,
            "id": 1,
            "address": "Kaer Morhen Sokak 15/3"
        },
        {
            "product_id": 2,
            "orderdate": "2022-02-13T16:05:28.180374",
            "quantity": 3,
            "orderstatus": "NEW",
            "restaurant_id": 2,
            "userid": 5,
            "id": 3,
            "address": "büyükdere mahallesi düzgün sokak 15/5"
        }
    ]
}
```
## Get Order by ID

#### Request Type: GET
#### Request to: <strong> 127.0.0.1:5000/api/user/orders/<order_id:int> </strong>

Response will be the specific order given by the authorized user.

### Response
```json
{
    "status": true,
    "message": "Order loaded successfully",
    "order": {
        "product_id": 1,
        "orderdate": "2022-02-13T15:44:37.730014",
        "quantity": 1,
        "orderstatus": "CANCELLED",
        "restaurant_id": 2,
        "userid": 5,
        "id": 1,
        "address": "Kaer Morhen Sokak 15/3"
    }
}
```


## Create Order


#### Request to: <strong> 127.0.0.1:5000/api/user/orders </strong>
#### Request Type: POST



```json
        {
            "restaurant_id": 2,
            "product_id": 1,
            "quantity":2,
            "address":"büyükdere mahallesi düzgün sokak 15/5"
        }
```


### Response
```json
{
    "status": true,
    "message": "Order created successfully",
    "order": {
        "restaurant_id": 2,
        "id": 1,
        "userid": 5,
        "quantity": 2,
        "orderdate": "2022-02-13T15:44:37.730014",
        "address": "büyükdere mahallesi düzgün sokak 15/5",
        "orderstatus": "NEW",
        "product_id": 1
    }
}
```
## Update Order


#### Request to: <strong> 127.0.0.1:5000/api/user/orders/<order_id:int> </strong>
#### Request Type: PUT



```json
{
    "quantity":"1",
    "product_id":"1",
    "address":"Kaer Morhen Sokak 15/3"
}
```

To update, you can change quantity, address or product that you ordered IF the order_status is still 'NEW'

### Response
```json
{
    "status": true,
    "message": "Order updated successfully",
    "order": {
        "restaurant_id": 2,
        "id": 1,
        "userid": 5,
        "quantity": 1,
        "orderdate": "2022-02-13T15:44:37.730014",
        "address": "Kaer Morhen Sokak 15/3",
        "orderstatus": "NEW",
        "product_id": 1
    }
}
```

## Cancel Order


#### Request to: <strong> 127.0.0.1:5000/api/user/orders/cancel/<order_id:int> </strong>
#### Request Type: PUT

Don't need a send body for the cancel request.

Make put request the given url with order_id

### Response
```json
{
    "status": true,
    "message": "Order cancelled successfully",
    "order": {
        "product_id": 1,
        "orderdate": "2022-02-13T15:44:37.730014",
        "quantity": 1,
        "orderstatus": "CANCELLED",
        "restaurant_id": 2,
        "userid": 5,
        "id": 1,
        "address": "Kaer Morhen Sokak 15/3"
    }
}
```

# RESTAURANT ENDPOINTS

Restaurant endpoints is inside 'api/restaurant' namespace.

## Get All Products of a Restaurant

#### Request Type: GET
#### Request to: <strong> 127.0.0.1:5000/api/restaurant/<restaurant id:int>/products </strong>

   Response will be the all products of the restaurant. </br>
   Since it is the menu of the specified restaurant, token is not needed.

### Response
```json
{
    "status": true,
    "message": "Orders loaded successfully",
    "orders": [
        {
            "product_id": 1,
            "orderdate": "2022-02-13T15:44:37.730014",
            "quantity": 1,
            "orderstatus": "CANCELLED",
            "restaurant_id": 2,
            "userid": 5,
            "id": 1,
            "address": "Kaer Morhen Sokak 15/3"
        },
        {
            "product_id": 2,
            "orderdate": "2022-02-13T16:05:28.180374",
            "quantity": 3,
            "orderstatus": "NEW",
            "restaurant_id": 2,
            "userid": 5,
            "id": 3,
            "address": "büyükdere mahallesi düzgün sokak 15/5"
        }
    ]
}
```

