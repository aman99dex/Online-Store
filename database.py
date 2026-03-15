from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:@#XYxx69@localhost:5432/fast"

engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
