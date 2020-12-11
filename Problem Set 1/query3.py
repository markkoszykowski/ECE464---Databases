# Mark Koszykowski
# ECE464 - Problem Set 1
# Question 3
# Querying and Testing Code

import pytest
from tables3 import Base, Sailor, Boat, Reservation, Employee, Maintenance
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ps1p2', echo=True)
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

# New test for how many times each boat has been maintained (excluding ones that have not been maintained)
def test6():
    raw_query = "SELECT B.bid, B.bname, COUNT(*) as '# of maintenances' FROM boats B, maintains M WHERE B.bid = M.bid GROUP BY B.bid ORDER BY B.bid;"
    q = session.query(Boat.bid, Boat.bname, func.count('*')).filter(Boat.bid == Maintenance.bid).group_by(Boat.bid).order_by(Boat.bid)
    assert check(raw_query, q)

# New test for which employees maintained boats with a broken sail
def test7():
    raw_query = "SELECT E.eid, E.ename FROM employees E WHERE E.eid IN (SELECT M.eid FROM maintains M, boats B WHERE B.bid = M.bid AND B.cond = 'broken sail');"
    subq = session.query(Maintenance.eid).filter(Maintenance.bid == Boat.bid).filter(Boat.cond == 'broken sail').subquery()
    q = session.query(Employee.eid, Employee.ename).filter(Employee.eid.in_(subq))
    assert check(raw_query, q)

# Ran code with "pytest query2.py" to ensure queries worked

test1()
test5()
test6()
test7()