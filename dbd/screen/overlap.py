import numpy as np

def overlap(line, box, buffer=2):
    # Buffer the box points with simple loop
    buffered_box = box.copy()
    for i in range(4):
        buffered_box[i, 0] = buffered_box[i, 0] - buffer if i < 2 else buffered_box[i, 0] + buffer
        buffered_box[i, 1] = buffered_box[i, 1] - buffer if i in [0, 3] else buffered_box[i, 1] + buffer

    # Check intersection with each box edge
    for i in range(4):
        next_i = (i + 1) % 4
        # Calculate line coefficients
        a2 = buffered_box[next_i, 1] - buffered_box[i, 1]
        b2 = buffered_box[i, 0] - buffered_box[next_i, 0]
        c2 = a2*buffered_box[i, 0] + b2*buffered_box[i, 1]
        a1 = line[3] - line[1]
        b1 = line[0] - line[2]
        c1 = a1*line[0] + b1*line[1]
        determinant = a1*b2 - a2*b1
        
        if determinant != 0:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            if (min(buffered_box[i, 0], buffered_box[next_i, 0]) <= x <= max(buffered_box[i, 0], buffered_box[next_i, 0]) and
                min(buffered_box[i, 1], buffered_box[next_i, 1]) <= y <= max(buffered_box[i, 1], buffered_box[next_i, 1]) and
                min(line[0], line[2]) <= x <= max(line[0], line[2]) and
                min(line[1], line[3]) <= y <= max(line[1], line[3])):
                return True
    return False