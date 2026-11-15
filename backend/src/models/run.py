from datetime import datetime
from sqlalchemy import String,ForeignKey,Float,JSON,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ComparisonRun(Base):
    __tablename__="comparison_runs"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(160),unique=True)
    dataset_id:Mapped[int]=mapped_column(ForeignKey("pair_datasets.id"))
    lambda_ratio:Mapped[float]=mapped_column(Float)
    allowance:Mapped[float]=mapped_column(Float)
    range_low:Mapped[float]=mapped_column(Float)
    range_high:Mapped[float]=mapped_column(Float)
    bootstrap_count:Mapped[int]=mapped_column(default=500)
    status:Mapped[str]=mapped_column(String(20),default="queued")
    error:Mapped[str]=mapped_column(String(600),default="")
    result:Mapped[dict]=mapped_column(JSON,default=dict)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
