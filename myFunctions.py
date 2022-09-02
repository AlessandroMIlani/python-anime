from AnilistPython import Anilist
import random


def get_anime(genre_list, years, vote):
    anilist = Anilist()
    # Get anime list
    if years[0] == years[1] or years[0] > years[1]:
        print("Error: invalid year range")
        print("Years will not be considered as a filter")
        random_anime = anilist.search_anime(genre=genre_list, score=range(int(vote), 101))
    else:
        # Get random anime
        random_anime = anilist.search_anime(genre=genre_list, score=range(int(vote), 101), year=years)
    # if random_anime is empty, get another one
    if len(random_anime) != 0:
        picked = random.choice(random_anime)
        anilist.print_anime_info(picked["name_english"])
    else:
        print("No anime found")