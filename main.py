import email
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Union
from fastapi.responses import JSONResponse



app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):

    email: str
    username: str
    password: str
    confirm_password: str 

class Login(BaseModel):

    email: str
    password: str

class Cart(BaseModel):

    email: str
    food: str
    topping: str
    sauce: str
    qty: str
    total: str

@app.get("/")
def read_root():
    return "pkpos api"


@app.get("/get_food")
def get_data(type : str):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )
    mycursor = mydb.cursor()

    sql = "SELECT food_id, food_type, food_name, food_price, food_desc, food_img FROM food where food_type=%s"
    mycursor.execute(sql, (type,))
    results = mycursor.fetchall()

    
    data = []
    
    print(results)

    for result in results:
        dict = {}
        dict["food_id"] = result[0]
        dict["food_type"] = result[1]
        dict["food_name"] = result[2]
        dict["food_price"] = result[3]
        dict["food_desc"] = result[4]
        dict["food_img"] = result[5]

        data.append(dict)

    print(data)
    return data

@app.post("/signup", response_model=User)
def signup(user: User):
    print("entered signup")
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )
    mycursor = mydb.cursor()

    if user.password == user.confirm_password:
        mycursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        result = mycursor.fetchall()

        if len(result) > 0:
            return JSONResponse(content="email already exists")
        
        else:
            print("correct creditials")
            userid = uuid.uuid1()
            userid = str(userid)
            sql = "INSERT INTO users (userid, username, email, password) VALUES (%s, %s, %s, %s)"
            val = (
                userid,
                user.username,
                user.email,
                user.password,
            )
            mycursor.execute(sql, (val))

            mydb.commit()

            return JSONResponse(content="success")
        

        
    else:
        print("didnt match")
        return JSONResponse(content="password does not match")


@app.post("/login", response_model=Login)
def signup(login: Login):
    print("entered login")
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users WHERE email = %s", (login.email,))
    result = mycursor.fetchall()


    if len(result) > 0:
        if result[0][4] == login.password:
            print("success")
            return JSONResponse(content="success")
        else:
            print("wrong 1")
            return JSONResponse(content="wrong email or password")
    else:
        print("wrong 2")
        return JSONResponse(content="wrong email or password")
    
@app.post("/addtocart", response_model=Cart)
def signup(cart: Cart):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )
    mycursor = mydb.cursor()
    cart_id = uuid.uuid1()
    cart_id = str(cart_id)
    sql = "INSERT INTO cart (cart_id, email, food, topping, sauce, qty, total) VALUES (%s,%s, %s, %s, %s, %s, %s)"
    val = (
        cart_id,
        cart.email,
        cart.food,
        cart.topping,
        cart.sauce,
        cart.qty,
        cart.total
    )
    mycursor.execute(sql, val)
    mydb.commit()


    return JSONResponse(content="success")
    
    
@app.get("/get_cart")
def get_data(email : str):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM cart where email=%s"
    mycursor.execute(sql, (email,))
    results = mycursor.fetchall()

    
    data = []
    total = 0

    for result in results:
        dict = {}
        dict["cart_id"] = result[1]
        dict["email"] = result[2]
        dict["food"] = result[3]
        dict["topping"] = result[4]
        dict["sauce"] = result[5]
        dict["qty"] = result[6]
        dict["total"] = result[7]
        total = total + float(result[7])
        dict['all_total'] = total

        data.append(dict)


    print(data)
    return data

@app.delete("/remove_cart")
def remove_cart(cart_id : str):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5523367",
        password="tIrlPr9iFe",
        database="sql5523367"
    )

    mycursor = mydb.cursor()

    sql = "DELETE FROM cart WHERE cart_id = %s"

    mycursor.execute(sql, (cart_id,))

    mydb.commit()

    return JSONResponse(content="success")