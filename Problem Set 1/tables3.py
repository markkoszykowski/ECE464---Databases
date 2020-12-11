# Mark Koszykowski
# ECE464 - Problem Set 1
# Question 3
# Table making Code

from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ps1p2', echo=True)
Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String(20))
    rating = Column(Integer)
    dob = Column(DateTime)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.rating)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String(20))
    color = Column(String(10))
    length = Column(Integer)
    cond = Column(String(20))

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

class Employee(Base):
    __tablename__ = 'employees'

    eid = Column(Integer, primary_key=True)
    ename = Column(String(20))
    position = Column(String(20))
    pay = Column(Integer)
    dob = Column(DateTime)

    def __repr__(self):
        return "<Employee(id=%s, name='%s', pay=%s)>" % (self.eid, self.ename, self.pay)

class Maintenance(Base):
    __tablename__ = 'maintains'
    __table_args__ = (PrimaryKeyConstraint('eid', 'bid', 'day'), {})

    eid = Column(Integer, ForeignKey('employees.eid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    employee = relationship('Employee')

    def __repr__(self):
        return "<Maintenance(eid=%s, bid=%s, day=%s)>" % (self.eid, self.bid, self.day)

Base.metadata.create_all(engine)