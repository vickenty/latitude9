def draw_line(x, y, cx, cy):
    dx = abs(x - cx)
    dy = abs(y - cy)
    sx = 1 if cx - x > 0 else -1
    sy = 1 if cy - y > 0 else -1
    err = dx - dy

    while True:
        yield x, y

        if x == cx and y == cy:
            break
        
        err2 = 2 * err
        if err2 > -dy:
            err = err - dy
            x += sx
        if err2 < dx:
            err = err + dx
            y += sy

if __name__ == '__main__':
    for x, y in draw_line(0, 0, -5, 15):
        print x, y
