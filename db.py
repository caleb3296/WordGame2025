import os
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Validate database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ ERROR: DATABASE_URL not set! Ensure your .env file or Render environment variables are correctly configured.")

# ✅ Set up the database engine with connection pooling
try:
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
except Exception as e:
    raise RuntimeError(f"❌ ERROR: Unable to connect to database. Details: {e}")

# ✅ Create session factory
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
    """Provide a database session, ensuring it's safely closed after use."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()  # ✅ Prevent potential session corruption
        raise e
    finally:
        db.close()

# ✅ Create all tables (run this once at startup)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables successfully created!")
except Exception as e:
    raise RuntimeError(f"❌ ERROR: Failed to create database tables. Details: {e}")