from sqlalchemy.orm import declarative_base
import sqlparse
from sqlmodel import SQLModel, create_engine, text
from sqlalchemy.orm import sessionmaker

rootpasswd = 'templekiller' # mine is this but you can change it.
# actually i know to use .env but i am so lazy for that.
# you can do that with interactive password input /w
# from getpass import getpass
# rootpasswd = getpass()
DATABASE_URL = f"postgresql://root:{rootpasswd}@localhost/bank"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_database_and_tables():
    SQLModel.metadata.create_all(engine)

def import_sql_file():
    with open('./scripts/data.sql/') as file:
        sql_raw_text = file.read()

    sql_queries = sqlparse.split(
        sqlparse.format(sql_raw_text, strip_comments =True)
    )

    with engine.connect() as conn:
        for query in sql_queries:
            result = conn.execute(text(query))
            print(f"{result.rowcount} rows has been updated/selected.")

def make_url():
    from getpass import getpass
    rootpasswd = getpass("Root password: ")
    DATABASE_URL = f"postgresql://root:{rootpasswd}@/localhost/bank"

if __name__ == '__main__':
    make_url()
    import_sql_file()
