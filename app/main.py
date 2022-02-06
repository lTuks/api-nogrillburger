from unidecode import unidecode
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from fastapi import FastAPI, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from app.security import get_api_key, get_api_key_admin
from app.models import db, Burger, Other, Client, Order, Stock

noGrill = FastAPI(openapi_url=None)

noGrill.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["token"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@noGrill.get("/burger/")
async def list_burgers(api_key: APIKey = Depends(get_api_key)):
    burgers = []
    for burger in db["burger"].find():
        burgers.append(Burger(**burger))
    burgers = jsonable_encoder(burgers)
    return JSONResponse(status_code=status.HTTP_200_OK, content=burgers)


@noGrill.get("/other/")
async def list_others(api_key: APIKey = Depends(get_api_key)):
    others = []
    for other in db["other"].find():
        others.append(Other(**other))
    others = jsonable_encoder(others)
    return JSONResponse(status_code=status.HTTP_200_OK, content=others)


@noGrill.get("/client/")
async def list_clients(api_key: APIKey = Depends(get_api_key_admin)):
    clients = []
    for client in db["client"].find():
        clients.append(Client(**client))
        clients = jsonable_encoder(clients)
    return JSONResponse(status_code=status.HTTP_200_OK, content=clients)


@noGrill.get("/client/{client_name}")
async def one_clients(client_name: str, api_key: APIKey = Depends(get_api_key_admin)):
    clients = []
    client_filter = []

    for client in db["client"].find():
        clients.append(Client(**client))
    clients = jsonable_encoder(clients)
    for i in range(len(clients)):
        if client_name in unidecode(clients[i]["name"]).lower():
            client_filter.append([clients[i]])

    def flatten(t):
        return [item for sublist in t for item in sublist]

    client_filter = flatten(client_filter)
    return JSONResponse(status_code=status.HTTP_200_OK, content=client_filter)


@noGrill.post("/client/new/")
async def create_client(client: Client, api_key: APIKey = Depends(get_api_key_admin)):
    client = jsonable_encoder(client)
    new_client = db["client"].insert_one(client)
    created_client = db["client"].find_one({"_id": new_client.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_client)


@noGrill.put("/client/{id}")
async def update_client(
    id: str, client: Client, api_key: APIKey = Depends(get_api_key_admin)
):
    update_client = (
        db["client"].update_one({"_id": id}, {"$set": client.dict()}).raw_result
    )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@noGrill.get("/order/")
async def list_orders(api_key: APIKey = Depends(get_api_key_admin)):
    orders = []
    for order in db["order"].find():
        orders.append(Order(**order))
        orders = jsonable_encoder(orders)
    return JSONResponse(status_code=status.HTTP_200_OK, content=orders)


@noGrill.post("/order/new/")
async def create_order(order: Order, api_key: APIKey = Depends(get_api_key)):
    order = jsonable_encoder(order)
    new_order = db["order"].insert_one(order)
    created_order = db["order"].find_one({"_id": new_order.inserted_id})
    print(created_order["client_id"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)


@noGrill.get("/stock/")
async def list_stock(api_key: APIKey = Depends(get_api_key_admin)):
    stocks = []
    for stock in db["stock"].find():
        stocks.append(Stock(**stock))
        stock = jsonable_encoder(stock)
    return JSONResponse(status_code=status.HTTP_200_OK, content=stocks)


@noGrill.post("/stock/new/")
async def create_stock(stock: Stock, api_key: APIKey = Depends(get_api_key_admin)):
    stock = jsonable_encoder(stock)
    new_stock = db["stock"].insert_one(stock)
    created_stock = db["stock"].find_one({"_id": new_stock.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_stock)


@noGrill.put("/stock/{id}")
async def update_stock(
    id: str, stock: Stock, api_key: APIKey = Depends(get_api_key_admin)
):
    update_stock = (
        db["stock"].update_one({"_id": id}, {"$set": stock.dict()}).raw_result
    )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
