const apiInput = document.querySelector("#apiBaseUrl");
const form = document.querySelector("#userForm");
const nameInput = document.querySelector("#name");
const emailInput = document.querySelector("#email");
const submitButton = document.querySelector("#submitButton");
const refreshButton = document.querySelector("#refreshButton");
const formMessage = document.querySelector("#formMessage");
const usersTable = document.querySelector("#usersTable");
const usersCount = document.querySelector("#usersCount");
const emptyState = document.querySelector("#emptyState");

const defaultApiUrl = "http://localhost:5000";
const savedApiUrl = localStorage.getItem("apiBaseUrl");

apiInput.value = savedApiUrl || defaultApiUrl;

function getApiUrl() {
  return apiInput.value.trim().replace(/\/$/, "") || defaultApiUrl;
}

function setMessage(text, type = "") {
  formMessage.textContent = text;
  formMessage.className = `message ${type}`.trim();
}

function formatDate(value) {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}

function resetEmptyState() {
  emptyState.querySelector("strong").textContent = "Nenhum usuário cadastrado ainda.";
  emptyState.querySelector("span").textContent = "Quando um cadastro for feito, ele aparece aqui.";
}

function renderUsers(users) {
  resetEmptyState();
  usersTable.innerHTML = "";
  emptyState.hidden = users.length > 0;
  usersCount.textContent =
    users.length === 1 ? "1 registro encontrado" : `${users.length} registros encontrados`;

  for (const user of users) {
    const row = document.createElement("tr");
    const name = document.createElement("td");
    const email = document.createElement("td");
    const createdAt = document.createElement("td");

    name.textContent = user.name;
    email.textContent = user.email;
    createdAt.textContent = formatDate(user.created_at);

    row.append(name, email, createdAt);
    usersTable.appendChild(row);
  }
}

async function loadUsers() {
  refreshButton.disabled = true;
  usersCount.textContent = "Carregando registros...";

  try {
    const response = await fetch(`${getApiUrl()}/users`);

    if (!response.ok) {
      throw new Error("Não foi possível carregar a lista de usuários.");
    }

    const users = await response.json();
    renderUsers(users);
  } catch (error) {
    usersTable.innerHTML = "";
    emptyState.hidden = false;
    emptyState.querySelector("strong").textContent = "Não foi possível acessar a API.";
    emptyState.querySelector("span").textContent =
      "Confira se a API está rodando e se a URL acima está correta.";
    usersCount.textContent = "Erro ao carregar";
  } finally {
    refreshButton.disabled = false;
  }
}

async function createUser(event) {
  event.preventDefault();
  submitButton.disabled = true;
  setMessage("Enviando cadastro...");

  try {
    const response = await fetch(`${getApiUrl()}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: nameInput.value,
        email: emailInput.value,
      }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || "Não foi possível cadastrar o usuário.");
    }

    form.reset();
    setMessage("Usuário cadastrado com sucesso.", "success");
    await loadUsers();
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
}

apiInput.addEventListener("change", () => {
  localStorage.setItem("apiBaseUrl", getApiUrl());
  loadUsers();
});

refreshButton.addEventListener("click", loadUsers);
form.addEventListener("submit", createUser);

loadUsers();
