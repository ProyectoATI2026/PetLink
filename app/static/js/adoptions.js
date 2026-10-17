/**
 * PetLink - Search and Filters Logic for Adoptions
 */
document.addEventListener('DOMContentLoaded', function () {
    const textInput = document.getElementById('filtroTexto');
    const clearBtn = document.getElementById('btnLimpiarBusqueda');
    const resetBtn = document.getElementById('btnResetFilters');
    const chipBtns = document.querySelectorAll('.filter-chip-btn');
    const vaccinatedSelect = document.getElementById('filtroVacunado');
    const ageSelect = document.getElementById('filtroEdad');
    const locationSelect = document.getElementById('filtroUbicacion');
    const gridCards = document.querySelectorAll('.pet-card');
    const counter = document.getElementById('contadorResultados');
    const emptyState = document.getElementById('emptyCatalogState');

    let currentSpecies = 'todos';

    // 1. Filtrado en vivo por texto
    if (textInput) {
        textInput.addEventListener('input', function () {
            if (clearBtn) {
                clearBtn.style.display = this.value.trim() ? 'block' : 'none';
            }
            applyFilters();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            textInput.value = '';
            this.style.display = 'none';
            applyFilters();
            textInput.focus();
        });
    }

    // 2. Filtrado por chips de especie
    chipBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            chipBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSpecies = this.getAttribute('data-especie').toLowerCase();
            applyFilters();
        });
    });

    // 3. Filtrado por selects secundarios
    if (vaccinatedSelect) vaccinatedSelect.addEventListener('change', applyFilters);
    if (ageSelect) ageSelect.addEventListener('change', applyFilters);
    if (locationSelect) locationSelect.addEventListener('change', applyFilters);

    // 4. Botón de restablecer
    if (resetBtn) {
        resetBtn.addEventListener('click', resetAllFilters);
    }

    // Función principal de filtrado
    function applyFilters() {
        const textQuery = textInput ? textInput.value.trim().toLowerCase() : '';
        const vaccinatedVal = vaccinatedSelect ? vaccinatedSelect.value : 'todos';
        const ageVal = ageSelect ? ageSelect.value : 'todos';
        const locationVal = locationSelect ? locationSelect.value.toLowerCase() : 'todos';

        let visibleCount = 0;

        gridCards.forEach(card => {
            const name = card.getAttribute('data-name') || card.getAttribute('data-nombre') || '';
            const species = card.getAttribute('data-species') || card.getAttribute('data-especie') || '';
            const breed = card.getAttribute('data-breed') || card.getAttribute('data-raza') || '';
            const age = card.getAttribute('data-age') || card.getAttribute('data-edad') || '';
            const location = card.getAttribute('data-location') || card.getAttribute('data-ubicacion') || '';
            const isVaccinated = card.getAttribute('data-vaccinated') === 'true' || card.getAttribute('data-vacunado') === 'true';

            // Comprobación de texto (busca en nombre, raza o ubicación)
            let matchText = true;
            if (textQuery) {
                matchText = name.includes(textQuery) || breed.includes(textQuery) || location.includes(textQuery) || species.includes(textQuery);
            }

            // Comprobación de especie
            let matchSpecies = true;
            if (currentSpecies !== 'todos') {
                matchSpecies = species.includes(currentSpecies);
            }

            // Comprobación de vacunación
            let matchVaccine = true;
            if (vaccinatedVal === 'vacunado') {
                matchVaccine = isVaccinated;
            } else if (vaccinatedVal === 'no-vacunado') {
                matchVaccine = !isVaccinated;
            }

            // Comprobación de edad
            let matchAge = true;
            if (ageVal !== 'todos') {
                matchAge = age.includes(ageVal);
            }

            // Comprobación de ubicación
            let matchLocation = true;
            if (locationVal !== 'todos') {
                matchLocation = location.includes(locationVal);
            }

            if (matchText && matchSpecies && matchVaccine && matchAge && matchLocation) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Actualizar contador
        if (counter) {
            counter.textContent = `Mostrando ${visibleCount} mascota${visibleCount === 1 ? '' : 's'}`;
        }

        // Mostrar / Ocultar empty state
        if (emptyState) {
            emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }

        // Mostrar / Ocultar botón de restablecer si hay filtros activos
        const hasActiveFilters = textQuery || currentSpecies !== 'todos' || vaccinatedVal !== 'todos' || ageVal !== 'todos' || locationVal !== 'todos';
        if (resetBtn) {
            resetBtn.style.display = hasActiveFilters ? 'inline-flex' : 'none';
        }
    }

    // Inicializar si hay parámetros URL
    applyFilters();
});

