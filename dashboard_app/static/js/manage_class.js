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
    // Clear error
    newRow.querySelector('.schedule-error').classList.add('hidden');
    newRow.querySelector('.schedule-error').textContent = '';
    container.appendChild(newRow);
    const sel = newRow.querySelector('select[name="days[]"]');
    if (sel) sel.addEventListener('change', updateDayOptions);
    updateDayOptions();
});

document
    .getElementById("scheduleContainer")
    .addEventListener("click", (e) => {
        if (e.target.closest(".remove-schedule")) {
            const row = e.target.closest(".schedule-item");
            const container = document.getElementById("scheduleContainer");
            if (container.children.length > 1) row.remove();
            updateDayOptions();
        }
    });

function updateDayOptions(){
    const selects = Array.from(document.querySelectorAll('select[name="days[]"]'));
    const selected = selects.map(s => s.value).filter(v => v);
    selects.forEach(s => {
        const current = s.value;
        Array.from(s.options).forEach(opt => {
            if (!opt.value) { opt.disabled = false; return; }
            if (opt.value === current) {
                opt.disabled = false;
            } else if (selected.includes(opt.value)) {
                opt.disabled = true;
            } else {
                opt.disabled = false;
            }
        });
    });

    const addBtn = document.getElementById('addSchedule');
    const meetingDaysCount = document.querySelectorAll('select[name="days[]"] option').length - 1; 
    if (selected.length >= meetingDaysCount) {
        addBtn.disabled = true;
        addBtn.classList.add('opacity-40','cursor-not-allowed');
    } else {
        addBtn.disabled = false;
        addBtn.classList.remove('opacity-40','cursor-not-allowed');
    }
}

document.querySelectorAll('select[name="days[]"]').forEach(s => s.addEventListener('change', updateDayOptions));
updateDayOptions();

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

