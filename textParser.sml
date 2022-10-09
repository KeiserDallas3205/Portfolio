(*
Name(s): Keiser Dallas
Date: 1/6/2022 
Course Number and Section: 330-001
Quarter: Winter 2022
Project #: 1


Write an ML function named parse : string -> int list that inputs the name of a text file. Your function will parse the text file character by character. The output will be a list of all the integers contained in the file. The goal of this project is to build your own parser by examining the file character by character and deciding what to do.

For example, if the text file is named input.txt and contains:
     d3%~19^fgh54 78nm,.j
     1.2k~78bv
Then your function should work as follows:
     - parse("input.txt");
     val it = [3,~19,54,78,1,2,~78] : int list
	 
Note: This parser only handles (+/-)integers up to the double digits. 
*)




(* Main Function*)

fun parse(x:string) =  
	let 
		val file = TextIO.openIn(x) (*Create an instream for the file*)
		val input = TextIO.input(file) (*Load the files text intro a string*)
		val output = explode(input) (*Convert the string to a list of chars*)
		
		(*Function determines whether a character is an integer (1-9) -> bool*)
		fun isDigit (a:char) = 
			if (ord(a) >= 48 andalso ord(a) <= 57) 
				then true
			else false
		
		(*Function turns a char into an integer*)
		fun toInt (b:char) = ord(b)-48
		
		
		(*Function to put characters in list*)
		fun enterList (nil) = [] (* Empty file -> empty list*)
		
			(* Split the head from rest of list *)
			| enterList(temp as x::xs) = 
				
				(* If there are two consecutive digits *)
				if isDigit(x) andalso isDigit(hd(xs))
				
					(* Add the double digit number to list*)
					then ((toInt(x) * 10) + toInt(hd(xs)))::enterList(tl(xs))
				
				(* If there is only one digit *)
				else if isDigit(x)
					
					(* Add the singular digit *)
					then toInt(x)::enterList(xs)
					
				(* If there is a negative sign followed by two consecutive digits *)
				else if(ord(x) = 126 andalso isDigit(hd(xs)) andalso isDigit(hd(tl(xs))))
					
					(* Add the negative double digit number *)
					then (~((toInt(hd(xs)) * 10) + toInt(hd(tl(xs)))))::enterList(tl(xs))
				
				(* If there is a negative sign *)
				else if (ord(x) = 126 andalso isDigit(hd(xs)))
					
					(* Add the negative integer to the list *)
					then ~(toInt(hd(xs)))::enterList(tl(xs))
				
				
				(* If not an integer, then ignore and process the rest of the list *)
				else enterList(xs)
	in 
		enterList(output) (*char list -> int list *)
		
	end;
