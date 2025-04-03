from pydantic import BaseModel, Field


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)

class Hotel(BaseModel):
    title: str
    name: str

