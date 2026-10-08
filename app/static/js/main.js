document.addEventListener('DOMContentLoaded', function () {
    const btnMenu = document.getElementById('menu-toggle');
    const listaMenu = document.getElementById('listaMenu');
    
    if (btnMenu && listaMenu) {
        btnMenu.addEventListener('click', function () {
            if (listaMenu.style.display === 'flex') {
                listaMenu.style.display = 'none';
            } else {
                listaMenu.style.display = 'flex';
            }
        });
    }

    const formBusqueda = document.getElementById('busqueda');
    const formBusquedaMini = document.getElementById('busquedaMini');

    if (formBusqueda) {
        formBusqueda.addEventListener('submit', function (event) {
            const busqueda = document.getElementById('campoBusqueda').value;
            console.log('Ejecutando búsqueda (Escritorio): ' + busqueda);
        });
    }

    if (formBusquedaMini) {
        formBusquedaMini.addEventListener('submit', function (event) {
            const busquedaMini = document.getElementById('campoBusquedaMini').value;
            console.log('Ejecutando búsqueda (Móvil): ' + busquedaMini);
        });
    }
});