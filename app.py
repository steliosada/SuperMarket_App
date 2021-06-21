from pymongo import MongoClient, cursor
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import pymongo
import json
from bson import ObjectId
from bson.json_util import dumps
import uuid
import time
    

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSMarkets']

# Choose collections
products = db['Products']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def get_cart_items_and_total_value(cart):
    items = []
    total_value = 0
    for id, item in cart.items():
        product = products.find_one({"_id": id})
        quant = int(item["quantity"])
        item_name = product['name']
        total_value += float(product["price"]) * quant
        items.append(f" {quant} of {item_name}")
    return ' ,'.join(items), total_value

def create_session(user_email):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (user_email, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

@app.route('/')

@app.route('/createUser', methods=['POST', 'GET'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "password" in data or not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

  
    # Έλεγχος δεδομένων email / password
    if users.find({"email":data["email"]}).count() == 0 :
        new_user ={"name" : data['name'],"email" : data['email'], "password" : data['password'], "category" : 'User' }
        users.insert_one(new_user)
        return Response(data['name']+" was added to the MongoDB", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
 
    else:
        return Response("A user with the given email already exists", mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS
    
#Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # Έλεγχος δεδομένων email / password
    if users.find({"email":data["email"]}).count() == 1 :
        user1 = users.find_one({"email" : data['email'] })
        if user1['password'] == data['password'] :
            global user_email
            global user_category
            global cart
            cart = {}
            user_email = str(data['email'])
            user_category = str(user1['category'])
            global user_uuid
            user_uuid = create_session(user_email)
            return Response(f"Logged in. Your UserID is : {user_uuid}",status=200 , mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS

    # Διαφορετικά, αν η αυθεντικοποίηση είναι ανεπιτυχής.
        else:
            return Response("Wrong email or password.", status=400 , mimetype='application/json') # ΠΡΟΣΘΗΚΗ STATUS

#Διαγραφη χρηση
@app.route('/deleteUser', methods=['POST','GET'])
def deleteUser():
    global user_email
    users.delete_one({"email": user_email})
    return Response("Your account has been deleted.",status=200 , mimetype='application/json') 

#Εισαγωγη αντικειμενου στο καταστημα.
@app.route('/insertItem', methods=['POST','GET'])
def insertItem():
    global user_category
    
    #Ελεγχος Χρηστη
    if user_category == "User" :
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "admin" :
        
        #ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "name" in data or not "price" in data or not "description" in data or not "category" in data or not "stock" in data :
            return Response("Information incomplete",status=500,mimetype="application/json")
        
        #Εισαγωγη Δεδομενων
        product ={'name':data["name"], 'price':data["price"], 'description':data["description"], 'category':data["category"], 'stock':data["stock"]}
        products.insert_one(product)
        return Response("item added to the store.",status=201 , mimetype='application/json')

#Διαγραφη αντικειμενου απο το καταστημα.
@app.route('/DeleteItem', methods=['POST','GET'])
def DeleteItem():

    # Ελεγχος Χρηστη
    global user_category
    if user_category == "User" :
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "admin" :

  # ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "id" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        # Διαγραφη αντικειμενου
        id = ObjectId(data["id"])
        products.delete_one({'_id':id })
        return Response("item deleted.",status=200 , mimetype='application/json')

#Ενημερωση αντικειμενου στο καταστημα.
@app.route('/UpdateItem', methods=['POST','GET'])
def UpdateItem():

    # Ελεγχος Χρηστη
    global user_category
    if user_category == "User" :
        return Response("Persmission Denied",status=401,mimetype="application/json")
    elif user_category == "admin" :

  # ελεγχος Δεδομενων
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "id" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        #Ενημερωση αντικειμενου
        id = ObjectId(data["id"])
        if "name" in data:
            products.update({"_id":id},{"$set":{'name':data["name"]}})

        if "price" in data :
            products.update({"_id":id},{"$set":{"price":data['price']}})    

        if "description" in data:
            products.update({"_id":id},{"$set":{"description":data['description']}})
    
        if "stock" in data :
            products.update({"_id":id},{"$set":{"stock":data['stock']}}) 

        return Response("item updated.",status=200 , mimetype='application/json')

#Αναζητηση αντικειμενου.
@app.route('/search', methods=['POST',' GET'])
def search():

    # Ελεγχος Χρηστη
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
    

    # ελεγχος Δεδομενων
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name"  in data and not "category" in data and not "id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else:
        if "name" in data:
            product = products.find({"name":data['name']}).sort("name", pymongo.ASCENDING) #de douleuei to sort
        if  "category" in data:
            product = list(products.find({"category":data['category']}))
        

            if "id" in data:
                id = ObjectId(data["id"])
                product = products.find_one({"_id":id})
        
        if product != None: 
            return Response(dumps(product), status=200, mimetype='application/json')
        else:
            return Response('No item found',status=500,mimetype='application/json')    

#Εισαγωγη του προιοντος στο καλαθι.
@app.route('/addItem',methods=['POST','GET' ])
def addItem():
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "id" in data or not "quantity" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else:
        id = ObjectId(data["id"])
        product = products.find_one({"_id":id})
        if product == None : 
            return Response("No item found.",status=500,mimetype="application/json")
        else : 
            stock = int(product['stock'])
            
            want = int(data['quantity'])
            
            stock_to_quantity = stock - want

            if stock_to_quantity < 0 :
                return Response(f"Not enough stock currently available only : {stock} ",  status=500,mimetype="application/json")
            else : 
                products.update({"_id":id},{"$set":{'stock':stock_to_quantity}})
                global user_email
                global cart
                a = id
                cart[a] = {"quantity" : data['quantity']}   
                item = f"{want}x {product['name']}"
                cart_items, total_value = get_cart_items_and_total_value(cart)
                return Response(f"Item added to cart: {item}.\n Items in cart: {cart_items}. \n Total value: {str(total_value)}" ,status=200, mimetype='application/json')


#Εμφανιση καλαθιου
@app.route('/showCart',methods=['GET'])
def showCart():
    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else:
        global user_category
        if user_category == "admin" :
            return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
        global user_email
        global cart
        if cart == None :
            return Response("Your cart is empty" ,status=500,mimetype="application/json")
        else :
            cart_items, total_value = get_cart_items_and_total_value(cart)
            return Response(f"Items in cart: {cart_items}. \n Total value: {str(total_value)}",  status=200 , mimetype='application/json')

#Διαγραφη αντικειμενου απο το καλαθι
@app.route('/deleteFromCart',methods=['POST','GET'])
def deleteFromCart():                
    
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=500,mimetype="application/json")
    
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "id" in data :
        return Response("Information incomplete",status=500,mimetype="application/json")

    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else:
        global cart 
        id = ObjectId(data["id"])
    
        try:
            delete = {}
            delete = cart[id]
            del cart[id]
            quantity = int(delete['quantity'])
            product = products.find_one({"_id":id})
            stock = int(product['stock'])
            stock_to_quantity = stock + quantity
            products.update({"_id":id},{"$set":{'stock':stock_to_quantity}})
        except KeyError as ex:
            return Response(f"No item with this id {id} was found",status=500,mimetype="application/json")      
        cart_items, total_value = get_cart_items_and_total_value(cart)
        return Response(f"Item deleted from cart. \n Items in cart: {cart_items}. \n Total value: {str(total_value)}",  status=200 , mimetype='application/json')

#Αγορα Αντικειμενων
@app.route('/Purchase',methods=['POST','GET'])
def Purchase():      
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=500,mimetype="application/json")
    
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "card" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else:
        global cart
        if len(cart) == 0:
            return Response("Theres nothing to buy inside your cart, please add items.",status=500,mimetype="application/json")

        card =  str(data["card"])
        if len(card) != 16 :
            return Response("Card number not valid.",status=500,mimetype="application/json")
        else:
            global user_email
            user = users.find_one({"email" : user_email})
            cart_items, total_value = get_cart_items_and_total_value(cart)
            order = {"Items" : cart_items , "Cost" : total_value}
            if 'Order History' not in user:
                order_History = {}
                order_History['1'] = order
                users.update({"email" : user['email']},{"$set": {'Order History': order_History}})
            else: 
                order_History = dict(user['Order History'])
                for key , value in order_History.items():
                    order_History[key] = value
                    last_key = int(key)
                    last_key = last_key +1
                    
                key = str(last_key)
                order_History[key] = order
                
                
            users.update({"email" : user['email']},{"$set": {'Order History': order_History}})
            cart = {}
            return Response(f"Items purchased: {cart_items}. \n Total Cost: {str(total_value)}", status=200 , mimetype='application/json')

#Ιστορικο παραγγελιων
@app.route('/orderHistory',methods=['GET'])
def orderHistory():
    global user_uuid
    uuid = user_uuid
    if is_session_valid(uuid)== False :
        return Response("Information incomplete",status=401,mimetype="application/json")
    else: 
        global user_category
        if user_category == "admin" :
            return Response("Admins Cannot access this menu",status=500,mimetype="application/json")
        global user_email
        user1 = users.find_one({"email" : user_email})
        if "Order History" not in user1 :
            return Response("No orders on your order history.",status=404,mimetype="application/json")
        else:
            orderHistory = user1["Order History"]
            return Response(f"Order History: \n {orderHistory}", status=200 , mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
