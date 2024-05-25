from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base


BASE = declarative_base()

class Model_Prediction(BASE):
    __tablename__ = 'model_predict'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gdp_per_capita = Column(Float, nullable=False)
    social_support = Column(Float, nullable=False)
    health_life_expectancy = Column(Float, nullable=False)
    freedom = Column(Float, nullable=False)
    generosity = Column(Float, nullable=False)
    perceptions_of_corruption = Column(Float, nullable=False)
    africa = Column(Float, nullable=False)
    asia = Column(Float, nullable=False)
    europe = Column(Float, nullable=False)
    north_america = Column(Float, nullable=False)
    oceania = Column(Float, nullable=False)
    south_america = Column(Float, nullable=False)
    happiness_score = Column(Float, nullable=False)
    prediction_happiness_score = Column(Float, nullable=False)