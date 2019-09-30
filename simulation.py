import argparse
import csv
import urllib.request
from urllib.error import HTTPError, URLError


class Queue:
    """
    A class object that represents a queue.
    """
    # default constructor
    def __init__(self):
        self.items = []

    # checks to see if queue object is empty
    def is_empty(self):
        return self.items == []

    # add item to queue
    def enqueue(self, item):
        self.items.insert(0, item)

    # removes an item from the queue
    def dequeue(self):
        return self.items.pop()

    # returns how many items are in queue
    def size(self):
        return len(self.items)


class Server:
    """
    A class object that represents a server.
    """
    # default constructor
    def __init__(self):
        self.current_request = None
        self.current_time = 0
        self.time_remaining = 0

    # increments a second on the server
    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining - 1
        if self.time_remaining <= 0:
            self.current_request = None
        self.current_time += 1

    # checks to see if server is in use
    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False

    # allows server to start processing a request
    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_process_time()


class Request:
    # default constructor
    def __init__(self, time):
        self.timestamp = int(time[0])
        self.process_time = int(time[2])

    # returns time a request came in
    def get_stamp(self):
        return self.timestamp

    # returns how long a request takes to process
    def get_process_time(self):
        return self.process_time

    # returns the wait time for a request
    def wait_time(self, current_time):
        return current_time - self.timestamp


def downloadCSV(url):
    """
    Function that takes in a url, downloads the data, and returns the data as a list to caller.
    :param url: A url that contains a csv file
    :return: csvlist: A list containing data from a csv file
    """
    # blank list to hold csv data
    csvlist = []

    # open the url, read it, and then decode it from binary to utf
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    # initialize a csv reader and pass string data to it, splitting it by lines
    csvreader = csv.reader(html.splitlines())

    # iterate through csv reader and add each row to a list before returning it to the caller
    for item in csvreader:
        csvlist.append(item)

    return csvlist


def simulateOneServer(csv_list):
    """
    Function that simulates the processing of requests passed in by a list using 1 server.
    :param csv_list: List containing data from a csv file
    :return:
    """
    # create server object, queue object, and list to store waiting times
    server = Server()
    server_queue = Queue()
    waiting_times = []

    # variable for how many seconds the simulation runs for
    num_of_seconds = 20000

    # set a loop that increments through every second of the simulation
    for current_second in range(num_of_seconds):
        # set a loop that increments through each item of the list
        for item in csv_list:
            # check to see if the incoming time of a request in the list matches the current second
            if int(item[0]) == current_second:
                request = Request(item)
                server_queue.enqueue(request)

            # check to see if server is busy and whether the queue is empty
            if (not server.busy()) and (not server_queue.is_empty()):
                next_task = server_queue.dequeue()
                waiting_times.append(next_task.wait_time(current_second))
                server.start_next(next_task)

                # calculate average wait time and print out the average
                average_wait = sum(waiting_times) / len(waiting_times)
                print("Average Wait %6.2f secs %3d tasks remaining." % (average_wait, server_queue.size()))

        # run server tick to take into account the next second
        server.tick()


def simulateManyServers(csv_list, num_of_servers):
    """
    Function that simulates the processing of requests passed in by a list using the number of server passed in.
    :param csv_list: List containing data from a csv file
    :return:
    """

    # create list to store dynamic amount of servers, queue object, and list to store waiting times
    servers_list = []
    server_queue = Queue()
    waiting_times = []

    # variable for how many seconds the simulation runs for
    num_of_seconds = 20000

    # loop to update servers list with the number of servers requested
    for num in range(num_of_servers):
        servers_list.append(Server())

    # set a loop that increments through every second of the simulation
    for current_second in range(num_of_seconds):
        # set a loop that increments through each item of the list
        for item in csv_list:
            # check to see if the incoming time of a request in the list matches the current second
            if int(item[0]) == current_second:
                request = Request(item)
                server_queue.enqueue(request)

            # loop that goes through the list of servers
            for server in servers_list:
                # check to see if server is busy and whether the queue is empty
                if (not server.busy()) and (not server_queue.is_empty()):
                    next_task = server_queue.dequeue()
                    waiting_times.append(next_task.wait_time(current_second))
                    server.start_next(next_task)

                    # calculate average wait time and print out the average
                    average_wait = sum(waiting_times) / len(waiting_times)
                    print("Average Wait %6.2f secs %3d tasks remaining." % (average_wait, server_queue.size()))

        # loop through the server list and run tick for each of them
        for server in servers_list:
            server.tick()


def main():
    """
    Main function that get called when application runs
    :return:
    """
    # initialize argument parser, add arguments, and then parse into script
    parser = argparse.ArgumentParser(description='Script that downloads csv data from URL')
    parser.add_argument('url', type=str, help='Url that contains a csv file.')
    parser.add_argument('-s', '--servers', type=int, default=1, help='Number of servers to simulate')
    args = parser.parse_args()

    # call downloadCSV function and pass in the url arg, print message to screen if there is an issue and exit
    try:
        csv_data = downloadCSV(args.url)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request. Please check your url!')
        print('Error code: ', e.code)
    except URLError as e:
        print('We are unable to reach the server. Please check your url!')
        print('Reason: ', e.reason)
    else:
        # check to see if optional servers were entered
        if args.servers > 1:
            # call function to simulate the number of servers passed in
            simulateManyServers(csv_data, args.servers)
        else:
            # call function to simulate 1 server with csv data
            simulateOneServer(csv_data)


if __name__ == '__main__':
    main()