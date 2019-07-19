/*** Pusher Set-Up */
var pusher = new Pusher('d4e5e20b03824cd11efd', {
  cluster: 'us2',
  encrypted: true
});
const channel = pusher.subscribe('ROKbot');
channel.bind('new_message', robotSend)

//Text-to-Speech Set-Up
var sound = false
$(".soundIcon").click(function() {
  if (sound == true) {
    sound = false
    $(this).attr("src","static/css/Images/noSound.png")
  } else {
    sound = true 
    $(this).attr("src","static/css/Images/sound.png")
  }
})


$(document).ready(function () {
  $(this).scrollTop(0);
});

//Allows for user input submission
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

//Create global variable to save user input
var userMessage = ""
//Create global filter list to pass to backend
var filterList = new Array;
function userSend() {
  if ($(".input").val() != "") {
    var userInput = $(".input").val();
    //Saving the user message as a global variable
    window.userMessage = userInput
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

//setting up flag value to decide to send data
var flag = false
var keywordFlag = false
function robotSend(data) {
  if (data.message != undefined) {
    $(' <div class="botSection"> ' + '<img class="botIcon" src="static/css/Images/robot4.png">' +
      '<div class="botBubble">' +
      '<h5 class="botMessage">' + data.message + '</h5>' +
      '</div>' +
      '<hr class="chatBreaker">' +
      '</div>').hide().appendTo(".chatMed").fadeIn(1500)
      var utterance = new SpeechSynthesisUtterance(data.message) 
      if (sound === true) {
        speechSynthesis.speak(utterance)
      }
    }
    if (window.keywordFlag == true) {
      console.log("keyword has been activated")
      window.filterList.push(window.userMessage)
    }

    if (window.flag == true) {
      window.filterList.push(window.userMessage)
      console.log(window.filterList.toString())
    }

    if ((data.message != undefined) && data.message.includes("What kind of filter are you looking to apply?")) {
      window.flag = true
    }

    if ((data.message != undefined) && data.message.includes("I can help you search for")) {
      window.filterList.push(window.userMessage)
    }

    if ((data.message != undefined) && data.message.includes("Sounds good to me.")) {
      nextPage()
    }

    console.log(window.filterList.toString())
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
  })
}

function nextPage() {
  $.post("/filter_process", {
    filterList: window.filterList.toString()
  })
} 