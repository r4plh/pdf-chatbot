function uploadPDF() {
    const fileInput = document.getElementById("pdf-upload");
    const file = fileInput.files[0];
    const uploadStatus = document.getElementById("upload-status");

    if (!file) {
        uploadStatus.textContent = "Please select a PDF file.";
        return;
    }

    const formData = new FormData();
    formData.append("pdf", file);

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            uploadStatus.textContent = data.message;

            // Enable chat interface on successful upload
            if (data.message.includes("successfully")) {
                document.getElementById("user-input").disabled = false;
                document.querySelector(".input-container button").disabled = false;
            }
        })
        .catch(() => {
            uploadStatus.textContent = "Failed to upload PDF.";
        });
}

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const query = userInput.value.trim();
    if (!query) return;

    // Display user message
    const messages = document.getElementById("messages");
    const userMessage = document.createElement("div");
    userMessage.textContent = "You: " + query;
    messages.appendChild(userMessage);

    // Clear input
    userInput.value = "";

    // Send query to server
    fetch("/get_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
    })
        .then((response) => response.json())
        .then((data) => {
            const botMessage = document.createElement("div");
            botMessage.textContent = "Bot: " + data.answer;
            messages.appendChild(botMessage);

            // Scroll to the bottom
            messages.scrollTop = messages.scrollHeight;
        });
}