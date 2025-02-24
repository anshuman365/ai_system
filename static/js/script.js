document.getElementById("send-message").addEventListener("click", () => {
    let userMessage = document.getElementById("chat-box").value;
    
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: userMessage, session_id: localStorage.getItem("session_id")})
    })
    .then(response => response.json())
    .then(data => {
        if (!localStorage.getItem("session_id")) {
            localStorage.setItem("session_id", data.session_id);
        }
        document.getElementById("response-box").innerText = "AI: " + data.response;

        // Read the AI response out loud
        playAudio(data.audio_url);  // Assume audio_url is returned with the response

        // Restart listening after audio ends
        let audio = new Audio(data.audio_url);
        audio.onended = function() {
            recognition.start();  // Restart listening after audio finishes
        };
    });
});

let recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = false;

document.getElementById("start-listening").addEventListener("click", () => {
    recognition.start();  // Start recognizing speech
});

document.getElementById("stop-listening").addEventListener("click", () => {
    recognition.stop();  // Stop listening
});

recognition.onresult = (event) => {
    let text = event.results[event.results.length - 1][0].transcript;
    document.getElementById("chat-box").value = text;
    
    // Send the recognized speech as a message to the backend
    document.getElementById("send-message").click();
};

// Function to play the audio response
function playAudio(audioUrl) {
    let audio = new Audio(audioUrl);
    audio.play();
    audio.onended = function() {
        // Restart listening after AI finishes speaking
        recognition.start();
    };
}