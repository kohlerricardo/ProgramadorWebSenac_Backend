from fastapi import APIRouter, Response,status,Query
from typing import Annotated
from db.db import Database
item_cardapio_routes = APIRouter(tags=['Cardápio'])
database = Database()




# @item_cardapio_routes.get("/itens")
# def item_cardapio():
    # return database.retrieve()

@item_cardapio_routes.post("/itens",status_code=status.HTTP_201_CREATED)
def cadastrar_item_cardapio(payload:dict):
    database.insert(payload['id'],payload)
    return Response(status_code=status.HTTP_201_CREATED)

@item_cardapio_routes.get('/itens')
# def itens_disponiveis(disponivel :bool = None):
def itens_disponiveis(disponivel : Annotated[
                                bool,
                                Query(description="Valor de query inválido")]):
    disponiveis = database.retrieve()
    if disponivel is None:
        return disponiveis
    retorno={}
    for item in disponiveis:
        if disponiveis[item]["disponível"] == disponivel:
            retorno[item]=disponiveis[item]
    return retorno

