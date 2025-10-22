from pydantic import Pydantic 

class Cliente(BaseModel):
id: int
	nombre: str
	email: str
	telefone: str
	direccion: str


	class crearcliente(Cliente):
			pass



