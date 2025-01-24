import ckan.model as model
# from ckan.model.meta import Base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Initialize the base class for SQLAlchemy models
Base = declarative_base(metadata=model.meta.metadata) # tanpa menggunakan Base bawaan ckan.


# Define the metadata model
# class Metadata(db.Model):
class Metadata(Base):
    __tablename__ = 'ckanext_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(String, nullable=False)
    title = Column(String, nullable=True)
    desc = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, organization_id, title, desc=None, author=None, file_path=None):
        self.organization_id = organization_id
        self.title = title
        self.desc = desc
        self.author = author
        self.file_path = file_path

    def __repr__(self):
        return f"<Metadata(id={self.id}, organization_id='{self.organization_id}', title='{self.title}')>"

# Database utility functions
def get_engine(database_url):
    return create_engine(database_url)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()