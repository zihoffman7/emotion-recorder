window.onload = function() {
  var elems = document.querySelectorAll(".log-form input[type='radio']");
  for (var i = 0, len = elems.length; i < len; i++) {
    elems[i].onmouseup = function() {
      this.dataset.checked = this.checked? 1 : "";
    }
    elems[i].onclick = function() {
      this.checked = !this.dataset.checked;
    }
  }
}

function toggleSeasonDropdown(elem) {
  var parent = elem;
  $(elem).find(".arrow").each(function() {
    if ($(parent).hasClass("active")) {
      $(parent).removeClass("active");
      $(this).removeClass("down");
      $(this).addClass("right");
      $(parent).find(".dropdown").each(function() {
        $(this).slideToggle(200);
      });
    }
    else {
      $(parent).addClass("active");
      $(this).removeClass("right");
      $(this).addClass("down");
      $(parent).find(".dropdown").each(function() {
        $(this).slideToggle(200);
      });
    }
  });
}

$(document).on("click", ".dropdown-click", function() {
  toggleSeasonDropdown(this.parentNode);
});
