```javascript
const palpites = [
  { texto: "Palpite grátis: Ponte Preta x Novorizontino – Vitória da Ponte", tipo: "gratis"},
  { texto: "Palpite VIP 1: Chapecoense x Mirassol – Menos de 2.5 gols", tipo: "pago"},
  { texto: "Palpite VIP 2: Botafogo-SP x Ituano – Empate", tipo: "pago"}
];

const lista = document.getElementById("lista-palpites");
const pagamento = document.getElementById("pagamento");

palpites.forEach(p => {
  const item = document.createElement("li");
  item.innerHTML = p.tipo === "gratis"
? p.texto
: `<strong>Palpite VIP:</strong> <em>bloqueado – desbloqueie com 199MT</em>`;
  lista.appendChild(item);
});

pagamento.innerHTML = `
  <h3>Desbloqueie os palpites VIP</h3>
  <p>Envie 199MT via M-Pesa para <strong>+258 8523 19663</strong></p>
  <p>Depois envie o comprovativo para <a href="https://wa.me/258852319663" target="_blank">WhatsApp</a></p>
`;
```