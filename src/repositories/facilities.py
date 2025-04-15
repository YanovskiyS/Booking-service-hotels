from pydantic import BaseModel
from sqlalchemy import update, delete, select

from src.models.facilities import FacilitiesOrm
from src.models.rooms import RoomsOrm

from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility