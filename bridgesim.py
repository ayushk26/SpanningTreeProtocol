from bridge import Bridge,Lan

trace = input()
n_bridges=input()
n_bridges =int(n_bridges)
lans = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
lans = lans.split(" ")
for lan in lans:
    lans[lans.index(lan)] = Lan(lans[lans.index(lan)])

loop_state=list(True for i in range(0,n_bridges))

bridge = list(range(0, int(n_bridges)))

for i in range(0, int(n_bridges)):
    x = input()
    bridge_name = (x.split(" "))[0][:-1]
    lan_names = x.split(" ")[1:]
    list_lans = []
    for lan in lans:
        if lan_names.__contains__(lan.name):
            list_lans.append(lan)
    bridge[i] = Bridge(bridge_name,list_lans)


loop_running = True
t =0

for b in bridge:
    b.initialise_ports()

while loop_running:

    for b in bridge:
        b.send_message(t)
    t +=1
    for b in bridge:
        b.receive_message(t)
    t+=1
    for lan in lans:
        lan.clear_messages()

    temp = bridge[0].current_message.split(" ")[0]
    loop_state = list(temp == b.current_message.split(" ")[0] for b in bridge)

    if not loop_state.__contains__(False):
        for b in bridge:
            b.send_message(t)
        break

for b in bridge:
    res = b.name+" "
    for key in b.port_type:
        res += str(key)+"-"+str(b.port_type[key])+" "

    print(res)



