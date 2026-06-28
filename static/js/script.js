async function askAI() {

    const prompt = document.getElementById("prompt").value;

    if(prompt.trim()=="") return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<p><b>You:</b> ${prompt}</p>`;

    const response = await fetch("/ask-ai",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            prompt:prompt
        })

    });
    const data = await response.json();
    console.log(data);

    chatBox.innerHTML += `<p><b>CyberMind AI:</b> ${data.response}</p>`;

    document.getElementById("prompt").value="";
}
async function generateQuiz() {

    const container = document.getElementById("quiz-container");

    container.innerHTML = "Generating AI Quiz... 🤖";

    const response = await fetch("/generate-quiz", {
        method: "POST"
    });

    const data = await response.json();

    let quizText = data.quiz;

    let quiz;

    try {
        quiz = JSON.parse(quizText);
    } catch (e) {
        container.innerHTML = "Error parsing AI response 😢";
        return;
    }

    container.innerHTML = "";

    quiz.forEach((q, index) => {

        let div = document.createElement("div");

        div.innerHTML = `
            <h3>${index + 1}. ${q.question}</h3>
            <p>Answer: ${q.answer}</p>
            <hr>
        `;

        container.appendChild(div);
    });
}
async function analyzePhishing(){

    const text=document.getElementById("phishing-input").value;

    if(text.trim()=="") return;

    const result=document.getElementById("phishing-result");

    result.innerHTML="Analyzing... 🤖";

    const response=await fetch("/analyze-phishing",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            text:text
        })

    });

    const data=await response.json();

    result.innerHTML=`<pre>${data.response}</pre>`;
}