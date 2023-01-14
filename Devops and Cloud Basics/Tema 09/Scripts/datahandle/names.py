from imdbdatascrapping import movies, actors, top_actors, actor_names

def get():
    last_ten_year_movies = movies.get(2012, 2022)
    actors_casted_in_these_movies = actors.get(last_ten_year_movies)
    top_ten_casted_actors = top_actors.get(actors_casted_in_these_movies, 10)
    actors_names_list = actor_names.get(top_ten_casted_actors)
    return actors_names_list