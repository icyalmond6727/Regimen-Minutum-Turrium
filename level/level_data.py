LEVELS = {
    1: {
        "level_button": (100, 150, 60, 100),
        "path_tiles": [
            [(2, 0), (2, 5), (10, 5), (10, 11)]
        ],
        "build_tiles": [(4, 3), (6, 3), (8, 3), (4, 7), (6, 7), (8, 7)],
        "starting_gold": 100,
        "starting_lives": 20,
        "wave_count": 3,
        "waves": [
            [
                ("spawn", 0, "Scout Drone", 5, 60)
            ],
            [
                ("spawn", 0, "Juggernaut Mech", 2, 90),
                ("delay", 60),
                ("spawn", 0, "Scout Drone", 5, 60)
            ],
            [
                ("spawn", 0, "Scout Drone", 15, 30),
                ("delay", 60),                     
                ("spawn", 0, "Juggernaut Mech", 4, 60)
            ]
        ]
    },
    2: {
        "path_tiles": [
            [(5, 0), (5, 11)]
        ],
        "build_tiles": [(3, 3), (5, 3), (7, 3), (3, 5), (7, 5), (3, 7), (5, 7), (7, 7)],
        "wave_count": 5,
        "level_button": (200, 150, 60, 100),
        "starting_gold": 200,
        "starting_lives": 20,
        "waves": [
            [
                
            ],
            [
                
            ],
            [

            ], 
            [

            ], 
            [

            ]
        ]
    }
}