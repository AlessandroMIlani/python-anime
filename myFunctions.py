from AnilistPython import Anilist
import random
import time


def get_anime(genre_list, years, vote):
    anilist = Anilist()
    print("vote:", vote)
    # Get anime list
    if years[0] == years[1] or years[0] > years[1]:
        print("Error: invalid year range")
        print("Years will not be considered as a filter")
        random_anime = anilist.search_anime(genre=genre_list, score=range(int(vote), 101))
    else:
        # Get random anime
        random_anime = anilist.search_anime(genre=genre_list, year=[years[0], years[1]], score=range(int(vote), 100))
    # if random_anime is empty, get another one
    if len(random_anime) != 0:
        picked = random.Random(int(round(time.time() * 1000))).choice(random_anime)
        anilist.print_anime_info(picked["name_english"])
        return picked
    else:
        print("No anime found")
        return None
        
        

def get_font_markup(fontdesc, text):
    return f'<span font_desc="{fontdesc}">{text}</span>'
    
    
    