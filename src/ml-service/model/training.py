from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from model.database import Base
from enum import Enum

class Prediction(str, Enum):
    STABLE = "STABLE"
    BAISSE = "BAISSE"
    HAUSSE = "HAUSSE"

class Training(Base):

    __tablename__ = "training_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    annee: Mapped[int] = mapped_column(nullable=False)
    code_commune: Mapped[int] = mapped_column(nullable=False)
    prix_m2: Mapped[float] = mapped_column(nullable=False)
    nom_commune: Mapped[str] = mapped_column(nullable=False)
    dep_code: Mapped[int] = mapped_column()
    dep_nom: Mapped[str] = mapped_column()
    reg_code: Mapped[int] = mapped_column()
    reg_nom: Mapped[str] = mapped_column()
    code_postal: Mapped[int] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column()
    superficie_km2: Mapped[float] = mapped_column()
    zone_emploi: Mapped[int] = mapped_column()
    taux_global_tfb: Mapped[float] = mapped_column()
    taux_global_tfnb: Mapped[float] = mapped_column()
    taux_plein_teom: Mapped[float] = mapped_column()
    taux_global_th: Mapped[float] = mapped_column()
    sales_numbers: Mapped[int] = mapped_column()
    market_prediction: Mapped[Prediction] = mapped_column(SQLEnum(Prediction, native_enum=True))