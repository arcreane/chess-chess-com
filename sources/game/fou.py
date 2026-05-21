def fou_p(plateau , position):
    x , y = position
    coups = []
    dir = [(-1 , -1) , (-1 , 1) , (1 , -1) , (1 , 1)]

    for dx , dy in dir:
        nx , ny = x + dx, y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            if plateau[nx][ny] == '.':
                coups.append((nx , ny))
            elif plateau[nx][ny] == 'N':
                coups.append((nx,ny))
            else:
                break
            nx += dx
            ny += dy

    return coups



