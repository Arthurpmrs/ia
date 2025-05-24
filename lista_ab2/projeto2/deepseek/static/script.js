document.addEventListener("DOMContentLoaded", function () {
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const chatMessages = document.getElementById("chat-messages");
  const resultContainer = document.getElementById("result-container");
  const resultDecision = document.getElementById("result-decision");
  const resultJustification = document.getElementById("result-justification");
  const resultConfidence = document.getElementById("result-confidence");

  // Exemplo de mensagem inicial do bot
  addBotMessage(
    "Olá! Sou o assistente de RH. Por favor, me forneça informações sobre o candidato: formação, experiência, tecnologias que domina, idiomas e nota da entrevista comportamental."
  );

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });

  async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    addUserMessage(message);
    userInput.value = "";

    // Simular processamento
    addBotMessage("Processando informações...");

    // Extrair informações da mensagem (simplificado - na prática usaria NLP)
    const candidateData = await parseCandidateData(message);

    // Enviar para o backend
    console.log(candidateData);

    fetch("/api/evaluate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(candidateData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Remover a mensagem "Processando..."
        chatMessages.lastChild.remove();

        // Mostrar resultado
        addBotMessage(`Decisão: ${data.decision}. ${data.justification}`);
        showResult(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        addBotMessage(
          "Desculpe, ocorreu um erro ao processar sua solicitação."
        );
      });
  }

  function addUserMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", "user-message");
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function addBotMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", "bot-message");
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function showResult(data) {
    resultContainer.style.display = "block";
    resultDecision.textContent = `Decisão: ${data.decision}`;
    resultDecision.className = "result " + data.decision.replace(" ", "-");
    resultJustification.textContent = `Justificativa: ${data.justification}`;
    resultConfidence.textContent = `Confiança do modelo: ${(
      data.confidence * 100
    ).toFixed(1)}%`;
  }

  async function parseCandidateData(message) {
    try {
      const response = await fetch("/api/extract-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: message }),
      });
      return await response.json();
    } catch (error) {
      console.error("Error:", error);
      return {
        education: "Não informado",
        experience_years: 0,
        technologies: [],
        languages: [],
        behavioral_interview_score: 0,
      };
    }
  }
});


