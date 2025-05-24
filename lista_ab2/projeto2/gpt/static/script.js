async function enviar() {
  const requisitos = document.getElementById("requisitos").value;
  const texto = document.getElementById("input").value;

  const res = await fetch("/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ requisitos, texto })
  });

  const json = await res.json();
  document.getElementById("resposta").innerText = json.resposta;
}
