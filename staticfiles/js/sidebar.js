'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.content-wrapper');
    const toggleButton = document.querySelector('.sidebar-toggle');
    const toggleIcon = toggleButton.querySelector('i');
    const overlay = document.getElementById('sidebar-overlay');

    function toggleSidebar() {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        } else {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            
            // Toggle icon
            if (sidebar.classList.contains('collapsed')) {
                toggleIcon.classList.replace('fa-chevron-left', 'fa-chevron-right');
            } else {
                toggleIcon.classList.replace('fa-chevron-right', 'fa-chevron-left');
            }
            
            // Save state
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        }
    }

    // Add click event to toggle button
    toggleButton.addEventListener('click', toggleSidebar);

    // Handle overlay clicks on mobile
    overlay.addEventListener('click', function() {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });

    // Initialize sidebar state
    if (window.innerWidth > 768) {
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
            toggleIcon.classList.replace('fa-chevron-left', 'fa-chevron-right');
        }
    }
});

