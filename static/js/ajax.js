"use strict";

// Show Search Results

function replaceSearchResults(res) {
    $("#search-info").html(res);
    console.log(res='Missing?');
}

function showSearchResults(evt) {
    evt.preventDefault();

    let url = "/search.json";
    let formData = {"Results": $("#search-field").val()};

    $.get(url, formData, replaceSearchResults);
}

$("#search-form").on('submit', showSearchResults);

// SERVER-SIDE

// @app.route('/weather.json')
// def weather():
//     """Return a weather-info dictionary for this zipcode."""

//     zipcode = request.args.get('zipcode')
//     weather_info = WEATHER.get(zipcode, DEFAULT_WEATHER)
//     return jsonify(weather_info)

// AJAX ADVANCED

// Written now to use an inline function for handling the
// AJAX success handler.

// function showWeather(evt) {
//     evt.preventDefault();

//     let url = "/weather.json";
//     let formData = {"zipcode": $("#zipcode-field").val()};

//     $.get(url, formData, function (results) {
//         $("#weather-info").html(results.forecast);
//     });
// }

// $("#weather-form").on('submit', showWeather);

// AJAX SIMPLE

// PART 2: SHOW WEATHER

// function replaceForecast(results) {
//     $("#weather-info").html(results.forecast);
// }

// function showWeather(evt) {
//     evt.preventDefault();

//     let url = "/weather.json";
//     let formData = {"zipcode": $("#zipcode-field").val()};

//     $.get(url, formData, replaceForecast);
// }

// $("#weather-form").on('submit', showWeather);

// HTML

  // <h2>Weather Service</h2>

  // <form id="weather-form">
  //   <div class="form-group">
  //     Want weather?
  //     <input class="form-control" type="text" name="zipcode" id="zipcode-field"
  //            placeholder="zipcode">
  //   </div>
  //   <div class="form-group">
  //     <button class="btn btn-primary" type="submit">Get It</button>
  //   </div>
  // </form>

  // <div id="weather-info"></div>
