
sequence = "{2}{3}{20}{4}{5}"
rules = []
with open('output.txt', 'r') as f:
    for line in f:
        line = line.replace(' ', '')
        splitted = line.split('==>')
        lhs = splitted[0]
        rhs = splitted[1].split('#')[0]
        sup = splitted[1].split('#')[1]
        conf = splitted[1].split('#')[2]


        if lhs in sequence and rhs in sequence:
            #print(lhs, '==>',rhs)
            if lhs in rhs:
                splitted = rhs.split(lhs)
                head = splitted[0]
                tail = splitted[1]
                if tail:
                    #print(lhs, '==>',tail)
                    rule = lhs + '==>' +tail
                    if rule not in rules:
                        rules.append(rule)
        # else:
        #    print(lhs, '========>',rhs)
        # if lhs in rhs:
        #     splitted = rhs.split(lhs)
        #     head = splitted[0]
        #     tail = splitted[1]
        #     #print(tail, head)
        #     if tail:
        #         rule = lhs + '==>' +tail
        #         if rule not in rules:
        #             rules.append(rule)
        #         #print(lhs, '==>', tail)
        #         #print("-------------------")
        # #else:
        #     #print(lhs, '===>', rhs)
        # #print(lhs, rhs, sup, conf)

for r in rules:
    print(r)
