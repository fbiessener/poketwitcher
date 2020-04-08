# PokeTwitcher Project

An application that allows users to treat Pokémon Go as a birdwatching experience. Users can view and add sightings of Pokemon (restricted to currently available pokémon in Pokemon Go) to their Pokédex. This app was built using a Python/Flask backend and PostgreSQL database. The frontend is designed with Bootstrap and HTML.

## About Me:

Fiona tries very hard to keep plants alive. When failing to do that, she's adding more features to this app.

## Technologies:

* Python
* Flask
* PostGreSQL
* SQLAlchemy
* HTML
* Javascript (AJAX, JSON)
* jQuery
* Bootstrap
* Chart.js

## Features

### View Pokemon:
All Pokemon currently available in Pokemon are displayed on the pokemon route. Clicking on the ID, image or name will bring users to a detail page for that Pokemon where logged-in users may add sightings. The detail page displays a card with Pokemon image, ID, name, gender, and type. Chart.js is utilized to render a pie chart that displays the percentage of users who have/have not seen the Pokemon.

### Search for Pokemon:
* From the navbar, users may search for Pokemon name or username. Results are displayed in a Bootstrap card at the top of any page with an AJAX request. If a query finds a Pokemon or user in the DB that corresponds to input string, the results include an image and name which both link to the corresponding detail page.
* On the all pokemon route, jQuery is utilized for a live-search of the page. It manipulates the DOM to only display rows which contain the query string.

### Create/view a list of Pokemon sightings:
When logged in, users may add sightings of Pokemon. Sightings by a user are unique and timestamped automatically when added to the DB. User profiles display ID, name, and timestamp for entries. Chart.js is utilized to render a pie chart that displays a user's sightings broken down by Pokemon type.



## Future Implementation

### Testing Suite
Due to time constraints and a corrupted boot file in the second sprint, the original tests.py file was lost. Python's unittest library will be utilized to replicate the lost tests and implement further test coverage.

### GoogleMaps API
Users will log location of sighting and profiles will display a mini map populated with markers of sightings.

### Bulbapedia API
https://bulbapedia.bulbagarden.net/w/api.php?action=help&modules=main
Bulbapedia has its own MediaWiki API which will be used to add flavortext and missing images to Pokemon detail pages.

### Ranking of users/dynamic sorting of all-* tables
* To encourage competitive and social interactivity, the all-users page will be refactored to function as a leaderboard. Users will be ranked by Pokedex completeness. ID will be replaced with a rank column.
* Dynamic sorting will be implemented to allow users to order the tables on the all-pokemon and all-user pages by ID(Rank for users) or name(username for users).

## Installation

Git

```sh
$ git clone https://github.com/fbiessener/poketwitcher.git
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements
$ createdb poketwitcher
$ python3 seed.py
$ python3 server.py
```

0.0.0.0:5000

## License

## Planning

- Project Board: https://github.com/fbiessener/pt-tracker/projects/1?add_cards_query=is%3Aopen
- Visuals and Models: https://drive.google.com/drive/folders/1TVmpzDDEq1rczrivIA_VEc_JZgJfs-tA?usp=sharing

1. Sprint 1: MVP
2. Sprint 2: Feature Implementation