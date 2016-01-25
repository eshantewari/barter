$(function() {
  $("#drugs").autocomplete({
    source: "/get_drugs/",
    minLength: 1,
  });
});
