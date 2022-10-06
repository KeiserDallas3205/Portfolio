/*
Name(s): Keiser Dallas
Date: 2/8/22
Course Number and Section: 330-001
Quarter: Winter 2022
Project # 2: This is a Prolog program that can apply vector equations to one or multiple 3D coordinates, which are provided by the user. 
*/

/* 1. dist/3, where the first two arguments are 3D coordinates and the third argument is
		matched with the distance between them. For example:
			
			?- dist((2.0,1.0,5.0),(-2.0,3.0,0.0),R).
			R = 6.708 
*/
 
 dist((A,B,C), (D,E,F), R) :- G is (A - D)** 2, H is (B - E)** 2, I is (C - F)**2, R is sqrt(G + H + I).


/* 2. vecLength/2, where the first argument is a 3D coordinate representing a vector and
		the second argument matches with the length of the vector. For example:
			
			?- vecLength((3.0,0.0,4.0),R).
			R = 5.0 */

vecLength((A,B,C), R) :- A1 is A ** 2, B1 is B ** 2, C1 is C ** 2, R is sqrt(A1 + B1 + C1).

/* 3. vecNorm/2, where the first argument is a 3D coordinate representing a vector and the
		second argument is matched with the vector in the same direction, but of length 1. For example:
			
				?- vecNorm((3.0,0.0,4.0),R).
				R = vec(0.6,0.0,0.8)
				
*/

vecNorm((A,B,C),R) :- vecLength((A,B,C),T), A1 is A / T, B1 is B / T, C1 is C / T, R = (A1,B1,C1).


/* 4. vecDot/3, where the first two arguments are 3D coordinates representing a vector
		and the third argument is matched with their dot product. For example:
			
			?- vecDot((1.0,2.0,3.0),(4.0,5.0,6.0),R).
			R = 32.0 
*/

vecDot((A,B,C),(D,E,F),R) :- G is A * D, H is B * E, I is C * F, R is G + H + I.


/* 5. vecAngle/3, where the first two arguments are 3D coordinates representing a vector
		and the third argument is matched with the angle between the vectors in radians.
			
			?- vecAngle((1.0,-2.0,-2.0),(6.0,3.0,2.0),R).
			R = 1.76 
*/

vecAngle((A,B,C),(A,B,C),0). 
vecAngle((A,B,C),(D,E,F), R) :- vecDot((A,B,C),(D,E,F), S), vecLength((A,B,C),V1), vecLength((D,E,F), V2),
									T is V1 * V2, R is acos(S / T).


/* 6. areOrthog/2, which succeeds if the vectors in each argument are orthogonal. For example:
		
		-? areOrthog((3,0,4),(-4,5,3)).
		true 
*/

areOrthog((A,B,C),(D,E,F)) :- vecDot((A,B,C),(D,E,F), R), R =:= 0. 


/* 7. vecCross/3, where the first two arguments are 3D coordinates representing vectors
		and the third argument is matched the vector representing their cross product. For example:
			
			?- vecCross((2.0,1.0,1.0),(-4.0,3.0,1.0),R).	
			R = (2.0,6.0,-10.0) 
*/

vecCross((A,B,C),(D,E,F),R) :- I is (B * F - C * E), J is -1 *(A * F - C * D), K is (A * E - B * D), R = (I,J,K).

/* 8. vecProj/3, where the first two arguments are 3D coordinates representing vectors
		and the third argument is matched the vector projection of the first onto the second. For example:
			
			?- vecProj((6.0,3.0,2.0),(1.0,-2.0,-2.0),R).
			R = (-0.444,0.889,0.889) */

vecProj((A,B,C),(D,E,F),R) :- vecDot((A,B,C),(D,E,F),T), vecLength((D,E,F),S), T1 is T / (S **2),
								D1 is D * T1, E1 is E * T1, F1 is F * T1, R = (D1, E1, F1).

/* 9. distPointLine/4, where the first argument is a point not on a line, the second
		argument is a 3D coordinate representing a vector parallel to a line, the third argument
		is a point on the line, and the fourth argument is matched with the distance from the
		point not on the line to the line. For example,
			
			?- disPointLine((1.0,1.0,5.0),(1.0,-1.0,2.0),(1,3,0),R).
			R = 2.236 
*/	

disPointLine((O1,O2,O3),(V1,V2,V3),(L1,L2,L3), R) :- A is L1 - O1, B is L2 - O2, C is L3 - O3, vecCross((A,B,C),(V1,V2,V3),N),
														vecLength(N,S),vecLength((V1,V2,V3),D), R is S / D. 

/* 10. distPointPlane/4, where the first argument is a point not on a plane, the second
		argument is a 3D coordinate representing a vector normal to a plane, the third
		argument is a point on the plane, and the fourth argument is matched with the distance
		from the point not on the plane to the plane. For example,
			
			?- disPointPlane((1.0,1.0,3.0),(3.0,2.0,6.0),(0,0,1),R).
			R = 2.429 
*/

disPointPlane((O1,O2,O3),(V1,V2,V3),(P1,P2,P3),R) :- D is V1 * P1 + V2 * P2 + V3 * P3, vecDot((V1,V2,V3),(O1,O2,O3),S), 
															vecLength((V1,V2,V3),F), R is abs(S - D)/ F.
														
														