// Función global para restablecer
window.resetAllFilters = function () {
    const textInput = document.getElementById('filtroTexto');
    const vaccinatedSelect = document.getElementById('filtroVacunado');
    const ageSelect = document.getElementById('filtroEdad');
    const locationSelect = document.getElementById('filtroUbicacion');
    const chipBtns = document.querySelectorAll('.filter-chip-btn');
    const clearBtn = document.getElementById('btnLimpiarBusqueda');

    if (textInput) textInput.value = '';
    if (clearBtn) clearBtn.style.display = 'none';
    if (vaccinatedSelect) vaccinatedSelect.value = 'todos';
    if (ageSelect) ageSelect.value = 'todos';
    if (locationSelect) locationSelect.value = 'todos';

    chipBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-especie') === 'todos') {
            btn.classList.add('active');
        }
    });

    const evt = new Event('change');
    if (vaccinatedSelect) vaccinatedSelect.dispatchEvent(evt);
};

// Alias para retrocompatibilidad
window.restablecerTodosFiltros = window.resetAllFilters;

// Modal de detalle de la mascota
window.openPetDetailModal = function (card) {
    if (!card) return;
    const modal = document.getElementById('modalDetallePet');
    if (!modal) return;

    const name = card.querySelector('.pet-card-name').textContent;
    const breed = card.getAttribute('data-breed') || card.getAttribute('data-raza');
    const ageStr = card.getAttribute('data-age-str') || card.getAttribute('data-edad-str');
    const location = card.querySelector('.pet-card-location span:last-child').textContent;
    const description = card.getAttribute('data-description') || card.getAttribute('data-descripcion') || 'Mascota rescatada y cuidada con cariño en espera de adopción responsable.';
    const owner = card.getAttribute('data-owner') || card.getAttribute('data-propietario') || 'PetLink Cuidador';
    const chatKey = card.getAttribute('data-chat') || 'mariana';
    const image = card.getAttribute('data-image') || card.getAttribute('data-imagen');
    const isVaccinated = card.getAttribute('data-vaccinated') === 'true' || card.getAttribute('data-vacunado') === 'true';
    const isNeutered = card.getAttribute('data-neutered') === 'true' || card.getAttribute('data-esterilizado') === 'true';

    document.getElementById('modalPetTitle').textContent = name;
    document.getElementById('modalPetMeta').textContent = `${breed} · ${ageStr}`;
    document.getElementById('modalPetLocation').textContent = location;
    document.getElementById('modalPetDescription').textContent = description;
    document.getElementById('modalPetGuardian').textContent = owner;
    document.getElementById('modalPetImg').src = image;

    // Badges de salud
    const healthUl = document.getElementById('modalPetHealth');
    healthUl.innerHTML = `
        <li class="${isVaccinated ? 'status-ok' : 'status-pending'}">
            ${isVaccinated ? '✓ Vacunas al día' : '⏳ Vacunación en curso'}
        </li>
        <li class="${isNeutered ? 'status-ok' : 'status-pending'}">
            ${isNeutered ? '✓ Esterilizado / Castrado' : '⏳ Pendiente esterilización'}
        </li>
        <li class="status-ok">✓ Desparasitación vigente</li>
        <li class="status-ok">✓ Revisión veterinaria periódica</li>
    `;

    // Enlace de chat
    const chatBtn = document.getElementById('modalPetChatBtn');
    if (chatBtn) {
        chatBtn.href = `/messages/?chat=${encodeURIComponent(chatKey)}`;
    }

    modal.style.display = 'flex';
};

window.closePetDetailModal = function () {
    const modal = document.getElementById('modalDetallePet');
    if (modal) modal.style.display = 'none';
};

// Aliases para retrocompatibilidad
window.abrirModalDetallePet = window.openPetDetailModal;
window.cerrarModalDetallePet = window.closePetDetailModal;
