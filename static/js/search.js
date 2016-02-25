$(function() {
  $("#drugs").autocomplete({
    source: "/get_drugs/",
    minLength: 1,
  });
});

$(function() {
  $("#categories").autocomplete({
    source: "/categories/",
    minLength: 1,
  });
});
