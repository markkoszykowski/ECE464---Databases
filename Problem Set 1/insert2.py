# Mark Koszykowski
# ECE464 - Problem Set 1
# Question 2
# Inserting Code

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables2 import Base, Sailor, Boat, Reservation

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ps1', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

sailors = [
	(22, "dusting", 7, 45.0),
	(23, "emilio", 7, 45.0),
	(24, "scruntus", 1, 33.0),
	(29, "brutus", 1, 33.0),
	(31, "lubber", 8, 55.5),
	(32, "andy", 8, 25.5),
	(35, "figaro", 8, 55.5),
	(58, "rusty", 10, 35),
	(59, "stum", 8, 25.5),
	(60, "jit", 10, 35),
	(61, "ossola", 7, 16),
	(62, "shaun", 10, 35),
	(64, "horatio", 7, 16),
	(71, "zorba", 10, 35),
	(74, "horatio", 9, 25.5),
	(85, "art", 3, 25.5),
	(88, "kevin", 3, 25.5),
	(89, "will", 3, 25.5),
	(90, "josh", 3, 25.5),
	(95, "bob", 3, 63.5),
]

boats = [
	(101, "Interlake", "blue", 45),
	(102, "Interlake", "red", 45),
	(103, "Clipper", "green", 40),
	(104, "Clipper", "red", 40),
	(105, "Marine", "red", 35),
	(106, "Marine", "green", 35),
	(107, "Marine", "blue", 35),
	(108, "Driftwood", "red", 35),
	(109, "Driftwood", "blue", 35),
	(110, "Klapser", "red", 30),
	(111, "Sooney", "green", 28),
	(112, "Sooney", "red", 28),
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

for s in sailors:
	sailor = Sailor(sid=s[0], sname=s[1], rating=s[2], age=s[3])
	session.add(sailor)

for b in boats:
	boat = Boat(bid=b[0], bname=b[1], color=b[2], length=b[3])
	session.add(boat)

for r in reserves:
	reserve = Reservation(sid=r[0], bid=r[1], day=r[2])
	session.add(reserve)

session.commit()