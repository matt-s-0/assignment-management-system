document.addEventListener('DOMContentLoaded', () => {
    initializeAssignmentModals();
    initializeAssignmentGroupModals();
});

function initializeAssignmentModals() {

    const modal = document.getElementById('assignmentModal');
    const form = document.getElementById('assignmentForm');
    const modalTitle = document.getElementById('modalTitleDisplay');
    const submitBtn = document.getElementById('submitBtnText');
    const closeBtn = document.getElementById('closeAssignmentModalBtn');

    const fieldTitle = document.getElementById('title');
    const fieldDesc = document.getElementById('description');
    const fieldGrade = document.getElementById('gradeMax');
    const fieldHidden = document.getElementById('isHidden');
    const fieldType = document.getElementById('assignmentType');

    if (!modal || !form) return;

    document.querySelectorAll('.action-trigger-create').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            form.reset();
            const groupId = button.getAttribute('data-group-id');
            const groupTitle = button.getAttribute('data-group-title');

            form.action = `/assignment-group/${groupId}/assignment/create/`;
            if (modalTitle) modalTitle.innerHTML = `Create Assignment inside <span style="color:#3498db;">${escapeHTML(groupTitle)}</span>`;
            if (submitBtn) submitBtn.innerText = "Create Assignment";
            modal.style.display = "block";
        });
    });

    document.querySelectorAll('.action-trigger-edit').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            form.reset();

            const id = button.getAttribute('data-id');
            const title = button.getAttribute('data-title');
            const description = button.getAttribute('data-description');
            const isHidden = button.getAttribute('data-hidden') === "true";
            const gradeMax = button.getAttribute('data-grademax');
            const type = button.getAttribute('data-type');

            if (fieldTitle) fieldTitle.value = title || '';
            if (fieldDesc) fieldDesc.value = description || '';
            if (fieldGrade) fieldGrade.value = gradeMax || '';
            if (fieldHidden) fieldHidden.checked = isHidden;
            if (fieldType) fieldType.value = type || 'submittable';

            form.action = `/assignment/${id}/edit/`;
            if (modalTitle) modalTitle.innerHTML = `Edit Assignment: <span style="color:#f39c12;">${escapeHTML(title)}</span>`;
            if (submitBtn) submitBtn.innerText = "Save Changes";
            modal.style.display = "block";
        });
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.style.display = "none");
    }
}

function initializeAssignmentGroupModals() {

    const modal = document.getElementById('assignmentGroupModal');
    const form = document.getElementById('createAssignGroupForm');
    
    const modalTitle = document.getElementById('groupModalTitleDisplay');
    const submitBtn = document.getElementById('groupSubmitBtnText');
    const closeBtn = document.getElementById('closeAssignmentGroupModalBtn');

    const fieldTitle = document.getElementById('id_title');
    const fieldSubtitle = document.getElementById('id_subtitle');

    if (!modal || !form) return;

    // --- CREATE ---
    document.querySelectorAll('.group-trigger-create').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            form.reset();
            
            const mainGroupId = button.getAttribute('data-main-group-id'); 

            form.action = `/group/${mainGroupId}/assignment-group/create/`;
            
            if (modalTitle) modalTitle.innerHTML = 'Create Assignment Group';
            if (submitBtn) submitBtn.innerText = "Create Assignment Group";
            modal.style.display = "block";
        });
    });

    // --- EDIT ---
    document.querySelectorAll('.group-trigger-edit').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            form.reset();

            const id = button.getAttribute('data-id');
            const title = button.getAttribute('data-title');
            const subtitle = button.getAttribute('data-subtitle');

            if (fieldTitle) fieldTitle.value = title || '';
            if (fieldSubtitle) fieldSubtitle.value = subtitle || '';

            form.action = `/assignment-group/${id}/edit/`; 
            
            if (modalTitle) modalTitle.innerHTML = `Edit Assignment Group: <span style="color:#f39c12;">${escapeHTML(title)}</span>`;
            if (submitBtn) submitBtn.innerText = "Save Changes";
            modal.style.display = "block";
        });
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.style.display = "none");
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}