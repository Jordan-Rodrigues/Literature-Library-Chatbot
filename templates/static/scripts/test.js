function nameFade() {
  console.log("test")
  $(".name").hide().fadeIn(2500)
  setTimeout(animateBold, 1000);
}

function animateBold() {
  $(".bold").animate({
    fontSize: "1.4em"
  }, 4000)
}

function pageSwitcher() {
  $("html").load("/Chatbot");
}

$(document).ready(nameFade())
