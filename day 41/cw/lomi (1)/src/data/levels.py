LEVELS = [
    {
        "id": 1,
        "name": "First Steps",
        "name_ka": "პირველი ნაბიჯები",
        "description": "Move Karel to collect the beeper and return home.",
        "description_ka": "გადაადგილდი, შეაგროვე ბიპერი და დაბრუნდი სახლში.",
        "karel_start": (0, 0, "east"),
        "beepers": [(3, 0, 1)],
        "walls": [],
        "goal_position": (0, 0),
    },
    {
        "id": 2,
        "name": "Around the Corner",
        "name_ka": "კუთხის გარშემო",
        "description": "Navigate around the wall to get the beeper.",
        "description_ka": "გადმოიარე კედლის გარშემო და მიაღწიე ბიპერს.",
        "karel_start": (0, 0, "east"),
        "beepers": [(2, 2, 1)],
        "walls": [(1, 0, "south"), (1, 1, "south")],
        "goal_position": None,
    },
    {
        "id": 3,
        "name": "Beeper Hunt",
        "name_ka": "ბიპერების ძიება",
        "description": "Collect all 3 beepers scattered around.",
        "description_ka": "შეაგროვე ყველა 3 ბიპერი რომელიც გაფანტულია.",
        "karel_start": (0, 0, "east"),
        "beepers": [(2, 0, 1), (4, 2, 1), (1, 3, 1)],
        "walls": [(3, 1, "south"), (2, 3, "east")],
        "goal_position": None,
    },
    {
        "id": 4,
        "name": "Simple Maze",
        "name_ka": "მარტივი ლაბირინთი",
        "description": "Navigate through the maze to reach the beeper.",
        "description_ka": "გადალახე ლაბირინთი და მიაღწიე ბიპერს.",
        "karel_start": (0, 0, "east"),
        "beepers": [(5, 4, 1)],
        "walls": [
            (2, 0, "south"), (2, 1, "south"), (0, 2, "east"), (1, 2, "east"),
            (3, 2, "south"), (3, 3, "south"), (4, 3, "west")
        ],
        "goal_position": None,
    },
    {
        "id": 5,
        "name": "Beeper Line",
        "name_ka": "ბიპერების ხაზი",
        "description": "Place beepers in a line from (0,0) to (5,0).",
        "description_ka": "დადე ბიპერები ხაზად (0,0)-დან (5,0)-მდე.",
        "karel_start": (0, 0, "east"),
        "beepers": [],
        "walls": [],
        "karel_beepers": 6,
        "goal_beepers": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)],
    },
    {
        "id": 6,
        "name": "The Labyrinth",
        "name_ka": "ლაბირინთი",
        "description": "Find your way through the labyrinth!",
        "description_ka": "იპოვე გზა ლაბირინთში!",
        "karel_start": (0, 0, "east"),
        "beepers": [(7, 7, 3)],
        "walls": [
            (1, 0, "south"), (1, 1, "south"), (3, 0, "south"), (3, 1, "south"),
            (3, 2, "south"), (0, 3, "east"), (1, 3, "east"), (3, 4, "south"),
            (3, 5, "south"), (5, 2, "south"), (5, 3, "south"), (5, 5, "east"),
            (5, 6, "east"), (6, 4, "south"), (7, 5, "west")
        ],
        "goal_position": None,
    },
    {
        "id": 7,
        "name": "Climbing Stairs",
        "name_ka": "კიბეების ასვლა",
        "description": "Climb the stairs and place a beeper on each step.",
        "description_ka": "ავიდი კიბეებზე და დადე ბიპერი თითოეულ საფეხურზე.",
        "karel_start": (0, 4, "east"),
        "beepers": [],
        "walls": [
            (1, 4, "north"), (1, 4, "east"), (2, 3, "north"), (2, 3, "east"),
            (3, 2, "north"), (3, 2, "east"), (4, 1, "north"), (4, 1, "east"),
            (5, 0, "north")
        ],
        "karel_beepers": 5,
        "goal_beepers": [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0)],
    },
    {
        "id": 8,
        "name": "Treasure Room",
        "name_ka": "საგანძურის ოთახი",
        "description": "Enter the treasure room and collect all beepers!",
        "description_ka": "შევიდი საგანძურის ოთახში და შეაგროვე ყველა ბიპერი!",
        "karel_start": (0, 4, "east"),
        "beepers": [(6, 2, 1), (7, 2, 1), (8, 2, 1), (6, 3, 1), (7, 3, 1), (8, 3, 1)],
        "walls": [
            (5, 1, "east"), (5, 2, "east"), (5, 3, "east"), (5, 4, "east"),
            (6, 1, "north"), (7, 1, "north"), (8, 1, "north"),
            (9, 1, "west"), (9, 2, "west"), (9, 3, "west"), (9, 4, "west"),
            (6, 5, "south"), (7, 5, "south"), (8, 5, "south"), (5, 5, "north")
        ],
        "goal_position": (0, 4),
    },
    {
        "id": 9,
        "name": "Square Path",
        "name_ka": "კვადრატული გზა",
        "description": "Walk in a square and return to start.",
        "description_ka": "იარე კვადრატად და დაბრუნდი საწყის წერტილში.",
        "karel_start": (0, 0, "east"),
        "beepers": [],
        "walls": [],
        "goal_position": (0, 0),
    },
    {
        "id": 10,
        "name": "Beeper Zigzag",
        "name_ka": "ბიპერების ზიგზაგი",
        "description": "Collect beepers in a zigzag pattern.",
        "description_ka": "შეაგროვე ბიპერები ზიგზაგის ფორმით.",
        "karel_start": (0, 0, "east"),
        "beepers": [(1, 0, 1), (2, 1, 1), (3, 0, 1), (4, 1, 1), (5, 0, 1)],
        "walls": [],
        "goal_position": None,
    },
    {
        "id": 11,
        "name": "Fill the Row",
        "name_ka": "შეავსე რიგი",
        "description": "Place beepers in a horizontal line.",
        "description_ka": "დადე ბიპერები ჰორიზონტალურ ხაზზე.",
        "karel_start": (0, 0, "east"),
        "beepers": [],
        "walls": [],
        "karel_beepers": 7,
        "goal_beepers": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)],
    },
    {
        "id": 12,
        "name": "Corner Collector",
        "name_ka": "კუთხეების შემგროვებელი",
        "description": "Collect beepers from all four corners.",
        "description_ka": "შეაგროვე ბიპერები ოთხივე კუთხიდან.",
        "karel_start": (2, 2, "east"),
        "beepers": [(0, 0, 1), (5, 0, 1), (0, 5, 1), (5, 5, 1)],
        "walls": [],
        "goal_position": None,
    },
    {
        "id": 13,
        "name": "Hurdle Jump",
        "name_ka": "ბარიერების გადახტომა",
        "description": "Navigate around hurdles to reach the beeper.",
        "description_ka": "გადალახე ბარიერები და მიაღწიე ბიპერს.",
        "karel_start": (0, 1, "east"),
        "beepers": [(7, 1, 1)],
        "walls": [
            (1, 0, "north"), (1, 1, "north"),
            (3, 0, "north"), (3, 1, "north"),
            (5, 0, "north"), (5, 1, "north")
        ],
        "goal_position": None,
    },
    {
        "id": 14,
        "name": "Double Line",
        "name_ka": "ორმაგი ხაზი",
        "description": "Place beepers in two parallel lines.",
        "description_ka": "დადე ბიპერები ორ პარალელურ ხაზზე.",
        "karel_start": (0, 0, "east"),
        "beepers": [],
        "walls": [],
        "karel_beepers": 12,
        "goal_beepers": [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)
        ],
    },
    {
        "id": 15,
        "name": "Diagonal Path",
        "name_ka": "დიაგონალური გზა",
        "description": "Collect beepers along the diagonal.",
        "description_ka": "შეაგროვე ბიპერები დიაგონალზე.",
        "karel_start": (0, 0, "east"),
        "beepers": [(0, 0, 1), (1, 1, 1), (2, 2, 1), (3, 3, 1), (4, 4, 1), (5, 5, 1)],
        "walls": [],
        "goal_position": None,
    },
    {
        "id": 16,
        "name": "Checkerboard",
        "name_ka": "ჭადრაკის დაფა",
        "description": "Place beepers in a checkerboard pattern.",
        "description_ka": "დადე ბიპერები ჭადრაკის დაფის ფორმით.",
        "karel_start": (0, 0, "east"),
        "beepers": [],
        "walls": [],
        "karel_beepers": 8,
        "goal_beepers": [
            (0, 0), (2, 0), (1, 1), (3, 1),
            (0, 2), (2, 2), (1, 3), (3, 3)
        ],
    },
    {
        "id": 17,
        "name": "Spiral Collector",
        "name_ka": "სპირალური შემგროვებელი",
        "description": "Collect beepers in a spiral pattern.",
        "description_ka": "შეაგროვე ბიპერები სპირალის ფორმით.",
        "karel_start": (0, 0, "east"),
        "beepers": [
            (2, 0, 1), (4, 0, 1), (4, 2, 1), (4, 4, 1),
            (2, 4, 1), (0, 4, 1), (0, 2, 1), (2, 2, 1)
        ],
        "walls": [],
        "goal_position": None,
    },
    {
        "id": 18,
        "name": "Final Challenge",
        "name_ka": "საბოლოო გამოწვევა",
        "description": "Navigate the maze, collect all beepers, and return home!",
        "description_ka": "გადალახე ლაბირინთი, შეაგროვე ყველა ბიპერი და დაბრუნდი სახლში!",
        "karel_start": (0, 0, "east"),
        "beepers": [(3, 2, 1), (6, 3, 1), (7, 7, 2)],
        "walls": [
            (1, 0, "south"), (1, 1, "south"), (3, 1, "east"), (3, 2, "east"),
            (2, 3, "south"), (4, 3, "south"), (5, 2, "south"), (5, 4, "east"),
            (6, 5, "south"), (6, 6, "south"), (4, 6, "east"), (3, 5, "north")
        ],
        "goal_position": (0, 0),
    },
]


def get_level(level_id):
    for level in LEVELS:
        if level["id"] == level_id:
            return level
    return None


def get_level_count():
    return len(LEVELS)


def get_all_levels():
    return LEVELS
