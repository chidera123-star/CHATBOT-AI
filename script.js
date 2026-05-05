const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const micBtn = document.getElementById("mic-btn");
const voiceToggle = document.getElementById("voice-toggle");

// ---------- Intents ----------
const intents = {
  greeting: {
    patterns: ["hello", "hi", "hey", "good morning", "good afternoon"],
    responses: ["Hello there!", "Hi! How can I assist you today?", "Hey! Nice to see you!"]
  },
  exam: {
    patterns: ["exam", "test", "assessment"],
    responses: ["Exams start next Monday. Please check the official notice for details."]
  },
  timetable: {
    patterns: ["timetable", "schedule", "class timetable"],
    responses: ["You can view the class timetable on the student portal or notice board."]
  },
  fees: {
    patterns: ["fees", "payment", "tuition"],
    responses: ["School fees can be paid online or at the bursary office."]
  },
  location: {
    patterns: ["library", "office", "canteen", "principal", "sports"],
    responses: [
      "The library is on the second floor of the main building.",
      "The principal’s office is next to reception near the main gate."
    ]
  },
  goodbye: {
    patterns: ["bye", "goodbye", "see you", "later"],
    responses: ["Goodbye! Have a great day!", "See you soon!", "Bye for now!"]
  },
  fallback: {
    responses: [
      "I’m not sure I understand. Could you rephrase that?",
      "Sorry, I don’t have that information right now."
    ]
  }
};

// ---------- Chat Logic ----------
function getResponse(msg) {
  msg = msg.toLowerCase();
  for (const intent in intents) {
    const data = intents[intent];
    for (let keyword of data.patterns || []) {
      if (msg.includes(keyword)) {
        const possible = data.responses;
        return possible[Math.floor(Math.random() * possible.length)];
      }
    }
  }
  const fallback = intents["fallback"].responses;
  return fallback[Math.floor(Math.random() * fallback.length)];
}

function appendMessage(sender, message) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add(sender === "user" ? "user-msg" : "bot-msg");
  msgDiv.textContent = message;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function speak(message) {
  if (!voiceToggle.checked) return;
  const utterance = new SpeechSynthesisUtterance(message);
  utterance.lang = "en-US";
  speechSynthesis.speak(utterance);
}

function sendMessage(text = null) {
  const msg = text || userInput.value.trim();
  if (!msg) return;
  appendMessage("user", msg);
  userInput.value = "";
  const botReply = getResponse(msg);
  setTimeout(() => {
    appendMessage("bot", botReply);
    speak(botReply);
  }, 500);
}

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// ---------- Voice Input ----------
let recognition;
if ("webkitSpeechRecognition" in window) {
  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.continuous = false;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    appendMessage("user", transcript);
    const botReply = getResponse(transcript);
    setTimeout(() => {
      appendMessage("bot", botReply);
      speak(botReply);
    }, 400);
  };

  recognition.onerror = () => appendMessage("bot", "Sorry, I didn’t catch that.");

  micBtn.addEventListener("click", () => {
    if (micBtn.classList.contains("active")) {
      recognition.stop();
      micBtn.classList.remove("active");
    } else {
      recognition.start();
      micBtn.classList.add("active");
    }
  });
} else {
  micBtn.style.display = "none";
  console.log("Speech recognition not supported in this browser.");
}
