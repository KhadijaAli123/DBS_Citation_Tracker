const API_BASE = "/api"; // when running dev behind same server; or http://localhost:8000/api

async function createCitation() {
  const payload = {
    title: document.getElementById("title").value,
    authors: document.getElementById("authors").value,
    venue: document.getElementById("venue").value,
    year: parseInt(document.getElementById("year").value) || null,
    doi: document.getElementById("doi").value || null,
    tags: document.getElementById("tags").value || null,
    notes: document.getElementById("notes").value || null
  };
  const res = await fetch(`${API_BASE}/citations/`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById("createResult").innerText = JSON.stringify(data, null, 2);
  loadList();
}

async function loadList(q=null) {
  const qstr = q ? `?q=${encodeURIComponent(q)}` : "";
  const res = await fetch(`${API_BASE}/citations/${qstr}`);
  const data = await res.json();
  const tbody = document.querySelector("#results tbody");
  tbody.innerHTML = "";
  data.forEach(c => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${c.id}</td><td>${c.title}</td><td>${c.authors}</td><td>${c.year || ""}</td>
      <td>
        <button onclick="editCitation(${c.id})">Edit</button>
        <button onclick="deleteCitation(${c.id})">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
}

async function deleteCitation(id) {
  if(!confirm("Delete citation "+id+"?")) return;
  const res = await fetch(`${API_BASE}/citations/${id}`, { method: "DELETE" });
  if (res.ok) {
    loadList();
  } else {
    alert("Delete failed");
  }
}

async function editCitation(id) {
  const res = await fetch(`${API_BASE}/citations/${id}`);
  if (!res.ok) { alert("Not found"); return; }
  const cit = await res.json();
  // simplified — prompt for a new title only (for demo)
  const newTitle = prompt("New title:", cit.title);
  if (newTitle === null) return;
  const update = { title: newTitle };
  const r2 = await fetch(`${API_BASE}/citations/${id}`, {
    method: "PUT",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(update)
  });
  if (r2.ok) loadList();
  else alert("Update failed");
}

async function getSummary() {
  const res = await fetch(`${API_BASE}/report/summary`);
  const data = await res.json();
  document.getElementById("summaryRes").innerText = JSON.stringify(data, null, 2);
}

document.getElementById("createBtn").addEventListener("click", createCitation);
document.getElementById("searchBtn").addEventListener("click", ()=> {
  const q = document.getElementById("q").value;
  loadList(q);
});
document.getElementById("refreshBtn").addEventListener("click", ()=> loadList());
document.getElementById("getSummary").addEventListener("click", getSummary);

// initial load
loadList();
