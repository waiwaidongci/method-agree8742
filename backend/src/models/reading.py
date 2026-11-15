from sqlalchemy import String,ForeignKey,Float,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class PairedReading(Base):
    __tablename__="paired_readings"
    __table_args__=(UniqueConstraint("dataset_id","sample_code"),)
    id:Mapped[int]=mapped_column(primary_key=True)
    dataset_id:Mapped[int]=mapped_column(ForeignKey("pair_datasets.id"))
    sample_code:Mapped[str]=mapped_column(String(80))
    reference_value:Mapped[float]=mapped_column(Float)
    candidate_value:Mapped[float]=mapped_column(Float)
