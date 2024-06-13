def overlap(line, box):
    #print(line)
    # Line represented as a1x + b1y = c1
    a1 = line[3] - line[1]
    b1 = line[0] - line[2]
    c1 = a1*(line[0]) + b1*(line[1])

    # Box represented as a2x + b2y = c2
    # compare line and all four lines of the box
    for i in range(0, 4):
        a2 = box[(i+1)%4, 1] - box[i, 1]
        b2 = box[i, 0] - box[(i+1)%4, 0]
        c2 = a2*box[i, 0] + b2*box[i, 1]

        determinant = a1*b2 - a2*b1

        if determinant != 0:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            if min(box[i, 0], box[(i+1)%4, 0]) <= x <= max(box[i, 0], box[(i+1)%4, 0]) and min(box[i, 1], box[(i+1)%4, 1]) <= y <= max(box[i, 1], box[(i+1)%4, 1]) and min(line[0], line[2]) <= x <= max(line[0], line[2]) and min(line[1], line[3]) <= y <= max(line[1], line[3]):
                return True
    return False