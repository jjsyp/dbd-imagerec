import numpy as np

def merge_lines(lines, distance_threshold, angle_threshold):
    merged_lines = []

    # Sort the lines based on their mid-points. 
    # This is important to ensure that the merging algorithm correctly identifies overlapping lines.
    lines.sort(key = lambda line: ((line[0][0] + line[0][2])/2, (line[0][1] + line[0][3])/2))

    # For each line, check if it should be merged with the next one.
    for i in range(len(lines)-1):
        # Calculate the distance between the mid-points of the line segments
        distance = np.linalg.norm(np.subtract(((lines[i][0][0] + lines[i][0][2])/2, (lines[i][0][1] + lines[i][0][3])/2), ((lines[i+1][0][0] + lines[i+1][0][2])/2, (lines[i+1][0][1] + lines[i+1][0][3])/2)))

        # Calculate the angle between the line segments
        angle = abs(np.arctan2(lines[i+1][0][3] - lines[i+1][0][1], lines[i+1][0][2] - lines[i+1][0][0]) - np.arctan2(lines[i][0][3] - lines[i][0][1], lines[i][0][2] - lines[i][0][0]))

        if angle > np.pi:
            angle = 2*np.pi - angle

        # If the distance and angle between line segments are below some thresholds
        if distance < distance_threshold and angle < angle_threshold:
            # Merge the lines by creating a new line with averaged coordinates
            merged_lines.append([(lines[i][0][0] + lines[i+1][0][0]) / 2, 
                                    (lines[i][0][1] + lines[i+1][0][1]) / 2, 
                                    (lines[i][0][2] + lines[i+1][0][2]) / 2, 
                                    (lines[i][0][3] + lines[i+1][0][3]) / 2])
        else:
            merged_lines.append(lines[i])

    return merged_lines