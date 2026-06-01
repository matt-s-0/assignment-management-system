document.addEventListener('DOMContentLoaded', () => {
    initializeDashboardToggles();
});


function initializeDashboardToggles() {
    const groupHeaders = document.querySelectorAll('.group-header');

    groupHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const parentCard = header.closest('.group-card');
            const targetContainer = parentCard.querySelector('.assignment-groups-container');
            const toggleIcon = header.querySelector('.toggle-icon');

            if (!targetContainer) return;

            if (targetContainer.style.display === 'block') {
                // Close the tray
                targetContainer.style.display = 'none';
                toggleIcon.textContent = '+';
            } else {
                // Open the tray
                targetContainer.style.display = 'block';
                toggleIcon.textContent = '−';
            }
        });
    });
}