// Validation functions
function validateCode() {
    const codeEl = document.getElementById("code");
    const errorEl = document.getElementById("code-error");
    const code = codeEl.value.trim().toUpperCase();
    let errors = [];

    if (code) {
        if (code.length < 5 || code.length > 10) {
            errors.push("Class code must be between 5 and 10 characters.");
        }
        if (!/[a-zA-Z]/.test(code) || !/\d/.test(code)) {
            errors.push("Class code must contain at least one letter and one number.");
        }
        if (!/^[A-Z0-9_]+$/.test(code)) {
            errors.push("Class code can only contain letters, numbers, and underscores.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateTitle() {
    const titleEl = document.getElementById("title");
    const errorEl = document.getElementById("title-error");
    const title = titleEl.value.trim();
    let errors = [];

    if (title) {
        const cleanTitle = title.replace(/\s+/g, ' ');
        if (cleanTitle.length < 4) {
            errors.push("Class title must be at least 4 characters long.");
        }
        if (!/^[a-zA-Z0-9\s\.,!?\'"-]+$/.test(cleanTitle)) {
            errors.push("Class title can only contain letters, numbers, spaces, and basic punctuation.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateSection() {
    const sectionEl = document.getElementById("section");
    const errorEl = document.getElementById("section-error");
    const section = sectionEl.value.trim();
    let errors = [];

    if (section) {
        if (section.includes(' ')) {
            errors.push("Section cannot contain spaces.");
        }
        if (section.length > 3) {
            errors.push("Section must be at most 3 characters.");
        }
        if (!/^[a-zA-Z0-9]+$/.test(section)) {
            errors.push("Section must be alphanumeric.");
        }
        const letterCount = (section.match(/[a-zA-Z]/g) || []).length;
        const numberCount = (section.match(/\d/g) || []).length;
        if (letterCount !== 1 || numberCount < 1) {
            errors.push("Section must contain exactly one letter and at least one number.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateAcademicYear() {
    const academicYearEl = document.getElementById("academic_year");
    const errorEl = document.getElementById("academic_year-error");
    const academic_year = academicYearEl.value.trim();
    let errors = [];

    if (academic_year) {
        if (!/^\d{4}[-–]\d{4}$/.test(academic_year)) {
            errors.push("Academic year must be in the format YYYY-YYYY or YYYY–YYYY.");
        } else {
            const years = academic_year.replace('–', '-').split('-');
            const year1 = parseInt(years[0]);
            const year2 = parseInt(years[1]);
            if (year1 >= year2) {
                errors.push("First year must be less than the second year.");
            }
            const currentYear = new Date().getFullYear();
            if (year1 < currentYear - 1 || year1 > currentYear + 5) {
                errors.push("Academic year must be current or future (within 5 years).");
            }
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

// Event listeners for validation on blur (when user finishes typing)
document.getElementById("code").addEventListener("blur", validateCode);

document.getElementById("title").addEventListener("blur", validateTitle);

document.getElementById("section").addEventListener("blur", validateSection);

document.getElementById("academic_year").addEventListener("blur", validateAcademicYear);

// Client-side validation for add class form on submit
document.getElementById("addClassForm").addEventListener("submit", function(e) {
    // Run all validations
    validateCode();
    validateTitle();
    validateSection();
    validateAcademicYear();

    // Validate all schedule items
    const scheduleItems = document.querySelectorAll('.schedule-item');
    scheduleItems.forEach(item => validateScheduleItem(item));

    // Check if any errors are visible
    const hasErrors = Array.from(document.querySelectorAll('.text-red-500')).some(el => !el.classList.contains('hidden'));

    if (hasErrors) {
        e.preventDefault();
    }
});

// Validation for schedule items
function validateScheduleItem(item) {
    const day = item.querySelector('select[name="days[]"]').value;
    const start = item.querySelector('input[name="start_times[]"]').value;
    const end = item.querySelector('input[name="end_times[]"]').value;
    const errorEl = item.querySelector('.schedule-error');
    let errors = [];

    if (!day) {
        errors.push("Day is required.");
    }
    if (!start) {
        errors.push("Start time is required.");
    }
    if (!end) {
        errors.push("End time is required.");
    }
    if (start && end && start >= end) {
        errors.push("Start time must be before end time.");
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

// Event listeners for schedule validation
document.getElementById("scheduleContainer").addEventListener("blur", function(e) {
    if (e.target.matches('input[name="start_times[]"], input[name="end_times[]"], select[name="days[]"]')) {
        const item = e.target.closest('.schedule-item');
        validateScheduleItem(item);
    }
});

// Validation functions for edit form
function validateEditCode() {
    const codeEl = document.getElementById("editCode");
    const errorEl = document.getElementById("editCode-error");
    const code = codeEl.value.trim().toUpperCase();
    let errors = [];

    if (code) {
        if (code.length < 5 || code.length > 10) {
            errors.push("Class code must be between 5 and 10 characters.");
        }
        if (!/[a-zA-Z]/.test(code) || !/\d/.test(code)) {
            errors.push("Class code must contain at least one letter and one number.");
        }
        if (!/^[A-Z0-9_]+$/.test(code)) {
            errors.push("Class code can only contain letters, numbers, and underscores.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateEditTitle() {
    const titleEl = document.getElementById("editTitle");
    const errorEl = document.getElementById("editTitle-error");
    const title = titleEl.value.trim();
    let errors = [];

    if (title) {
        const cleanTitle = title.replace(/\s+/g, ' ');
        if (cleanTitle.length < 4) {
            errors.push("Class title must be at least 4 characters long.");
        }
        if (!/^[a-zA-Z0-9\s\.,!?\'"-]+$/.test(cleanTitle)) {
            errors.push("Class title can only contain letters, numbers, spaces, and basic punctuation.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateEditSection() {
    const sectionEl = document.getElementById("editSection");
    const errorEl = document.getElementById("editSection-error");
    const section = sectionEl.value.trim();
    let errors = [];

    if (section) {
        if (section.includes(' ')) {
            errors.push("Section cannot contain spaces.");
        }
        if (section.length > 3) {
            errors.push("Section must be at most 3 characters.");
        }
        if (!/^[a-zA-Z0-9]+$/.test(section)) {
            errors.push("Section must be alphanumeric.");
        }
        const letterCount = (section.match(/[a-zA-Z]/g) || []).length;
        const numberCount = (section.match(/\d/g) || []).length;
        if (letterCount !== 1 || numberCount < 1) {
            errors.push("Section must contain exactly one letter and at least one number.");
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

function validateEditAcademicYear() {
    const academicYearEl = document.getElementById("editYear");
    const errorEl = document.getElementById("editYear-error");
    const academic_year = academicYearEl.value.trim();
    let errors = [];

    if (academic_year) {
        if (!/^\d{4}[-–]\d{4}$/.test(academic_year)) {
            errors.push("Academic year must be in the format YYYY-YYYY or YYYY–YYYY.");
        } else {
            const years = academic_year.replace('–', '-').split('-');
            const year1 = parseInt(years[0]);
            const year2 = parseInt(years[1]);
            if (year1 >= year2) {
                errors.push("First year must be less than the second year.");
            }
            const currentYear = new Date().getFullYear();
            if (year1 < currentYear - 1 || year1 > currentYear + 5) {
                errors.push("Academic year must be current or future (within 5 years).");
            }
        }
    }

    if (errors.length > 0) {
        errorEl.textContent = errors.join('\n');
        errorEl.classList.remove('hidden');
    } else {
        errorEl.classList.add('hidden');
    }
}

// Event listeners for edit form validation
document.getElementById("editCode").addEventListener("blur", validateEditCode);
document.getElementById("editTitle").addEventListener("blur", validateEditTitle);
document.getElementById("editSection").addEventListener("blur", validateEditSection);
document.getElementById("editYear").addEventListener("blur", validateEditAcademicYear);

// Edit form submit validation
document.getElementById("editClassForm").addEventListener("submit", function(e) {
    validateEditCode();
    validateEditTitle();
    validateEditSection();
    validateEditAcademicYear();

    const hasErrors = Array.from(document.querySelectorAll('#editModal .text-red-500')).some(el => !el.classList.contains('hidden'));

    if (hasErrors) {
        e.preventDefault();
    }
});

// Auto-uppercase code and section on input
document.getElementById("code").addEventListener("input", function() {
    this.value = this.value.toUpperCase();
});

document.getElementById("section").addEventListener("input", function() {
    this.value = this.value.toUpperCase();
});

document.getElementById("editCode").addEventListener("input", function() {
    this.value = this.value.toUpperCase();
});

document.getElementById("editSection").addEventListener("input", function() {
    this.value = this.value.toUpperCase();
});
