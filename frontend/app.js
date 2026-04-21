document.addEventListener("DOMContentLoaded", () => {

  // ================= ELEMENTS =================
  const createPatientForm = document.getElementById("createPatientForm");
  const appointmentForm = document.getElementById("appointmentForm");

  const patientsTableBody = document.getElementById("patientsTableBody");
  const appointmentsTableBody = document.getElementById("appointmentsTableBody");

  const patientHistoryBody = document.getElementById("patientHistoryBody");
  const selectedPatientLabel = document.getElementById("selectedPatientLabel");

  const message = document.getElementById("message");
  const submitBtn = document.getElementById("submitBtn");

  const searchName = document.getElementById("searchName");

  let editMode = false;
  let editPatientId = null;

  // ================= HELPERS =================

  function getApiBaseUrl() {
    return "http://127.0.0.1:8000";
  }

  function showMessage(msg, isError = false) {
    message.textContent = msg;
    message.style.color = isError ? "red" : "green";
  }

  async function api(path, options = {}) {
    const res = await fetch(`${getApiBaseUrl()}${path}`, options);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) throw new Error(data.detail || "Request failed");

    return data;
  }

  function applyFilters(patients) {
    const name = searchName.value.toLowerCase();

    return patients.filter(p =>
      p.first_name.toLowerCase().includes(name) ||
      p.last_name.toLowerCase().includes(name)
    );
  }

  // ================= PATIENTS =================

  async function loadPatients() {
    try {
      const data = await api("/patients/");
      const filtered = applyFilters(data);

      patientsTableBody.innerHTML = "";

      if (filtered.length === 0) {
        patientsTableBody.innerHTML = `<tr><td colspan="6">No patients</td></tr>`;
        return;
      }

      filtered.forEach(p => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${p.id}</td>
          <td>${p.first_name}</td>
          <td>${p.last_name}</td>
          <td>${p.age}</td>
          <td>${p.gender}</td>
          <td>
            <button data-action="edit" data-id="${p.id}">Edit</button>
            <button data-action="delete" data-id="${p.id}">Delete</button>
          </td>
        `;

        patientsTableBody.appendChild(row);
      });

    } catch (err) {
      showMessage(err.message, true);
    }
  }

  // CREATE / UPDATE PATIENT
  createPatientForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      first_name: firstName.value,
      last_name: lastName.value,
      age: Number(age.value),
      gender: gender.value
    };

    try {
      if (editMode) {
        await api(`/patients/${editPatientId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        showMessage("Patient updated");
      } else {
        await api("/patients/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        showMessage("Patient created");
      }

      createPatientForm.reset();
      editMode = false;
      submitBtn.textContent = "Create Patient";

      await loadPatients();

    } catch (err) {
      showMessage(err.message, true);
    }
  });

  // EDIT / DELETE + HISTORY
  patientsTableBody.addEventListener("click", async (e) => {
    const btn = e.target.closest("button");
    const row = e.target.closest("tr");
    if (!row) return;

    const id = row.children[0].textContent;

    if (!btn) {
      loadPatientHistory(id);
      return;
    }

    const action = btn.dataset.action;

    if (action === "edit") {
      firstName.value = row.children[1].textContent;
      lastName.value = row.children[2].textContent;
      age.value = row.children[3].textContent;
      gender.value = row.children[4].textContent;

      editMode = true;
      editPatientId = id;
      submitBtn.textContent = "Update Patient";
    }

    if (action === "delete") {
      await api(`/patients/${id}`, { method: "DELETE" });
      await loadPatients();
    }
  });

  // SEARCH
  searchName.addEventListener("input", loadPatients);

  // ================= HISTORY =================

  async function loadPatientHistory(patientId) {
    const data = await api(`/appointments/patient/${patientId}`);

    patientHistoryBody.innerHTML = "";
    selectedPatientLabel.textContent = `History for Patient ID: ${patientId}`;

    if (data.length === 0) {
      patientHistoryBody.innerHTML = `<tr><td colspan="4">No history</td></tr>`;
      return;
    }

    data.forEach(a => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${a.id}</td>
        <td>${a.doctor_name}</td>
        <td>${a.date_time}</td>
        <td>${a.status}</td>
      `;

      patientHistoryBody.appendChild(row);
    });
  }

  // ================= APPOINTMENTS =================

  appointmentForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      patient_id: Number(patientId.value),
      doctor_name: doctorName.value,
      date_time: dateTime.value
    };

    await api("/appointments/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    appointmentForm.reset();
    await loadAppointments();
  });

  async function loadAppointments() {
    const data = await api("/appointments/");
    appointmentsTableBody.innerHTML = "";

    data.forEach(a => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${a.id}</td>
        <td>${a.patient_id}</td>
        <td>${a.doctor_name}</td>
        <td>${a.date_time}</td>
        <td>
          <select data-id="${a.id}" class="statusDropdown">
            <option value="scheduled" ${a.status === "scheduled" ? "selected" : ""}>Scheduled</option>
            <option value="completed" ${a.status === "completed" ? "selected" : ""}>Completed</option>
            <option value="cancelled" ${a.status === "cancelled" ? "selected" : ""}>Cancelled</option>
          </select>
        </td>
      `;

      appointmentsTableBody.appendChild(row);
    });
  }

  // STATUS UPDATE
  appointmentsTableBody.addEventListener("change", async (e) => {
    if (!e.target.classList.contains("statusDropdown")) return;

    const id = e.target.dataset.id;
    const status = e.target.value;

    await api(`/appointments/${id}?status=${status}`, {
      method: "PATCH"
    });

    await loadAppointments();
  });

  // ================= INIT =================

  loadPatients();
  loadAppointments();
});