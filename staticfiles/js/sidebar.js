'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const isMobile = () => window.innerWidth <= 768;

    function toggleSidebar() {
        if (isMobile()) {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        } else {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        }
    }

    // Event Listeners
    document.querySelector('.sidebar-toggle').addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);

    // Handle window resize
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            overlay.classList.remove('active');
            sidebar.classList.remove('active');
        }
    });

    // Initialize sidebar state
    if (!isMobile()) {
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
        }
    }
});

