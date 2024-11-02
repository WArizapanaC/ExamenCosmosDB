from pydantic import BaseModel, Field, EmailStr

class Usuario(BaseModel):
    id: str = Field(..., example="user01")
    nombre: str = Field(..., example="Wagner Arizapana")
    email: EmailStr = Field(..., example="Wagner.Arizapana@teamsoft.com.pe")
    edad: int = Field(..., ge=1, le=130, example="35")

class Proyecto(BaseModel):
    id: str = Field(..., example="proy01")
    nombre: str = Field(..., example="Proyecto X")
    descripcion: str = Field(..., example="Evaluaciones de Cosmos DB")
    id_usuario: str = Field(..., example="user01")