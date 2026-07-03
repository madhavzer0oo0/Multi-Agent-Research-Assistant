const API_BASE_URL = "http://localhost:8000";

const state = {
  authMode: "login",
  token: localStorage.getItem("research_token") || "",
  email: localStorage.getItem("research_email") || "",
  reports: [],
  selectedReport: null,
};

const elements = {
  authView: document.getElementById("authView"),
  dashboardView: document.getElementById("dashboardView"),
  authForm: document.getElementById("authForm"),
  emailInput: document.getElementById("emailInput"),
  passwordInput: document.getElementById("passwordInput"),
  authSubmitButton: document.getElementById("authSubmitButton"),
  authStatusLine: document.getElementById("authStatusLine"),
  loginTab: document.getElementById("loginTab"),
  registerTab: document.getElementById("registerTab"),
  reportForm: document.getElementById("reportForm"),
  topicInput: document.getElementById("topicInput"),
  maxResultsInput: document.getElementById("maxResultsInput"),
  generateButton: document.getElementById("generateButton"),
  statusLine: document.getElementById("statusLine"),
  reportList: document.getElementById("reportList"),
  reportOutput: document.getElementById("reportOutput"),
  reportTitle: document.getElementById("reportTitle"),
  reportDate: document.getElementById("reportDate"),
  reportContent: document.getElementById("reportContent"),
  accountChip: document.getElementById("accountChip"),
  logoutButton: document.getElementById("logoutButton"),
  refreshReportsButton: document.getElementById("refreshReportsButton"),
  downloadMarkdownButton: document.getElementById("downloadMarkdownButton"),
  printButton: document.getElementById("printButton"),
  deleteReportButton: document.getElementById("deleteReportButton"),
};

function setStatus(message, type = "", target = "dashboard") {
  const element = target === "auth" ? elements.authStatusLine : elements.statusLine;
  element.textContent = message;
  element.className = `status-line ${type}`.trim();
}

function setAuthMode(mode) {
  state.authMode = mode;
  const isLogin = mode === "login";

  elements.loginTab.classList.toggle("active", isLogin);
  elements.registerTab.classList.toggle("active", !isLogin);
  elements.loginTab.setAttribute("aria-selected", String(isLogin));
  elements.registerTab.setAttribute("aria-selected", String(!isLogin));
  elements.authSubmitButton.textContent = isLogin ? "Login" : "Register";
  elements.passwordInput.autocomplete = isLogin ? "current-password" : "new-password";
}

function renderApp() {
  const isAuthenticated = Boolean(state.token);

  elements.authView.classList.toggle("hidden", isAuthenticated);
  elements.dashboardView.classList.toggle("hidden", !isAuthenticated);
  elements.logoutButton.classList.toggle("hidden", !isAuthenticated);
  elements.accountChip.textContent = state.email || "Signed in";

  if (!isAuthenticated) {
    elements.reportList.innerHTML = '<p class="muted">Sign in to load reports.</p>';
    elements.reportOutput.classList.add("hidden");
  }
}

