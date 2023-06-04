import numpy as np
import heapq


def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(array, start, goal, obstacles):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # 超出列范围
                    continue
            else:
                # 超出行范围
                continue

            if neighbor in obstacles:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return None


if __name__ == '__main__':
    array = np.zeros((510,690))
    start = (0, 0)
    goal = (500,600)
    obstacles = [[154-15, 216-15, 221+15, 215+15]]
    for obs in obstacles:
        array[obs[1]:obs[1]+obs[3], obs[0]:obs[0]+obs[2]] = 1
    path = astar(array, start, goal, obstacles)
    length = len(path)
    Path=[]
    for i in range(length-2):
        if (path[i+2][0]-path[i][0]) == 0 and (path[i+1][0]-path[i][0]) != 0:
            Path.append(path[i+1])
        if (path[i+2][0]-path[i][0]) != 0 and (path[i+1][0]-path[i][0]) == 0:
            Path.append(path[i+1])
        elif(path[i+2][0]-path[i][0]) != 0 and (path[i+1][0]-path[i][0]) != 0 and (path[i+2][1]-path[i][1])/(path[i+2][0]-path[i][0]) != (path[i+1][1]-path[i][1])/(path[i+1][0]-path[i][0]):
            Path.append(path[i+1])
        else:
            continue
    print(Path)
    #print(path)