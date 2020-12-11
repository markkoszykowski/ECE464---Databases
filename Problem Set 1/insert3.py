# Mark Koszykowski
# ECE464 - Problem Set 1
# Question 3
# Inserting Code

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables3 import Base, Sailor, Boat, Reservation, Employee, Maintenance

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ps1p2', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

sailors = [
	(22, "dusting", 7, datetime.datetime(1975, 10, 10)),
	(23, "emilio", 7, datetime.datetime(1975, 10, 10)),
	(24, "scruntus", 1, datetime.datetime(1987, 10, 10)),
	(29, "brutus", 1, datetime.datetime(1987, 10, 10)),
	(31, "lubber", 8, datetime.datetime(1965, 4, 10)),
	(32, "andy", 8, datetime.datetime(1995, 4, 10)),
	(35, "figaro", 8, datetime.datetime(1965, 4, 10)),
	(58, "rusty", 10, datetime.datetime(1985, 10, 10)),
	(59, "stum", 8, datetime.datetime(1965, 4, 10)),
	(60, "jit", 10, datetime.datetime(1985, 10, 10)),
	(61, "ossola", 7, datetime.datetime(2004, 10, 10)),
	(62, "shaun", 10, datetime.datetime(1985, 10, 10)),
	(64, "horatio", 7, datetime.datetime(2004, 10, 10)),
	(71, "zorba", 10, datetime.datetime(1985, 10, 10)),
	(74, "horatio", 9, datetime.datetime(1995, 4, 10)),
	(85, "art", 3, datetime.datetime(1995, 4, 10)),
	(88, "kevin", 3, datetime.datetime(1995, 4, 10)),
	(89, "will", 3, datetime.datetime(1995, 4, 10)),
	(90, "josh", 3, datetime.datetime(1995, 4, 10)),
	(95, "bob", 3, datetime.datetime(1957, 4, 10)),
]

boats = [
	(101, "Interlake", "blue", 45, 'like new'),
	(102, "Interlake", "red", 45, 'okay'),
	(103, "Clipper", "green", 40, 'good'),
	(104, "Clipper", "red", 40, 'broken sail'),
	(105, "Marine", "red", 35, 'like new'),
	(106, "Marine", "green", 35, 'good'),
	(107, "Marine", "blue", 35, 'broken sail'),
	(108, "Driftwood", "red", 35, 'like new'),
	(109, "Driftwood", "blue", 35, 'good'),
	(110, "Klapser", "red", 30, 'good'),
	(111, "Sooney", "green", 28, 'like new'),
	(112, "Sooney", "red", 28, 'like new'),
]

reserves = [
	(22, 101, datetime.datetime(1998, 10, 10)),
	(22, 102, datetime.datetime(1998, 10, 10)),
	(22, 103, datetime.datetime(1998, 8, 10)),
	(22, 104, datetime.datetime(1998, 7, 10)),
	(23, 104, datetime.datetime(1998, 10, 10)),
	(23, 105, datetime.datetime(1998, 11, 10)),
	(24, 104, datetime.datetime(1998, 10, 10)),
	(31, 102, datetime.datetime(1998, 11, 10)),
	(31, 103, datetime.datetime(1998, 11, 6)),
	(31, 104, datetime.datetime(1998, 11, 12)),
	(35, 104, datetime.datetime(1998, 8, 10)),
	(35, 105, datetime.datetime(1998, 11, 6)),
	(59, 105, datetime.datetime(1998, 7, 10)),
	(59, 106, datetime.datetime(1998, 11, 12)),
	(59, 109, datetime.datetime(1998, 11, 10)),
	(60, 106, datetime.datetime(1998, 9, 5)),
	(60, 106, datetime.datetime(1998, 9, 8)),
	(60, 109, datetime.datetime(1998, 7, 10)),
	(61, 112, datetime.datetime(1998, 9, 8)),
	(62, 110, datetime.datetime(1998, 11, 6)),
	(64, 101, datetime.datetime(1998, 9, 5)),
	(64, 102, datetime.datetime(1998, 9, 8)),
	(74, 103, datetime.datetime(1998, 9, 8)),
	(88, 107, datetime.datetime(1998, 9, 8)),
	(88, 110, datetime.datetime(1998, 9, 5)),
	(88, 110, datetime.datetime(1998, 11, 12)),
	(88, 111, datetime.datetime(1998, 9, 8)),
	(89, 108, datetime.datetime(1998, 10, 10)),
	(89, 109, datetime.datetime(1998, 8, 10)),
	(90, 109, datetime.datetime(1998, 10, 10)),
]

employees = [
    (75, "Bob", "Repairer", 30, datetime.datetime(1985, 4, 10)),
    (76, "Eugene", "Repairer", 35, datetime.datetime(1995, 10, 10)),
    (78, "Mark", "Cleaner", 20, datetime.datetime(2000, 10, 10)),
    (79, "Sara", "Reparier", 25, datetime.datetime(2000, 4, 10)),
    (80, "John", "Cleaner", 35, datetime.datetime(1995, 4, 10)),
    (82, "Chris", "Checker", 33, datetime.datetime(1985, 10, 10)),
    (83, "Alexa", "Checker", 35, datetime.datetime(1965, 4, 10))
]

maintains = [
    (76, 102, datetime.datetime(1998, 10, 10)),
    (78, 101, datetime.datetime(1998, 9, 10)),
    (83, 112, datetime.datetime(1998, 11, 10)),
    (79, 106, datetime.datetime(1998, 12, 10)),
    (80, 104, datetime.datetime(1999, 1, 10)),
    (75, 103, datetime.datetime(1999, 2, 10)),
    (80, 105, datetime.datetime(1999, 4, 10)),
    (78, 111, datetime.datetime(1999, 8, 10)),
    (83, 105, datetime.datetime(1999, 5, 10)),
    (79, 103, datetime.datetime(1999, 7, 10))
]

for s in sailors:
	sailor = Sailor(sid=s[0], sname=s[1], rating=s[2], dob=s[3])
	session.add(sailor)

for b in boats:
	boat = Boat(bid=b[0], bname=b[1], color=b[2], length=b[3], cond=b[4])
	session.add(boat)

for r in reserves:
	reserve = Reservation(sid=r[0], bid=r[1], day=r[2])
	session.add(reserve)

for e in employees:
	employee = Employee(eid=e[0], ename=e[1], position=e[2], pay=e[3], dob=e[4])
	session.add(employee)

for m in maintains:
	maintain = Maintenance(eid=m[0], bid=m[1], day=m[2])
	session.add(maintain)

session.commit()