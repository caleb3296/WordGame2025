from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Replace 'yourpassword' with your actual PostgreSQL password
DATABASE_URL = "postgresql://postgres:yourpassword@localhost/wordgame_leaderboard"

# ✅ Set up the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Define the Leaderboard Table
class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    score = Column(Integer, index=True)
    date_played = Column(TIMESTAMP)

# ✅ Create all tables (run this once at startup)
Base.metadata.create_all(bind=engine)