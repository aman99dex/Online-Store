from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#put your db url here
db_url = "postgresql://username:password@localhost:5432/database_name"

engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
