import math

def get_tile_center(x, y, tile_size):
    x = x * tile_size + tile_size / 2
    y = y * tile_size + tile_size / 2
    return (x, y)

def get_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return None
        return -c / b
    
    delta = b**2 - 4 * a * c
    if delta < 0:
        return None
    else:
        sqrt_delta = math.sqrt(delta)
        root1 = (-b + sqrt_delta) / (2 * a)
        root2 = (-b - sqrt_delta) / (2 * a)
        return (root1, root2)

def get_interception(tower, enemy):
    t0 = 0
    for i in range(enemy.path_index, len(enemy.path) - 1):
        if i == enemy.path_index:
            x1, y1 = enemy.x, enemy.y
        else:
            x1, y1 = enemy.path[i]
        x2, y2 = enemy.path[i + 1]

        dx, dy = x2 - x1, y2 - y1
        t = get_distance(x1, y1, x2, y2) / enemy.current_speed
        vx, vy = dx / t, dy / t

        delta_x, delta_y = x1 - tower.x, y1 - tower.y

        a = vx**2 + vy**2 - tower.current_bullet_speed**2
        b = 2 * (vx * delta_x + vy * delta_y - tower.current_bullet_speed**2 * t0)
        c = delta_x**2 + delta_y**2 - tower.current_bullet_speed**2 * t0**2

        root1, root2 = solve_quadratic(a, b, c)
        res = None
        if root1 >= 0:
            if res == None:
                res = root1
        if root2 >= 0:
            if res == None or root2 < res:
                res = root2
        
        if res is not None and res <= t:
            return (x1 + vx * res, y1 + vy * res, int(t0 + res))
        
        t0 += t
    
    return None