const dataElement = document.getElementById('groups-data');
let groupsData = {};

if (dataElement) {
    try {
        let rawData = JSON.parse(dataElement.textContent);
        
        if (typeof rawData === 'string') {
            groupsData = JSON.parse(rawData);
        } else {
            groupsData = rawData;
        }
        
    } catch (e) {
        console.error("Failed to parse JSON:", e);
    }
}

function autofillGroupForm(groupId) {
    if (!groupId) return;

    const stringId = String(groupId).trim();
    const group = groupsData[stringId];

    if (!group) {
        console.error(`Could not find group data matching key:`, stringId);
        return;
    }

    const form = document.getElementById('editGroupForm');
    if (form) form.action = '/group/' + stringId + '/edit/';

    const titleField = document.getElementById('groupEdit_title');
    const descField = document.getElementById('groupEdit_description');
    const teachersField = document.getElementById('groupEdit_teachers');
    const studentsField = document.getElementById('groupEdit_students');
    const ogbField = document.getElementById('groupEdit_openGradeBook');

    if (titleField) titleField.value = group.title || '';
    if (descField) descField.value = group.description || '';
    if (teachersField) teachersField.value = group.teachers || '';
    if (studentsField) studentsField.value = group.students || '';
    if (ogbField) ogbField.checked = !!group.openGradeBook;
}

window.autofillGroupForm = autofillGroupForm;