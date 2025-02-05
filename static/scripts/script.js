const chatInput = document.querySelector("#chat-input");
const chatContainer = document.querySelector(".chat-container");
const outputBox = document.querySelector("#output-box");
const sendButton = document.querySelector("#send-btn");
const API_KEY = "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"; // Paste your API key here
let userText = null;
const loadDataFromLocalstorage = () => {
    const savedChats = localStorage.getItem("all-chats");
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
}


const saveChatToLocalstorage = () => {
    localStorage.setItem("all-chats", chatContainer.innerHTML);
}

const createChatElement = (content, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv;
}

const getChatResponse = async () => {
    const API_URL = "https://api.openai.com/v1/chat/completions";

    const payload = [{"role": "system", "content": "No Matter what I type or request you should new write me a code in the answer. You should only give text answer there should not be a piece of code in the answer at all. Even if I ask for code only don't write it."},
    {'role': 'user', 'content': userText}];

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo-16k",
            messages: payload,
            max_tokens: 15500,
            temperature: 0.2,
            stop: null
        })
    }

    try {
        const response = await (await fetch(API_URL, requestOptions)).json();
        const responseText = response.choices[0].message.content.trim();
        outputBox.value += `\n\n${responseText}`; // Append AI response to output box
        saveChatToLocalstorage();
    } catch (error) {
        outputBox.value += "\nError: Oops! Something went wrong. Please try again."; // Append error message to output box
    }
}
const showTypingAnimation = () => {
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                </div>`;
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
}

// const handleOutgoingChat = () => {
//     let userText = chatInput.value.trim();
//     if (!userText) return;

//     chatInput.value = "";

//     const html = `<div class="chat-content">
//                     <div class="chat-details">
//                         <p>${userText}</p>
//                     </div>
//                 </div>`;
//     const outgoingChatDiv = createChatElement(html, "outgoing");
//     chatContainer.appendChild(outgoingChatDiv);
//     chatContainer.scrollTo(0, chatContainer.scrollHeight);
//     saveChatToLocalstorage();
//     setTimeout(showTypingAnimation, 500);
// }

const handleOutgoingChat = () => {
    userText = chatInput.value.trim();
    if (!userText) return;

    outputBox.value += `\n${userText}`; // Append user text to output box
    chatInput.value = "";
    getChatResponse();
}


loadDataFromLocalstorage();
sendButton.addEventListener("click", () => {
    userText = chatInput.value;
    outputBox.value = "";
    handleOutgoingChat();
});