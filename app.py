from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import(
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title ='Live de Python')
spec.register(server)
database = TinyDB('database.json')


class Pessoa(BaseModel):
    id: Optional[int]
    nome: str
    idade: int  


class Pessoas(BaseModel):
    pessoas: list[Pessoa]
    count: int


@server.get('/pessoas') #Rota endpoint recurso
@spec.validate(
  resp=Response(HTTP_200=Pessoas)
)
def buscar_pessoas():
  """ Retorna um usuario na Base de Dados."""
  return jsonify(
    Pessoas(
        pessoas=database.all(),
        count=len(database.all())
    ).dict()
  )


@server.post('/pessoas') #Rota endpoint recurso
@spec.validate(
  body=Request(Pessoa), 
  resp=Response(HTTP_200=Pessoa)
  )
def inserir_pessoas():
  """Insere uma Pessoa no Base de Dados."""
  body = request.context.body.dict()
  database.insert(body)
  return body


# def buscar_pessoas():
#   return  'Programaticamente Falando, Victor Nascimento' 

server.run()