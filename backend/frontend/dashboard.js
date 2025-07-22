// frontend/dashboard.js

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/frontend/index.html";
        return;
    }

    fetchRelatorios(token);
});

async function fetchRelatorios(token) {
    try {
        const res = await fetch("/analisar/relatorios", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error("Erro ao carregar relatórios");

        const data = await res.json();
        renderTable(data.relatorios);

    } catch (error) {
        alert("Erro: " + error.message);
    }
}

function renderTable(relatorios) {
    const tbody = document.querySelector("#relatorios-table tbody");
    tbody.innerHTML = "";

    for (const item of relatorios) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.timestamp}</td>
            <td>${item.cliente}</td>
            <td>${item.account_id}</td>
            <td>${item.servico}</td>
            <td>${item.descricao}</td>
            <td>${item.severidade}</td>
            <td>${item.recomendacao}</td>
        `;

        tbody.appendChild(row);
    }
}
