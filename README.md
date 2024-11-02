# ExamenCosmosDB - Wagner Arizapana
Se instalo los siguientes librerias

-python-dotenv

-fastapi uvicorn azure-cosmos

-pip install pydantic[email]

* Se creó el CosmosDB en azure con el nombre **acdb-wac-examen**
* Los container se llaman *Usuarios* y *Proyectos*
* Las credenciales tomarla del CosmosDB Configuracion>Claves

## USUARIO
La creación de usuarios tienen las siguientes reglas
* email: formato de correo es decir debe tener el caracter @ y dominio
* edad: debe estar entre 1 y 130

La actualización de usuarios se debe considerar un usuario valido

La consulta de usuario es la lista completa

La eliminación se realiza por id (usuario)

## PROYECTO
La creación de proyectos tienen las siguientes reglas
* id_usuario: debe ser un usuario valido

La actualización de proyectos se debe considerar un proyecto y usuario valido, cualquiera es motivo de observación

Las consultas son de lista completa o filtrado por id de usuario

La eliminación de proyectos es por id (proyecto)
