/*** Pusher Set-Up */
var pusher = new Pusher('d4e5e20b03824cd11efd', {
  cluster: 'us2',
  encrypted: true
});

const channel = pusher.subscribe('ROKbot');

channel.bind('new_message', robotSend)

var sound = false

$(".soundIcon").click(function() {
  if (sound == true) {
    console.log("func1 is called")
    sound = false
    $(this).attr("src","static/css/Images/noSound.png")
  } else {
    console.log("func 2 is called")
    sound = true 
    $(this).attr("src","static/css/Images/sound.png")
  }
})


$(document).ready(function () {
  $(this).scrollTop(0);
});

$("#inputMessage").keypress(function (event) {
  if (event.which == 13) {
    userSend()
    chatScroll()
  }
});

$(".sendButton").click(function () {
  userSend()
  chatScroll()
})

$("#target").submit(function (e) {
  e.preventDefault()
  return false;
})


function userSend() {
  if ($(".input").val() != "") {
    var userInput = $(".input").val();
    submit_message(userInput)
    $(' <div class="userSection"> ' +
      '<div class="userBubble">' +
      '<h5 class="userMessage">' + $(".input").val() + '</h5>' +
      '</div>' +
      '<img class="userIcon" src="static/css/Images/person.png">' +
      '<hr class="chatBreaker">' +
      '</div>').hide().appendTo(".chatMed").fadeIn(1500)
    $(".input").val('')
  }
}

function chatScroll() {
  $('.chatMed').scrollTop($('.chatMed')[0].scrollHeight);
}

function robotSend(data) {
  console.log(sound + " outside")
  if (data.message != undefined) {
    $(' <div class="botSection"> ' + '<img class="botIcon" src="static/css/Images/robot4.png">' +
      '<div class="botBubble">' +
      '<h5 class="botMessage">' + data.message + '</h5>' +
      '</div>' +
      '<hr class="chatBreaker">' +
      '</div>').hide().appendTo(".chatMed").fadeIn(1500)
      var utterance = new SpeechSynthesisUtterance(data.message) 
      console.log(sound === true)
      if (sound === true) {
        console.log("test")
        speechSynthesis.speak(utterance)
      }
      
  }
  chatScroll()
}


/*********** Text to Speech Functions ****************************/

function textSpeech() {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.start();
  $("#inputMessage").val("   Feel free to speak. ROKBot is listening!")
}

var final_transcript = '';
var recognizing = false;
var recognition = new webkitSpeechRecognition();
recognition.onstart = function () {
  recognizing = true;
};

recognition.onresult = function (event) {
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    final_transcript += event.results[i][0].transcript;
    final_transcript = final_transcript.replace("rockbot", 'ROKBot')
    final_transcript = final_transcript.replace("Rock", 'ROK')
    final_transcript = capitalize(final_transcript);
    $("#inputMessage").val(final_transcript)
    $('.sendButton').trigger('click');
    recognizing = false;
    $("#inputMessage").val("")
  }
}

recognition.onend = function() {
  recognizing = false
  console.log(final_transcript)
  if (final_transcript == "") {
    alert("Sorry, your mic didn't catch that. Please check your settings and try again")
  }
  final_transcript = ''
  $("#inputMessage").val("")
}

/** Functions to do line breaks */
var two_line = /\n\n/g;
var one_line = /\n/g;

function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}
var first_char = /\S/;

function capitalize(s) {
  var firstChar = s[0].toUpperCase()
  s = firstChar + s.substr(1)
  return s
}


/*********************MESSAGE PROCESSING WITH DIALOGFLOW *******************************/
//Sends it to the appropriate python page
function submit_message(message) {
  var socketId = pusher.connection.socket_id
  $.post("/send_message", {
    message: message,
    socketId: socketId
  }, robotSend)
}