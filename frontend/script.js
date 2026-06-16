// Elite Foam Insulation — front-end behavior.
// The contact form POSTs to the FastAPI backend, which stores the lead and emails the owner.

// Where the backend lives. Local dev = localhost:8000. On deploy, change this to the
// deployed backend URL (e.g. https://elitefoam-api.onrender.com).
const API_BASE = "http://localhost:8000";

// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("contact-form");
const statusEl = document.getElementById("form-status");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusEl.className = "form-status";
  statusEl.textContent = "";

  const data = {
    name: form.name.value.trim(),
    phone: form.phone.value.trim(),
    email: form.email.value.trim(),
    service: form.service.value,
    message: form.message.value.trim(),
    source: "website",
  };

  // Minimal client-side validation (server validates too).
  if (!data.name) {
    showError("Please enter your name.");
    return;
  }
  if (!data.phone && !data.email) {
    showError("Please leave a phone number or email so we can reach you.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Sending…";

  try {
    const res = await fetch(`${API_BASE}/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error(`Request failed (${res.status})`);

    form.reset();
    statusEl.className = "form-status ok";
    statusEl.textContent = "Thanks! We got your request and will reach out soon.";
  } catch (err) {
    showError("Something went wrong. Please call us at (904) 570-8897.");
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Request My Free Quote";
  }
});

function showError(msg) {
  statusEl.className = "form-status err";
  statusEl.textContent = msg;
}
