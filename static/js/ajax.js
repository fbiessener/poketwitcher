"use strict";

// Show Search Results

// function replaceSearchResults(res) {
//     $("#search-info").html(res);
//     console.log(res);
// }

// function showSearchResults(evt) {
//     evt.preventDefault();

//     let url = "/search.json";
//     let formData = {"results": $("#search-field").val()};

//     $.get(url, formData, replaceSearchResults(formData.results));
// }

// $("#search-form").on('submit', showSearchResults);

// ANONYMOUS INLINE FUNCTION

$('#search-form').on('submit', (evt) => {
  evt.preventDefault();
  let url = '/search.json';
  const formValues = $('#search-field').serialize();
  $.get(url, formValues, (response) => {
    $('#search-info').html(response.card);
  });
});
