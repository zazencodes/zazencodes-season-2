# Example dataset: `data.csv`
# name,age,city
# Alice,30,New York
# Bob,25,Los Angeles
# Charlie,35,Chicago

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
db_url = "sqlite:///example.db"
engine = create_engine(db_url)
Base = declarative_base()

# Define the database model
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    city = Column(String(100))

def etl_pipeline():
    # Extract
    def extract():
        try:
            df = pd.read_csv('data.csv')
            return df
        except Exception as e:
            print(f"Error during extraction: {e}")
            return None

    # Transform
    def transform(df):
        if df is None:
            return None

        try:
            # Example transformations
            df = df.copy()
            # Convert names to title case
            df['name'] = df['name'].str.title()
            # Ensure age is integer
            df['age'] = df['age'].astype(int)
            # Convert city names to title case
            df['city'] = df['city'].str.title()

            return df
        except Exception as e:
            print(f"Error during transformation: {e}")
            return None

    # Load
    def load(df):
        if df is None:
            return False

        try:
            # Create tables
            Base.metadata.create_all(engine)

            # Create session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Convert DataFrame to dictionary and load into database
            for _, row in df.iterrows():
                person = Person(
                    name=row['name'],
                    age=row['age'],
                    city=row['city']
                )
                session.add(person)

            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error during loading: {e}")
            return False

    # Execute ETL pipeline
    print("Starting ETL pipeline...")
    df = extract()
    df_transformed = transform(df)
    success = load(df_transformed)

    if success:
        print("ETL pipeline completed successfully")
    else:
        print("ETL pipeline failed")