async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers || {});

  if (state.token) {
    headers.set("Authorization", `Bearer ${state.token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  let data = null;
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const message = data?.detail || data || `Request failed with status ${response.status}`;
    throw new Error(Array.isArray(message) ? message.map((item) => item.msg).join(" ") : message);
  }

  return data;
}

async function login(email, password) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  return apiRequest("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
}

async function register(email, password) {
  return apiRequest("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
}

async function loadReports() {
  if (!state.token) return;

  elements.reportList.innerHTML = '<p class="muted">Loading reports...</p>';

  try {
    state.reports = await apiRequest("/reports");
    renderReports();
  } catch (error) {
    elements.reportList.innerHTML = `<p class="muted">${escapeHtml(error.message)}</p>`;
  }
}

function renderReports() {
  if (!state.reports.length) {
    elements.reportList.innerHTML = '<p class="muted">No reports found.</p>';
    return;
  }

  elements.reportList.innerHTML = "";

  state.reports.forEach((report) => {
    const button = document.createElement("button");
    button.className = "report-item";
    button.type = "button";
    button.classList.toggle("active", state.selectedReport?.id === report.id);
    button.innerHTML = `
      <strong>${escapeHtml(report.topic)}</strong>
      <span>${formatDate(report.created_at)}</span>
    `;
    button.addEventListener("click", () => selectReport(report));
    elements.reportList.appendChild(button);
  });
}

function selectReport(report) {
  state.selectedReport = report;
  elements.reportTitle.textContent = report.topic;
  elements.reportDate.textContent = formatDate(report.created_at);
  elements.reportContent.innerHTML = renderMarkdown(report.report);
  elements.reportOutput.classList.remove("hidden");
  renderReports();
}

async function createReport(topic, maxResults) {
  return apiRequest("/reports", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic, max_results: maxResults }),
  });
}

async function deleteSelectedReport() {
  if (!state.selectedReport) return;

  const reportId = state.selectedReport.id;
  await apiRequest(`/reports/${reportId}`, { method: "DELETE" });
  state.reports = state.reports.filter((report) => report.id !== reportId);
  state.selectedReport = null;
  elements.reportOutput.classList.add("hidden");
  renderReports();
}

function logout() {
  localStorage.removeItem("research_token");
  localStorage.removeItem("research_email");
  state.token = "";
  state.email = "";
  state.reports = [];
  state.selectedReport = null;
  setStatus("");
  setStatus("", "", "auth");
  renderApp();
}

function downloadMarkdown() {
  if (!state.selectedReport) return;

  const filename = `${slugify(state.selectedReport.topic)}.md`;
  const blob = new Blob([`# ${state.selectedReport.topic}\n\n${state.selectedReport.report}`], {
    type: "text/markdown;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function renderMarkdown(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let listType = null;

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (!line.trim()) {
      closeList();
      continue;
    }

    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      html.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const unordered = line.match(/^\s*[-*]\s+(.+)$/);
    if (unordered) {
      openList("ul");
      html.push(`<li>${inlineMarkdown(unordered[1])}</li>`);
      continue;
    }

    const ordered = line.match(/^\s*\d+\.\s+(.+)$/);
    if (ordered) {
      openList("ol");
      html.push(`<li>${inlineMarkdown(ordered[1])}</li>`);
      continue;
    }

    closeList();
    html.push(`<p>${inlineMarkdown(line)}</p>`);
  }

  closeList();
  return html.join("");

  function openList(type) {
    if (listType === type) return;
    closeList();
    listType = type;
    html.push(`<${type}>`);
  }

  function closeList() {
    if (!listType) return;
    html.push(`</${listType}>`);
    listType = null;
  }
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, "<code>$1</code>");
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatDate(value) {
  if (!value) return "";

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "report";
}

elements.loginTab.addEventListener("click", () => setAuthMode("login"));
elements.registerTab.addEventListener("click", () => setAuthMode("register"));

elements.authForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = elements.emailInput.value.trim();
  const password = elements.passwordInput.value;
  elements.authSubmitButton.disabled = true;

  try {
    if (state.authMode === "register") {
      await register(email, password);
      setAuthMode("login");
      setStatus("Registration complete. You can sign in now.", "success", "auth");
      elements.passwordInput.value = "";
      return;
    }

    const data = await login(email, password);
    state.token = data.access_token;
    state.email = email;
    localStorage.setItem("research_token", state.token);
    localStorage.setItem("research_email", email);
    elements.passwordInput.value = "";
    setStatus("");
    setStatus("", "", "auth");
    renderApp();
    await loadReports();
  } catch (error) {
    setStatus(error.message, "error", "auth");
  } finally {
    elements.authSubmitButton.disabled = false;
  }
});

elements.reportForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const topic = elements.topicInput.value.trim();
  const maxResults = Number(elements.maxResultsInput.value);

  if (!topic) {
    setStatus("Please enter a research topic.", "error");
    return;
  }

  elements.generateButton.disabled = true;
  setStatus("Generating report...");

  try {
    const data = await createReport(topic, maxResults);
    state.reports = [data.report, ...state.reports.filter((report) => report.id !== data.report.id)];
    selectReport(data.report);
    elements.topicInput.value = "";
    setStatus("Report generated successfully.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    elements.generateButton.disabled = false;
  }
});

elements.logoutButton.addEventListener("click", logout);
elements.refreshReportsButton.addEventListener("click", loadReports);
elements.downloadMarkdownButton.addEventListener("click", downloadMarkdown);
elements.printButton.addEventListener("click", () => window.print());
elements.deleteReportButton.addEventListener("click", async () => {
  elements.deleteReportButton.disabled = true;
  setStatus("Deleting report...");

  try {
    await deleteSelectedReport();
    setStatus("Report deleted.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    elements.deleteReportButton.disabled = false;
  }
});

setAuthMode("login");
renderApp();
loadReports();
