from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Replace 'yourpassword' with your actual PostgreSQL password
DATABASE_URL = "postgresql://postgres:Derkaderka2@localhost/wordgame_leaderboard"

# ✅ Set up the database engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)  # Added connection pooling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Define the Leaderboard Table
class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, nullable=False, index=True)  # ✅ Enforce required player name
    score = Column(Integer, nullable=False, index=True)  # ✅ Ensure score cannot be null
    date_played = Column(TIMESTAMP, server_default=func.now())  # ✅ Auto-fill timestamp on insert

# ✅ Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create all tables (run this once at startup)
Base.metadata.create_all(bind=engine)