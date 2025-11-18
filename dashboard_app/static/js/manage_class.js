const editModal = document.getElementById("editModal");
const closeEditModal = document.getElementById("closeEditModal");
const cancelEdit = document.getElementById("cancelEdit");
const modal = document.getElementById("addClassModal");

const openBtn = document.getElementById("openAddClassModal");
const closeBtn = document.getElementById("closeAddClassModal");
const cancelBtn = document.getElementById("cancelAddClass");

const deleteModal = document.getElementById("deleteModal");
const cancelDelete = document.getElementById("cancelDelete");

cancelDelete.addEventListener("click", () => deleteModal.classList.add("hidden"));
closeEditModal.addEventListener("click", () => editModal.classList.add("hidden"));
cancelEdit.addEventListener("click", () => editModal.classList.add("hidden"));
openBtn.addEventListener("click", () => modal.classList.remove("hidden"));
closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
cancelBtn.addEventListener("click", () => modal.classList.add("hidden"));
modal.addEventListener("click", (e) => { if (e.target === modal) modal.classList.add("hidden");});

deleteModal.addEventListener("click", (e) => { if (e.target === deleteModal) deleteModal.classList.add("hidden");});
editModal.addEventListener("click", (e) => { if (e.target === editModal) editModal.classList.add("hidden");});

document.getElementById("addSchedule").addEventListener("click", () => {
    const container = document.getElementById("scheduleContainer");
    const newRow = container.firstElementChild.cloneNode(true);
    newRow.querySelectorAll("input, select").forEach((el) => (el.value = ""));
    container.appendChild(newRow);
});

document
    .getElementById("scheduleContainer")
    .addEventListener("click", (e) => {
        if (e.target.closest(".remove-schedule")) {
            const row = e.target.closest(".schedule-item");
            const container = document.getElementById("scheduleContainer");
            if (container.children.length > 1) row.remove();
        }
    });

document.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        e.preventDefault();

        document.getElementById("editClassId").value = btn.dataset.id;
        document.getElementById("editCode").value = btn.dataset.code;
        document.getElementById("editTitle").value = btn.dataset.title;
        document.getElementById("editSection").value = btn.dataset.section;
        document.getElementById("editSemester").value = btn.dataset.semester;
        document.getElementById("editYear").value = btn.dataset.year;

        document.getElementById("editClassForm").action = `/dashboard/teacher/manage-classes/${btn.dataset.id}/edit/`;

        editModal.classList.remove("hidden");
    });
});



document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        e.preventDefault();

        document.getElementById("deleteClassId").value = btn.dataset.id;
        document.getElementById("deleteClassName").innerText = `"${btn.dataset.title}"`;

        document.getElementById("deleteClassForm").action = `/dashboard/teacher/manage-classes/${btn.dataset.id}/delete/`;

        deleteModal.classList.remove("hidden");
    });
});
