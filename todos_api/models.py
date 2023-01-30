from sqlalchemy import Boolean, Column, Integer, String
from database.db import Base

class Todos(Base):
    """Model-table for Todos"""
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    