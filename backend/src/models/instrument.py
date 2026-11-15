from sqlalchemy import String,Float
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class Instrument(Base):
    __tablename__="instruments"
    id:Mapped[int]=mapped_column(primary_key=True)
    code:Mapped[str]=mapped_column(String(60),unique=True)
    name:Mapped[str]=mapped_column(String(120))
    serial:Mapped[str]=mapped_column(String(100))
    unit:Mapped[str]=mapped_column(String(30),default="反射率 %")
    lower:Mapped[float]=mapped_column(Float,default=0)
    upper:Mapped[float]=mapped_column(Float,default=100)
