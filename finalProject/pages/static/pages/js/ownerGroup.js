document.addEventListener('DOMContentLoaded', () => {
    initializeAssignmentModals();
    initializeGroupModal();
});

// --- ASSIGNMENT MODAL HANDLING LOGIC ---
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
            modalTitle.innerHTML = `Create Assignment inside <span style="color:#3498db;">${escapeHTML(groupTitle)}</span>`;
            submitBtn.innerText = "Create Assignment";
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

    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.style.display = "none");
    }
}

// --- DYNAMIC PILL/CHIP FUNCTION ENGINE ---
function createChipInputManager(wrapperId, inputId, hiddenFieldId) {
    const wrapper = document.getElementById(wrapperId);
    const input = document.getElementById(inputId);
    const hiddenInput = document.getElementById(hiddenFieldId);
    let chipsList = [];

    if (!wrapper || !input || !hiddenInput) return null;

    // Direct cursor focus window target whenever background wrapper is clicked
    wrapper.addEventListener('click', () => input.focus());

    function syncHiddenField() {
        hiddenInput.value = chipsList.join(', ');
    }

    function removeChip(val) {
        chipsList = chipsList.filter(item => item !== val);
        renderChips();
        syncHiddenField();
    }

    function renderChips() {
        // Clear out existing chip structures safely without purging our main keyboard entry node
        wrapper.querySelectorAll('.mail-chip').forEach(chip => chip.remove());

        chipsList.forEach(value => {
            const chipNode = document.createElement('span');
            chipNode.className = 'mail-chip';
            chipNode.innerText = value;

            const closeAction = document.createElement('span');
            closeAction.className = 'chip-close';
            closeAction.innerHTML = '&times;';
            closeAction.addEventListener('click', (e) => {
                e.stopPropagation(); // Avoid triggering parent wrapper focus
                removeChip(value);
            });

            chipNode.appendChild(closeAction);
            wrapper.insertBefore(chipNode, input);
        });
    }

    function addChipFromInput() {
        let textVal = input.value.trim().replace(/,/g, '');
        if (textVal && !chipsList.includes(textVal)) {
            chipsList.push(textVal);
            renderChips();
            syncHiddenField();
        }
        input.value = '';
    }

    // Capture completion inputs (Enter, Space, Comma)
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ' || e.key === ',') {
            e.preventDefault();
            addChipFromInput();
        } else if (e.key === 'Backspace' && input.value === '' && chipsList.length > 0) {
            // Remove last item if backspacing into an empty text field
            chipsList.pop();
            renderChips();
            syncHiddenField();
        }
    });

    // Handle blur events when clicking away from modal inputs
    input.addEventListener('blur', () => {
        addChipFromInput();
    });

    // Return control API handlers so our outer script sets values smoothly on modal load
    return {
        setValues: function(commaSeparatedString) {
            if (!commaSeparatedString || commaSeparatedString.trim() === "") {
                chipsList = [];
            } else {
                chipsList = commaSeparatedString.split(',')
                                                 .map(s => s.trim())
                                                 .filter(s => s.length > 0);
            }
            renderChips();
            syncHiddenField();
            input.value = '';
        }
    };
}

// --- GROUP SETTINGS MODAL HANDLING LOGIC ---
function initializeGroupModal() {
    const modal = document.getElementById('groupModal');
    const form = document.getElementById('editGroupForm');
    const triggerBtn = document.getElementById('editGroupTriggerBtn');
    const closeBtn = document.getElementById('closeGroupModalBtn');

    const fieldTitle = document.getElementById('groupEdit_title');
    const fieldDesc = document.getElementById('groupEdit_description');
    const fieldGradebook = document.getElementById('groupEdit_openGradeBook');

    if (!modal || !form || !triggerBtn) return;

    // Spin up chip UI controllers safely
    const teacherChips = createChipInputManager('teachers_chip_wrapper', 'groupEdit_teachers_input', 'groupEdit_teachers');
    const studentChips = createChipInputManager('students_chip_wrapper', 'groupEdit_students_input', 'groupEdit_students');

    triggerBtn.addEventListener('click', () => {
        form.reset();

        const id = triggerBtn.getAttribute('data-id');
        const title = triggerBtn.getAttribute('data-title');
        const description = triggerBtn.getAttribute('data-description');
        const openGradebook = triggerBtn.getAttribute('data-open-gradebook') === "true";
        
        const teachersStr = triggerBtn.getAttribute('data-teachers');
        const studentsStr = triggerBtn.getAttribute('data-students');

        // Populate base fields
        fieldTitle.value = title;
        fieldDesc.value = description;
        fieldGradebook.checked = openGradebook;

        // Populate chip arrays seamlessly using control pipelines
        if (teacherChips) teacherChips.setValues(teachersStr);
        if (studentChips) studentChips.setValues(studentsStr);

        form.action = `/group/${id}/edit/`;
        modal.style.display = "block";
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.style.display = "none");
    }

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
        const assignModal = document.getElementById('assignmentModal');
        if (event.target === assignModal) {
            assignModal.style.display = "none";
        }
    });
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}