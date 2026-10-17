/**
 * PetLink - Messages and Chats Logic
 * UI skeleton ready to connect with the database messages model.
 */
document.addEventListener('DOMContentLoaded', function () {

    // DOM Elements
    const chatAppCard       = document.getElementById('chatAppCard');
    const conversationItems = document.querySelectorAll('.chat-item');
    const messagesContainer = document.getElementById('messagesContainer');
    const chatMessagesBody  = document.getElementById('chatMessagesBody');
    const messageInput      = document.getElementById('inputMensajeChat');
    const searchInput       = document.getElementById('inputBuscarChat');
    const backBtn           = document.getElementById('btnVolverListaChats');

    // -------------------------------------------------------------------------
    // 1. Click on conversation items (switches active chat)
    // -------------------------------------------------------------------------
    conversationItems.forEach(function (item) {
        item.addEventListener('click', function () {
            // Marcar como activo
            conversationItems.forEach(function (i) { i.classList.remove('active'); });
            this.classList.add('active');

            // Limpiar badge de no leídos
            var badge = this.querySelector('.chat-unread-badge');
            if (badge) badge.remove();

            // En móvil: mostrar panel de chat y ocultar sidebar
            if (chatAppCard) {
                chatAppCard.classList.add('mobile-chat-open');
            }

            // Foco en el campo de texto
            if (messageInput) messageInput.focus();
        });
    });

    // -------------------------------------------------------------------------
    // 2. Back button on mobile devices
    // -------------------------------------------------------------------------
    if (backBtn) {
        backBtn.addEventListener('click', function () {
            if (chatAppCard) {
                chatAppCard.classList.remove('mobile-chat-open');
            }
        });
    }

    // -------------------------------------------------------------------------
    // 3. Send new message
    // -------------------------------------------------------------------------
    window.sendChatMessage = function (event) {
        event.preventDefault();
        if (!messageInput || !messagesContainer) return;

        var text = messageInput.value.trim();
        if (!text) return;

        var now = new Date();
        var timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        // Crear burbuja de mensaje propio
        var wrapper = document.createElement('div');
        wrapper.className = 'message-bubble-wrapper message-me';
        wrapper.innerHTML =
            '<div class="message-bubble">' +
                '<p class="message-text">' + escapeHtml(text) + '</p>' +
                '<span class="message-time">' + timeStr + ' <span class="message-check">\u2713\u2713</span></span>' +
            '</div>';

        messagesContainer.appendChild(wrapper);
        messageInput.value = '';
        scrollToBottom();

        // Actualizar snippet en la lista lateral (el activo)
        var activeItem = document.querySelector('.chat-item.active');
        if (activeItem) {
            var snippet = activeItem.querySelector('.chat-item-snippet');
            var time    = activeItem.querySelector('.chat-item-time');
            if (snippet) snippet.textContent = 'Tú: ' + text;
            if (time)    time.textContent    = timeStr;
        }
    };

    // Alias para retrocompatibilidad
    window.enviarMensajeChat = window.sendChatMessage;

    // -------------------------------------------------------------------------
    // 4. Live search in conversations list
    // -------------------------------------------------------------------------
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            var q = this.value.trim().toLowerCase();
            conversationItems.forEach(function (item) {
                var name = (item.getAttribute('data-name') || item.getAttribute('data-nombre') || '').toLowerCase();
                var subject = (item.getAttribute('data-subject') || item.getAttribute('data-asunto') || '').toLowerCase();
                item.style.display = (name.includes(q) || subject.includes(q)) ? 'flex' : 'none';
            });
        });
    }

    // -------------------------------------------------------------------------
    // Utilities
    // -------------------------------------------------------------------------
    function scrollToBottom() {
        if (chatMessagesBody) {
            chatMessagesBody.scrollTop = chatMessagesBody.scrollHeight;
        }
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.innerText = str;
        return div.innerHTML;
    }

    // Scroll inicial al cargar la página
    scrollToBottom();
});
