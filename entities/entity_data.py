import config

TOWERS = {
    "Pulse Blaster": {
        "name": "Pulse Blaster",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 200,
        "damage": 10,
        "attack_speed": 30,
        "bullet_speed": 5,
        "gold_cost": 50,
        "color": (0, 255, 0)
    },
    "Railgun Sentinel": {
        "name": "Railgun Sentinel",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 400,
        "damage": 50,
        "attack_speed": 90,
        "bullet_speed": 20,
        "gold_cost": 100,
        "color": (0, 0, 255)
    }
}

ENEMIES = {
    "Scout Drone": {
        "name": "Scout Drone",
        "width": config.TILE_SIZE * 0.25,
        "height": config.TILE_SIZE * 0.25,
        "health": 50,
        "speed": 0.75,
        "gold_yield": 10,
        "lives_penalty": 1,
        "color": (255, 0, 0)
    },
    "Juggernaut Mech": {
        "name": "Juggernaut Mech",
        "width": config.TILE_SIZE * 0.75,
        "height": config.TILE_SIZE * 0.75,
        "health": 200,
        "speed": 0.25,
        "gold_yield": 50,
        "lives_penalty": 2,
        "color": (150, 0, 0)
    }
}