from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, ForeignKey, Table, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Table, Column, MetaData, Integer, Computed

# Database engine and base class
engine = create_engine('postgresql+psycopg2://postgres:students@127.0.0.1/SDK_DB')
Base = declarative_base()


# Actions Table
class Action(Base):
    __tablename__ = 'actions'
    action_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    action = Column(String(256), nullable=False)
    action_time = Column(TIMESTAMP, nullable=False, primary_key=True)


# User Table
class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    role = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    actions = relationship('Action', backref='user')
    votes = relationship('Vote', backref='vote')

# Feature Poll Table
class FeaturePoll(Base):
    __tablename__ = 'feature_poll'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    options = relationship('Option', backref='feature')
    votes = relationship('Vote', backref='vote')
    poll_results = relationship('Poll_result',backref='poll_result')

# Option Table
class Option(Base):
    __tablename__ = 'option'
    id = Column(BigInteger, primary_key=True)
    feature_id = Column(BigInteger, ForeignKey('feature_poll.id'))
    description = Column(Text, nullable=False)
    votes = relationship('Vote', backref='vote')


# Poll Result Table
class PollResult(Base):
    __tablename__ = 'poll_result'
    result_id = Column(BigInteger, primary_key=True)
    feature_id = Column(BigInteger, ForeignKey('feature_poll.id'))
    total_votes = Column(Integer)

class Vote(Base):
    __tablename__ = 'vote'
    option_id = Column(BigInteger, ForeignKey('option.id'), primary_key = True)
    feature_id = Column(BigInteger, ForeignKey('feature_poll.id'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)


