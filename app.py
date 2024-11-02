from fastapi import FastAPI, HTTPException
from models import Usuario, Proyecto
from database import usuarios_container, proyectos_container
from azure.cosmos import exceptions
from typing import List

app = FastAPI(title='API Examen - Usuarios y Proyectos')

#Crear usuarios
@app.post("/usuarios/",status_code=201,response_model=Usuario)
def Crear_Usuario(usuario: Usuario):
    try:
        usuarios_container.create_item(body=usuario.dict())
        return usuario
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=409, detail="Usuario ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Lista usuarios
@app.get("/usuarios/",response_model=List[Usuario])
def Listar_Usuarios():
    try:
        script = f"SELECT * FROM c"
        items = list(usuarios_container.query_items(query=script, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Actualiza usuario por id
@app.put("/usuarios/{id}",response_model=Usuario)
def Actualizar_Usuario(update_usuario: Usuario):
    try:
        existing_usuario = usuarios_container.read_item(item = update_usuario.id, partition_key = update_usuario.id)
        existing_usuario.update(update_usuario.dict(exclude_unset=True))
        usuarios_container.replace_item(item=update_usuario.id, body=existing_usuario)
        return existing_usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#Eliminar usuario por id
@app.delete("/usuarios/{id}",status_code=204)
def Eliminar_Usuario(id: str):
    try:
        usuarios_container.delete_item(item=id, partition_key=id)
        return "Usuario eliminado exitosamente"
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#Crear proyectos

@app.post("/proyectos/",status_code=201,response_model=Proyecto)
def Crear_Proyecto(proyecto: Proyecto):
    try:
    #Verifica si el usuario existe
        usuario = usuarios_container.read_item(item=proyecto.id_usuario, partition_key=proyecto.id_usuario)
        proyectos_container.create_item(body=proyecto.dict())
        return proyecto
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=409, detail="Proyecto ya existe")
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Lista proyectos
@app.get("/proyectos/",response_model=List[Proyecto])
def Listar_Proyectos():
    try:
        script = f"SELECT * FROM c"
        items = list(proyectos_container.query_items(query=script, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Lista proyectos por id de usuario

@app.get("/proyectos/{id_usuario}",response_model=List[Proyecto])
def Listar_Proyectos(id_usuario: str):
    try:
        script = f"SELECT * FROM c WHERE c.id_usuario = '{id_usuario}'"
        items = list(proyectos_container.query_items(query=script, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Actualiza proyecto por id
@app.put("/proyectos/{id}",response_model=Proyecto)
def Actualizar_Proyecto(update_proyecto: Proyecto):
    try:
        usuario = usuarios_container.read_item(item=update_proyecto.id_usuario, partition_key=update_proyecto.id_usuario)
        existing_proyecto = proyectos_container.read_item(item = update_proyecto.id, partition_key = update_proyecto.id)
        existing_proyecto.update(update_proyecto.dict(exclude_unset=True))
        proyectos_container.replace_item(item=update_proyecto.id, body=existing_proyecto)
        return existing_proyecto
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto/Usuario no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#Eliminar proyecto por id
@app.delete("/proyectos/{id}",status_code=204)
def Eliminar_Proyecto(id: str):
    try:
        proyectos_container.delete_item(item=id, partition_key=id)
        return "Proyecto eliminado exitosamente"
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))