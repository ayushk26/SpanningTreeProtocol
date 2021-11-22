
class Bridge():

    def __init__(self, name, ports):
        self.name = name
        self.ports = ports
        self.current_best_message = self.name+" "+str(0)+" "+self.name
        self.previous_received_message = ""
        self.previous_sent_message = ""
        self.port_type = {}
        self.assumed_root = self.name
        self.received_best_message = self.name+" "+str(0)+" "+self.name

    def initialise_ports(self):
        for port in self.ports:
            self.port_type[port.name] = "DP"

    def send_message(self, time,trace):
        # message is a string of type "Bi d Bj"
        self.previous_sent_message = self.current_best_message
        for port in self.ports:
            # if self.port_type[port.name] != "NP":
            if int(trace) == 1 :
                print(str(time)+" "+self.name + " s (" + self.current_best_message + ") at port " + port.name)
            port.messages.append(self.current_best_message)


    def receive_message(self, time,trace):
        for port in self.ports:
            for msg in port.messages:
                if msg != self.previous_sent_message :
                    if (int(trace) == 1):
                        print(str(time)+" "+self.name + " r (" + msg + ") at port " + port.name)
                    # If the root bridge index is less in message
                    if int(msg.split(" ")[0][1:]) < int(self.current_best_message.split(" ")[0][1:]):
                        self.received_best_message = msg
                        self.current_best_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                               self.name
                        self.assumed_root = msg.split(" ")[0]
                        # change the port type to root
                        for key in self.port_type:
                            if self.port_type[key] == "RP":
                                self.port_type[key] = "DP"
                        self.port_type[port.name] = "RP"
                        self.previous_received_message = msg

                    # If the root bridge index is equal in message
                    elif int(msg.split(" ")[0][1:]) == int(self.current_best_message.split(" ")[0][1:]):
                        # If the root bridge index is equal in message and distance is less
                        if int(msg.split(" ")[1]) + 1 < int(self.current_best_message.split(" ")[1]):
                            self.received_best_message = msg
                            self.current_best_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                                   self.name
                            self.assumed_root = msg.split(" ")[0]
                            #Change the port type to root
                            for key in self.port_type:
                                if self.port_type[key] == "RP":
                                    self.port_type[key] = "DP"
                            self.port_type[port.name] = "RP"
                            self.previous_received_message = msg

                        # If the root bridge index is equal in message and distance is equal
                        elif int(msg.split(" ")[1]) + 1 == int(self.current_best_message.split(" ")[1]):
                            # If the root bridge index is equal in message and distance is equal but sender has less index
                            if int(msg.split(" ")[2][1:]) < int(self.current_best_message.split(" ")[2][1:]) and msg != self.received_best_message:
                                self.received_best_message = msg
                                self.current_best_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                                       self.name
                                self.assumed_root = msg.split(" ")[0]
                                for key in self.port_type:
                                    if self.port_type[key] == "RP":
                                        for remove_port in self.ports:
                                            if remove_port.name == key:
                                                self.ports.remove(remove_port)
                                        self.port_type[key] = "NP"
                                self.port_type[port.name] = "RP"
                                self.previous_received_message = msg
                            elif int(msg.split(" ")[2][1:]) > int(self.current_best_message.split(" ")[2][1:]) :
                                self.ports.remove(port)
                                self.port_type[port.name] = "NP"
                                self.previous_received_message = msg
                            elif int(msg.split(" ")[2][1:]) == int(self.current_best_message.split(" ")[2][1:]) and msg != self.received_best_message :
                                self.ports.remove(port)
                                self.port_type[port.name] = "NP"
                                self.previous_received_message = msg
                        else:
                            if msg.split(" ")[2] == self.received_best_message.split(" ")[2]:
                                self.ports.remove(port)
                                self.port_type[port.name] = "NP"
                                self.previous_received_message = msg
                    else:
                        self.previous_received_message = msg



        noDP = True
        for key in self.port_type:
            if self.port_type[key] == "DP":
                noDP = False
                break
        if noDP:
            for key in self.port_type:
                self.port_type[key] = "NP"


class Lan():
    def __init__(self, name):
        self.name = name
        self.messages = []

    def clear_messages(self):
        self.messages = []