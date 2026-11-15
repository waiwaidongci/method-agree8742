from datetime import datetime
from sqlalchemy import String,ForeignKey,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class PairDataset(Base):
    __tablename__="pair_datasets"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(160),unique=True)
    reference_id:Mapped[int]=mapped_column(ForeignKey("instruments.id"))
    candidate_id:Mapped[int]=mapped_column(ForeignKey("instruments.id"))
    source_file:Mapped[str]=mapped_column(String(180))
    note:Mapped[str]=mapped_column(String(600),default="")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
