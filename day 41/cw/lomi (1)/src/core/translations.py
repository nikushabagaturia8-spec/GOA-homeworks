TRANSLATIONS = {
    "en": {
        "controls": "Controls:",
        "run": "ENTER/SPACE - Run",
        "speed": "UP/DOWN - Speed",
        "next_level": "N - Next Level",
        "prev_level": "P - Prev Level",
        "restart": "R - Restart Level",
        "music_toggle": "M - Music On/Off",
        "stop": "S - Stop",
        "quit": "Q - Quit",
        "code_file": "Code: my_program.py",
        
        "level_goal": "Level Goal:",
        "position": "Position:",
        "facing": "Facing:",
        "beepers": "Beepers:",
        
        "north": "North ↑",
        "south": "South ↓",
        "east": "East →",
        "west": "West ←",
        
        "place_beepers": "Place beepers at:",
        "positions": "positions",
        "collect": "Collect",
        "beeper_s": "beeper(s)",
        "return_to": "Return to",
        
        "level_complete": "Level Complete!",
        "level_incomplete": "Level Incomplete!",
        "blocked": "Blocked!",
        "no_beeper": "No Beeper!",
        "empty_bag": "Empty Bag!",
        
        "try_again": "Try Again - Press R to restart",
        "next_level_msg": "Press any key for next level",
        
        "all_beepers_collected": "All beepers collected!",
        "all_beepers_placed": "All beepers placed correctly!",
        "not_all_collected": "Not all beepers collected!",
        "not_all_placed": "Not all beepers placed at goal positions!",
    },
    
    "ka": {
        "controls": "მართვა:",
        "run": "ENTER/SPACE - გაშვება",
        "speed": "UP/DOWN - სიჩქარე",
        "next_level": "N - შემდეგი დონე",
        "prev_level": "P - წინა დონე",
        "restart": "R - თავიდან",
        "music_toggle": "M - მუსიკა ჩართ/გამორთ",
        "stop": "S - გაჩერება",
        "quit": "Q - გასვლა",
        "code_file": "კოდი: my_program.py",
        
        "level_goal": "დონის მიზანი:",
        "position": "პოზიცია:",
        "facing": "მიმართულება:",
        "beepers": "ბიპერები:",
        
        "north": "ჩრდილოეთი ↑",
        "south": "სამხრეთი ↓",
        "east": "აღმოსავლეთი →",
        "west": "დასავლეთი ←",
        
        "place_beepers": "დადე ბიპერები:",
        "positions": "პოზიციებზე",
        "collect": "შეაგროვე",
        "beeper_s": "ბიპერი",
        "return_to": "დაბრუნდი",
        
        "level_complete": "დონე დასრულებულია!",
        "level_incomplete": "დონე არ არის დასრულებული!",
        "blocked": "ბლოკირებული!",
        "no_beeper": "ბიპერი არ არის!",
        "empty_bag": "ჩანთა ცარიელია!",
        
        "try_again": "სცადე ისევ - დააჭირე R-ს",
        "next_level_msg": "შემდეგი დონისთვის დააჭირე ნებისმიერ ღილაკს",
        
        "all_beepers_collected": "ყველა ბიპერი შეგროვებულია!",
        "all_beepers_placed": "ყველა ბიპერი სწორად არის დადებული!",
        "not_all_collected": "ყველა ბიპერი არ არის შეგროვებული!",
        "not_all_placed": "ყველა ბიპერი არ არის დადებული!",
    }
}


def get_text(key, lang="en"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
