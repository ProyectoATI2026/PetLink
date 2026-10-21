/**
 * PetLink - Funcionalidades Principales y Navegación Global
 */
document.addEventListener('DOMContentLoaded', function () {
    // 1. Menú móvil desplegable
    const btnMenu = document.getElementById('menu-toggle');
    const listaMenu = document.getElementById('listaMenu');
    
    if (btnMenu && listaMenu) {
        btnMenu.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = listaMenu.classList.contains('open') || listaMenu.style.display === 'flex';
            if (isOpen) {
                listaMenu.style.display = 'none';
                listaMenu.classList.remove('open');
            } else {
                listaMenu.style.display = 'flex';
                listaMenu.classList.add('open');
            }
        });

        // Cerrar menú si se hace click fuera
        document.addEventListener('click', function (e) {
            if (!listaMenu.contains(e.target) && e.target !== btnMenu && !btnMenu.contains(e.target)) {
                listaMenu.style.display = 'none';
                listaMenu.classList.remove('open');
            }
        });
    }

    // 2. Auto-desvanecimiento de alertas del sistema
    const banners = document.querySelectorAll('.alert-banner');
    banners.forEach(banner => {
        setTimeout(() => {
            banner.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            banner.style.opacity = '0';
            banner.style.transform = 'translateY(-10px)';
            setTimeout(() => banner.remove(), 500);
        }, 5000);
    });
});