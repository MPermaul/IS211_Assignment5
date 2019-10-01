# IS211_Assignment5
Week 5 Assignment 5

Author: Moses Permaul - moses.permaul13@spsmail.cuny.edu

Application Details:

1) This application contains 1 file: simulation.py

2) The simulation.py file is designed to run via command line.

3) When running the .py file, you must pass in a valid URL that has a csv file. Checks will be done to make sure the url is valid.

4) There is an optional argement that can be passed in and represents how many servers you want to use in the simulation. By default this is set to 1.

5) When a request is being processed by the server, the average wait time and how many tasks are still on the queue will be displayed.

6) When runing a simulation with more than 1 server, the requests will be sent to the servers in a round robin fashion:

	ex: python simulation.py http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv 3
	
	server 1 will get the first request	(start of round robin sequence)
	server 2 will get the next request
	server 3 will get the next request	(end of round robin sequence)
	server 1 will get the next request	(sequence starts over)

7) The application is set to simulate 20,000 seconds for both single and multiple servers.