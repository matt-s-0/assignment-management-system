document.addEventListener('DOMContentLoaded', () => {
    initializeGroupModal();
});

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
    const form = document.getElementById('createGroupForm');

    const fieldTitle = document.getElementById('groupCreate_title');
    const fieldDesc = document.getElementById('groupCreate_description');
    const fieldGradebook = document.getElementById('groupCreate_openGradeBook');

    if (!modal || !form) return;

    const teacherChips = createChipInputManager('teachers_chip_wrapper', 'groupCreate_teachers_input', 'groupCreate_teachers');
    const studentChips = createChipInputManager('students_chip_wrapper', 'groupCreate_students_input', 'groupCreate_students');

    const teachersStr = "";
    const studentsStr = "";

    if (teacherChips) teacherChips.setValues(teachersStr);
    if (studentChips) studentChips.setValues(studentsStr);

    form.action = `/group/create/`;
    modal.style.display = "block";
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}