document.addEventListener('DOMContentLoaded', () => {
    initializeTeacherActions();
});

function initializeTeacherActions() {
    // Structural Modal Target Elements
    const modal = document.getElementById('assignmentModal');
    const form = document.getElementById('assignmentForm');
    const modalTitle = document.getElementById('modalTitleDisplay');
    const submitBtn = document.getElementById('submitBtnText');
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Form inputs field mapping elements
    const fieldTitle = document.getElementById('title');
    const fieldDesc = document.getElementById('description');
    const fieldGrade = document.getElementById('gradeMax');
    const fieldHidden = document.getElementById('isHidden');
    const fieldType = document.getElementById('assignmentType');

    if (!modal || !form) return;

    // --- 1. Intercept "+ Add Assignment" button clicks ---
    document.querySelectorAll('.action-trigger-create').forEach(button => {
        button.addEventListener('click', (event) => {
            // Stops event bubbling from triggering home.js's accordion click handler
            event.stopPropagation();
            
            form.reset();
            const groupId = button.getAttribute('data-group-id');
            const groupTitle = button.getAttribute('data-group-title');

            form.action = `/assignment-group/${groupId}/assignment/create/`;
            modalTitle.innerHTML = `Create Assignment inside <span style="color:#3498db;">${escapeHTML(groupTitle)}</span>`;
            submitBtn.innerText = "Create Assignment";
            
            modal.style.display = "block";
        });
    });

    // --- 2. Intercept "Edit" button clicks ---
    document.querySelectorAll('.action-trigger-edit').forEach(button => {
        button.addEventListener('click', (event) => {
            // Defensive separation block 
            event.stopPropagation();
            form.reset();

            const id = button.getAttribute('data-id');
            const title = button.getAttribute('data-title');
            const description = button.getAttribute('data-description');
            const isHidden = button.getAttribute('data-hidden') === "true";
            const gradeMax = button.getAttribute('data-grademax');
            const type = button.getAttribute('data-type');

            // Form structural mapping state value mutations
            fieldTitle.value = title;
            fieldDesc.value = description;
            fieldGrade.value = gradeMax;
            fieldHidden.checked = isHidden;
            fieldType.value = type;

            form.action = `/assignment/${id}/edit/`;
            modalTitle.innerHTML = `Edit Assignment: <span style="color:#f39c12;">${escapeHTML(title)}</span>`;
            submitBtn.innerText = "Save Changes";
            
            modal.style.display = "block";
        });
    });

    // --- 3. Modal close bindings ---
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            modal.style.display = "none";
        });
    }

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
}

// Quick helper helper function to secure text rendered into innerHTML spaces dynamically
function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}