document.addEventListener('DOMContentLoaded', function() {
    // Add NiceAdmin specific functionality here
    
    // Add toggle sidebar functionality
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toggle-sidebar-btn';
    toggleBtn.innerHTML = '<i class="bi bi-list"></i>';
    document.getElementById('header').prepend(toggleBtn);
    
    toggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('toggle-sidebar');
    });
    
    // Add active class to current menu items
    const currentPath = window.location.pathname;
    document.querySelectorAll('#content-main a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});