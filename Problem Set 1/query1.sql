SELECT B.bid, B.bname, COUNT(*) AS "# of Reserves"
FROM boats B, reserves R
WHERE B.bid = R.bid
GROUP BY B.bid
ORDER BY B.bid;

SELECT S.sid, S.sname
FROM sailors S
WHERE NOT EXISTS (SELECT *
		  FROM boats B
                  WHERE B.color = 'red' AND NOT EXISTS (SELECT *
							FROM reserves R
                                                        WHERE S.sid = R.sid AND B.bid = R.bid));
                                                        
SELECT S.sid, S.sname
FROM sailors S
WHERE S.sid IN (SELECT R1.sid
		FROM reserves R1, boats B1
                WHERE R1.bid = B1.bid AND B1.color = 'red')
AND S.sid NOT IN (SELECT R2.sid
		  FROM reserves R2, boats B2
                  WHERE R2.bid = B2.bid and B2.color != 'red');
                  
SELECT B.bid, B.bname, COUNT(*)
FROM boats B, reserves R1
WHERE B.bid = R1.bid
GROUP BY B.bid
HAVING COUNT(*) >= ALL (SELECT COUNT(*)
			FROM reserves R2
                        GROUP BY R2.bid);
                        
SELECT S.sid, S.sname
FROM sailors S
WHERE S.sid NOT IN (SELECT R.sid
		    FROM reserves R, boats B
		    WHERE R.bid = B.bid AND B.color = 'red');
                    
SELECT AVG(S.age)
FROM sailors S
WHERE S.rating = 10;

SELECT S1.sid, S1.sname, S1.age, S1.rating
FROM sailors S1
HAVING S1.age <= ALL (SELECT S2.age
		      FROM sailors S2
                      WHERE S1.rating = S2.rating)
ORDER BY S1.rating;
