from azure.cosmos import CosmosClient, exceptions

#variables de inicio de sesión
url = ""
Key = ""
database_name = "GestorProyectosDB"
container_name_usuarios = "Usuarios"
container_name_proyectos = "Proyectos"

client = CosmosClient(url, credential=Key)

#usuarios_container = client.get_database_client(database_name).get_container_client("Usuarios")
#proyectos_container = client.get_database_client(database_name).get_container_client("Proyectos")

#Crear base de datos
try:
    database = client.create_database_if_not_exists(id=database_name)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(database_name)

#Crear contenedor Usuarios
try:
    usuarios_container = database.create_container_if_not_exists(id=container_name_usuarios, partition_key={'paths':['/id'], 'kind': 'Hash'},offer_throughput=400)
except exceptions.CosmosResourceExistsError:
    usuarios_container = database.get_container_client(container_name_usuarios)

#Crear contenedor Proyectos
try:
    proyectos_container = database.create_container_if_not_exists(id=container_name_proyectos, partition_key={'paths':['/id'], 'kind': 'Hash'},offer_throughput=400)
except exceptions.CosmosResourceExistsError:
    proyectos_container = database.get_container_client(container_name_proyectos)
