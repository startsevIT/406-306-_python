from datetime import time
from uuid import UUID, uuid4
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

 
class BusShedule(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    stop_complex: str
    date_time: time
    bus_number: str


class BusSheduleUpdateDTO(BaseModel):
    stop_complex: str | None = None
    date_time: time | None = None
    bus_number: str | None = None
 

class BusSheduleRepository:
    _shedules : list[BusShedule]
    
    def __init__(self):
        self._shedules = [
            BusShedule(id=uuid4(),stop_complex="123",date_time=time(15,00,00),bus_number="45")
        ]
    
    def create(self, shedule : BusShedule) -> None:
         self._shedules.append(shedule)
         
    def read(self) -> list[BusShedule]:
         return self._shedules
     
    def update(self, id : UUID,
               stop_complex : str | None,
               date_time : time | None,
               bus_number : str | None) -> None:
        items = [x for x in self._shedules if x.id == id]
        if (items == []):
            raise Exception("Нет такого")
        item = items[0]
        if(stop_complex != None):
            item.stop_complex = stop_complex
        if (date_time != None):
            item.date_time = date_time
        if(bus_number != None):
            item.bus_number = bus_number
 
    def delete(self, id : UUID) -> None:
        items = [x for x in self._shedules if x.id == id]
        if (items == []):
            raise Exception("Нет такого")
        item = items[0]
        self._shedules.remove(item)


app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Разрешает запросы из любого источника
    allow_credentials=True,         # Разрешает передачу куки/авторизации
    allow_methods=["*"],          # Разрешает все HTTP‑методы (GET, POST и др.)
    allow_headers=["*"],          # Разрешает все заголовки
)
 
repo : BusSheduleRepository = BusSheduleRepository()

@app.get("/shedule")
def get_shedule():
    return repo.read()

@app.post("/shedule")
def post_shedule(shedule : BusShedule = Body()):
    repo.create(shedule)

@app.put("/shedule/{id}")
def put_shedule(id : UUID, dto : BusSheduleUpdateDTO = Body()):
    repo.update(id, dto.stop_complex, dto.date_time, dto.bus_number)

@app.delete("/shedule/{id}")
def delete_shedule(id : UUID):
    repo.delete(id)

uvicorn.run(app) 