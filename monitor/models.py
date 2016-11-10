from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Process(Base):
    __tablename__ = 'processes'
    id = Column(integer, primary_key = True)
    name = Column(Text)
    start_command = Column(Text)
    search_regex = Column(Text) 
    last_process_id = Column(Integer)
    kind = Column(Text)
    
    
