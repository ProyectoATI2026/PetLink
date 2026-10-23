/**
 * PetLink - Messages and Chats Logic
 * UI connected with Django conversations and messages.
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
    // 1. Click on conversation items
    // -------------------------------------------------------------------------
    conversationItems.forEach(function (item) {
        item.addEventListener('click', function () {

            // Marcar como activo
            conversationItems.forEach(function (i) {
                i.classList.remove('active');
            });

            this.classList.add('active');

            // Limpiar badge de no leídos
            var badge = this.querySelector('.chat-unread-badge');

            if (badge) {
                badge.remove();
            }

            // Abrir la conversación real usando Django
            var chatUrl = this.getAttribute('data-url');

            if (chatUrl) {
                window.location.href = chatUrl;
                return;
            }

            // En móvil: mostrar panel de chat
            if (chatAppCard) {
                chatAppCard.classList.add('mobile-chat-open');
            }

            // Foco en el campo de texto
            if (messageInput) {
                messageInput.focus();
            }
        });

        // Permitir abrir con Enter o barra espaciadora
        item.addEventListener('keydown', function (event) {

            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();

                var chatUrl = this.getAttribute('data-url');

                if (chatUrl) {
                    window.location.href = chatUrl;
                }
            }
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

        if (event) {
            event.preventDefault();
        }

        var form = document.getElementById('formEnviarMensaje');

        if (!messageInput || !form) {
            return;
        }

        var text = messageInput.value.trim();

        if (!text) {
            return;
        }

        /*
         * El mensaje ya no se crea solamente en el navegador.
         * El formulario se envía a Django y MessagesView
         * guarda el mensaje en SQLite.
         */
        form.submit();
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

                var name = (
                    item.getAttribute('data-name') ||
                    item.getAttribute('data-nombre') ||
                    ''
                ).toLowerCase();

                var subject = (
                    item.getAttribute('data-subject') ||
                    item.getAttribute('data-asunto') ||
                    ''
                ).toLowerCase();

                item.style.display =
                    (name.includes(q) || subject.includes(q))
                        ? 'flex'
                        : 'none';
            });
        });
    }

    // -------------------------------------------------------------------------
    // Utilities
    // -------------------------------------------------------------------------
    function scrollToBottom() {

        if (chatMessagesBody) {
            chatMessagesBody.scrollTop =
                chatMessagesBody.scrollHeight;
        }
    }

    // Scroll inicial al cargar la página
    scrollToBottom();
});
