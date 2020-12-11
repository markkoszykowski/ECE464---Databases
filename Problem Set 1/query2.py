# Mark Koszykowski
# ECE464 - Problem Set 1
# Question 2
# Querying and Testing Code

import pytest
from tables2 import Base, Sailor, Boat, Reservation
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, aliased

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ps1', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def check(mysql_query, orm_table):
    mysql_list = []
    orm_list = []
    with engine.connect() as connection:
        mysql_table = connection.execute(mysql_query)
        for row in mysql_table:
            mysql_list.append(row)
    for row in orm_table:
        orm_list.append(row)

    return orm_list == mysql_list

def test1():
    raw_query = "SELECT B.bid, B.bname, COUNT(*) as '# of Reserves' FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY B.bid ORDER BY B.bid;"
    q = session.query(Boat.bid, Boat.bname, func.count('*').label('# of Reserves')).filter(Boat.bid == Reservation.bid).group_by(Boat.bid).order_by(Boat.bid)
    assert check(raw_query, q)

def test5():
    raw_query = "SELECT S.sid, S.sname FROM sailors S WHERE S.sid NOT IN (SELECT R.sid FROM reserves R, boats B WHERE R.bid = B.bid AND B.color = 'red');"
    subq = session.query(Reservation.sid).filter(Reservation.bid == Boat.bid).filter(Boat.color == "red").subquery()
    q = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(subq))
    assert check(raw_query, q)

def test6():
    raw_query = "SELECT AVG(S.age) FROM sailors S WHERE s.rating = 10;"
    q = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10)
    assert check(raw_query, q)

def test7():
    raw_query = "SELECT S1.sid, S1.sname, S1.age, S1.rating FROM sailors S1 HAVING age <= ALL(SELECT age FROM sailors S2 WHERE S1.rating = S2.rating) ORDER BY S1.rating;"
    sailorAlias = aliased(Sailor)
    q = session.query(Sailor.sid, Sailor.sname, Sailor.age, Sailor.rating).having(Sailor.age <= session.query(func.min(sailorAlias.age)).filter(sailorAlias.rating == Sailor.rating)).order_by(Sailor.rating)
    assert check(raw_query, q)

# Ran code with "pytest query2.py" to ensure queries worked

test1()
test5()
test6()
test7()