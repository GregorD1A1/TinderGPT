from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
import os


# Create a connection to the SQLite database
abs_script_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_script_path)
engine = create_engine(f'sqlite:///{dir_name}/rules_db.sqlite')

metadata = MetaData()


pickup_rules = Table(f'pickup_rules', metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)


# Function to query rule by tag
def query_rule(tag_name):
    with Session() as session:
        rule = session.query(pickup_rules).filter_by(tag=tag_name).first()
        rule = str(rule)

        return rule
