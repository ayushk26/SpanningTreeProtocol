
class Bridge():

    def __init__(self, name, ports):
        self.name = name
        self.ports = ports
        self.current_message = self.name+" "+str(0)+" "+self.name
        self.previous_received_message = ""
        self.previous_sent_message = ""
        self.port_type = {}
        self.assumed_root= self.name
        self.previous_received_message = ""

    def initialise_ports(self):
        for port in self.ports:
            self.port_type[port.name] = "DP"

    def send_message(self, time):
        # message is a string of type "Bi d Bj"
        self.previous_sent_message = self.current_message
        for port in self.ports:
            print(str(time) + self.name + " s " + self.current_message)
            port.messages.append(self.current_message)
            data = {"t":time, "type":"s", "bridge":self.name, "message":self.current_message}


    def receive_message(self, time):
        for port in self.ports:
            for msg in port.messages:
                if msg != self.previous_sent_message:
                    print(str(time)+self.name+" r "+msg)
                    # If the root bridge index is less in message
                    if int(msg.split(" ")[0][1:]) < int(self.current_message.split(" ")[0][1:]):
                        self.current_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                               self.name
                        self.assumed_root = msg.split(" ")[0]
                        # change the port type to root
                        for key in self.port_type:
                            if self.port_type[key] == "RP":
                                self.port_type[key] = "DP"
                        self.port_type[port.name] = "RP"
                        self.previous_received_message = msg

                    # If the root bridge index is equal in message
                    elif int(msg.split(" ")[0][1:]) == int(self.current_message.split(" ")[0][1:]):
                        # If the root bridge index is equal in message and distance is less
                        if int(msg.split(" ")[1]) < int(self.current_message.split(" ")[1]) :
                            self.current_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                                   self.name
                            self.assumed_root = msg.split(" ")[0]
                            for key in self.port_type:
                                if self.port_type[key] == "RP":
                                    self.port_type[key] = "DP"
                            self.port_type[port.name] = "RP"
                            self.previous_received_message = msg

                        # If the root bridge index is equal in message and distance is equal
                        elif int(msg.split(" ")[1]) == int(self.current_message.split(" ")[1]):
                            # If the root bridge index is equal in message and distance is equal but sender has less index
                            if int(msg.split(" ")[2][1:]) < int(self.previous_received_message.split(" ")[2][1:]):
                                self.current_message = msg.split(" ")[0] + " " + str(int(msg.split(" ")[1]) + 1) + " " + \
                                                       self.name
                                self.assumed_root = msg.split(" ")[0]
                                for key in self.port_type:
                                    if self.port_type[key] == "RP":
                                        self.port_type[key] = "DP"
                                self.port_type[port.name] = "RP"
                                self.previous_received_message = msg

                                for key in self.port_type:
                                    if self.port_type[key] == "DP" and key != port.name :
                                        self.port_type[key] = "NP"
                                        # self.ports.remove(port)

                            # If the root bridge index is equal in message and distance is equal but sender has equal index
                            elif msg.split(" ")[2] == self.previous_received_message.split(" ")[2] :
                                self.port_type[port.name] = "NP"
                                # self.ports.remove(port)
                            else :
                                self.port_type[port.name] = "NP"
                                # self.ports.remove(port)
                        else:
                            if  self.port_type[port.name] == "RP":
                                self.port_type[port.name] = "NP"
                                # self.ports.remove(port)


class Lan():

    def __init__(self, name):
        self.name = name
        self.messages = []

    def clear_messages(self):
        self.messages = []