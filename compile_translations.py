import os
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Diccionario completo de traducciones español -> inglés
TRANSLATIONS = {
    # Base / Navbar / Footer
    "PetLink - Comunidad y Adopción Responsable": "PetLink - Community and Responsible Adoption",
    "Inicio": "Home",
    "Adopciones": "Adoptions",
    "Mensajes": "Messages",
    "Buscar mascotas...": "Search pets...",
    "Buscar": "Search",
    "Buscar en móvil": "Search on mobile",
    "Ver mi perfil": "View my profile",
    "Ver perfil": "View profile",
    "Cerrar sesión": "Log out",
    "Salir": "Exit",
    "Iniciar Sesión": "Log In",
    "Registro": "Register",
    "Casa": "Home",
    "Pata": "Paw",
    "Chat": "Chat",
    "Usuario": "User",
    "Usuarios": "Users",
    "Ir a Inicio de PetLink": "Go to PetLink Home",
    "Ir a Inicio de Administrador": "Go to Admin Home",
    "Abrir menú": "Open menu",
    "Copyright &copy; 2026 Escuela de computación - ATI. Todos los derechos reservados": "Copyright &copy; 2026 School of Computing - ATI. All rights reserved",

    # Home
    "Inicio - PetLink | Comunidad y Adopción Responsable": "Home - PetLink | Community and Responsible Adoption",
    "Filtros Rápidos": "Quick Filters",
    "Perros": "Dogs",
    "Gatos": "Cats",
    "Aves": "Birds",
    "Otros": "Others",
    "¿Sabías qué?": "Did you know?",
    "En PetLink todas las adopciones son <strong>gratuitas</strong> y verificadas por la comunidad. Denuncia cualquier intento de cobro.": "At PetLink all adoptions are <strong>free</strong> and verified by the community. Report any attempt to charge.",
    "+ Dar en Adopción": "+ Put up for Adoption",
    "Encuentra un compañero": "Find a companion",
    "¿Listo para dar amor?": "Ready to give love?",
    "Cientos de mascotas en tu zona están buscando un hogar cálido. Explora nuestro catálogo verificado hoy mismo.": "Hundreds of pets in your area are looking for a warm home. Explore our verified catalog today.",
    "Ver Adopciones": "View Adoptions",
    "Mascota en adopción": "Pet for adoption",
    "Todos": "All",
    "¿Tienes una historia de rescate o una mascota para reportar?": "Do you have a rescue story or a pet to report?",
    "Foto / Mascota": "Photo / Pet",
    "Reportar Encontrado": "Report Found",
    "Adoptar": "Adopt",
    "Publicaciones Recientes": "Recent Posts",
    "Actualizado en tiempo real": "Updated in real time",
    "Imagen de": "Image of",
    "Me gusta": "Like",
    "Comentarios": "Comments",
    "Compartir": "Share",
    "Enviar mensaje directo a": "Send direct message to",
    "Contactar": "Contact",
    "Escribe un comentario respetuoso...": "Write a respectful comment...",
    "Comentar": "Comment",
    "Tú": "You",
    "Aún no hay publicaciones": "No posts yet",
    "Sé el primero en compartir una historia de rescate, adopción o mascota encontrada con la comunidad.": "Be the first to share a rescue, adoption, or found pet story with the community.",
    "+ Crear Publicación": "+ Create Post",
    "Crear Publicación Comunitaria": "Create Community Post",
    "Describe la situación: rescate, extravío o adopción...": "Describe the situation: rescue, loss, or adoption...",
    "Puedes adjuntar fotos en la versión completa": "You can attach photos in the full version",
    "Cancelar": "Cancel",
    "Publicar": "Publish",
    "Por favor escribe algún detalle para la publicación.": "Please write some details for the post.",
    "¡Publicación enviada exitosamente a la comunidad PetLink!": "Post successfully submitted to the PetLink community!",
    "¡Enlace a la publicación de": "Link to the post of",
    "copiado al portapapeles!": "copied to clipboard!",
    "Publicación de": "Post of",
    "compartida.": "shared.",

    # Adoptions
    "Adopciones - PetLink | Catálogo de Mascotas": "Adoptions - PetLink | Pet Catalog",
    "Mascotas disponibles": "Available pets",
    "Mostrando": "Showing",
    "mascotas": "pets",
    "↺ Restablecer filtros": "↺ Reset filters",
    "Buscar por nombre, raza o ubicación (ej. Simba, Pastor Alemán, Chacao)...": "Search by name, breed, or location (e.g., Simba, German Shepherd, Chacao)...",
    "Mestizo": "Mixed breed",
    "Conocer a": "Meet",
    "No hay mascotas disponibles": "No pets available",
    "Aún no se han registrado mascotas, o ninguna coincide con tu búsqueda. ¡Regresa pronto!": "No pets have been registered yet, or none match your search. Check back soon!",
    "+ Registrar una mascota": "+ Register a pet",

    # Messages
    "Mensajes - PetLink | Chats y Conversaciones": "Messages - PetLink | Chats and Conversations",
    "Continúa tus conversaciones con la comunidad.": "Continue your conversations with the community.",
    "Buscar conversaciones...": "Search conversations...",
    "Abrir chat con": "Open chat with",
    "No tienes conversaciones aún.": "You don't have conversations yet.",
    "Cuando contactes a alguien desde una ficha de adopción, aparecerá aquí.": "When you contact someone from an adoption listing, it will appear here.",
    "Volver a lista de mensajes": "Back to messages list",
    "Chats": "Chats",
    "En línea": "Online",
    "Desconectado": "Offline",
    "Ver ficha de adopción": "View adoption listing",
    "Ficha": "Listing",
    "No hay mensajes aún. ¡Envía el primero!": "No messages yet. Send the first one!",
    "Adjuntar foto o archivo": "Attach photo or file",
    "Escribe un mensaje seguro...": "Write a secure message...",
    "Enviar mensaje": "Send message",
    "Enviar": "Send",
    "Tus mensajes": "Your messages",
    "Selecciona una conversación de la lista, o inicia una nueva desde la ficha de adopción de una mascota.": "Select a conversation from the list, or start a new one from a pet adoption listing.",
    "Explorar Adopciones": "Explore Adoptions",

    # Reports
    "Moderación de Reportes - PetLink Admin": "Reports Moderation - PetLink Admin",
    "Administración / Moderación": "Administration / Moderation",
    "Moderación de Reportes": "Reports Moderation",
    "Revisa y procesa las denuncias enviadas por la comunidad para mantener a PetLink seguro y libre de abusos.": "Review and process reports submitted by the community to keep PetLink safe and free of abuse.",
    "Pendientes": "Pending",
    "Procesados": "Processed",
    "Historial Completo": "Full History",
    "Reportado por:": "Reported by:",
    "Publicación denunciada:": "Reported post:",
    "reportes acumulados": "accumulated reports",
    "Ignorar": "Ignore",
    "Eliminar Post": "Delete Post",
    "¡Bandeja de moderación limpia!": "Moderation inbox clean!",
    "No hay denuncias o publicaciones pendientes de moderación en este momento. La comunidad está en orden.": "There are no pending reports or posts at this time. The community is in order.",
    "Confirmar Acción": "Confirm Action",
    "¿Estás seguro de procesar esta moderación?": "Are you sure you want to process this moderation action?",
    "Confirmar": "Confirm",

    # Pet Profile
    "Propietario": "Owner",
    "Editar Perfil": "Edit Profile",
    "Iniciar Chat con el Dueño": "Start Chat with Owner",
    "Información de la Mascota": "Pet Information",
    "Edad / Fecha Nacimiento": "Age / Birth Date",
    "No especificada": "Not specified",
    "Género": "Gender",
    "No especificado": "Not specified",
    "Registrado el": "Registered on",
    "Sobre": "About",
    "Sin descripción disponible.": "No description available.",
    "Editar Perfil de": "Edit Profile of",
    "Guardar Cambios": "Save Changes",

    # User Profile
    "Mi perfil": "My profile",
    "Administra tu información personal y tus preferencias en PetLink.": "Manage your personal information and preferences on PetLink.",
    "Modificar perfil": "Modify profile",
    "Perfil Verificado": "Verified Profile",
    "Tu información ayuda a crear una comunidad PetLink más segura y cercana.": "Your information helps create a safer and closer PetLink community.",
    "Información personal": "Personal information",
    "Datos visibles únicamente para ti.": "Data visible only to you.",
    "Cédula de identidad": "National ID",
    "Cédula": "National ID",
    "Fecha de nacimiento": "Birth date",
    "Ubicación": "Location",
    "Intereses y afinidades": "Interests and affinities",
    "Mis Mascotas": "My Pets",
    "Nacimiento:": "Birth:",
    "Editar": "Edit",
    "No tienes mascotas registradas todavía.": "You don't have registered pets yet.",
    "Agregar mascota": "Add pet",
    "Modificar Perfil": "Modify Profile",
    "Información de Usuario": "User Information",
    "Nombre": "First Name",
    "Apellido": "Last Name",
    "Detalles Personales": "Personal Details",
    "Gustos e Intereses (separados por comas)": "Interests and Hobbies (separated by commas)",

    # Auth
    "Conectando corazones, cambiando vidas": "Connecting hearts, changing lives",
    "Nombre de Usuario": "Username",
    "Contraseña": "Password",
    "Confirmar Contraseña": "Confirm Password",
    "Correo Electrónico": "Email Address",
    "Ingresar": "Sign In",
    "¿No tienes una cuenta?": "Don't have an account?",
    "Regístrate aquí": "Register here",
    "Crear Cuenta": "Create Account",
    "Registrarse": "Register",
    "¿Ya tienes cuenta?": "Already have an account?",
    "Inicia sesión": "Log in",

    # Pet Registration
    "Registro Mascota": "Pet Registration",
    "Registrar nueva Mascota": "Register new Pet",
    "Nombre de la Mascota": "Pet Name",
    "Especie": "Species",
    "Raza / Mestizaje": "Breed / Mixed",
    "Edad": "Age",
    "Macho": "Male",
    "Hembra": "Female",
    "Breve Descripción / Estado": "Brief Description / Status",
    "Imagen de la Mascota": "Pet Image",
    "Foto de Perfil de la Mascota": "Pet Profile Photo",
    "Registrar Mascota": "Register Pet",
    "Al registrar la mascota, aceptas publicar esta información de forma abierta para que otros miembros de PetLink puedan contactarte.": "By registering the pet, you agree to publish this information openly so other PetLink members can contact you.",

    # Backend / System messages
    "El usuario inició sesión correctamente.": "User logged in successfully.",
    "¡Bienvenido de nuevo!": "Welcome back!",
    "Nombre de usuario o contraseña incorrectos.": "Invalid username or password.",
    "El usuario cerró sesión.": "User logged out.",
    "Nuevo usuario registrado en la plataforma.": "New user registered on the platform.",
    "Cuenta creada exitosamente. Ya puedes iniciar sesión.": "Account created successfully. You can now log in.",
    "Mascota registrada exitosamente.": "Pet registered successfully.",
    "No tienes permiso para editar el perfil de esta mascota.": "You do not have permission to edit this pet's profile.",
    "Perfil de la mascota actualizado correctamente.": "Pet profile updated successfully.",
    "Acceso denegado: Se requieren credenciales de Administrador para ver la pantalla de moderación de reportes.": "Access denied: Administrator credentials required to view the report moderation screen.",
    "El administrador accedió a la pantalla de moderación de reportes.": "Administrator accessed the report moderation screen.",
    "Inicio de Sesión Exitoso": "Successful Login",
    "Intento de Login Fallido": "Failed Login Attempt",
    "Cierre de Sesión": "Logout",
    "Registro de Usuario": "User Registration",
    "Acción": "Action",
    "Dirección IP": "IP Address",
    "Detalles": "Details",
    "Fecha y Hora": "Date and Time",
    "Log de Auditoría": "Audit Log",
    "Logs de Auditoría": "Audit Logs",
    "Mascota": "Pet",
    "Mascotas": "Pets",
    "Anónimo": "Anonymous",
    "Ingrese su usuario": "Enter your username",
    "Ingrese su contraseña": "Enter your password",
    "Ingrese el nombre de la mascota": "Enter pet name",
    "Ingrese la especie de la mascota": "Enter pet species",
    "Ingrese la edad de la mascota": "Enter pet age",
    "Ingrese la raza de la mascota": "Enter pet breed",
    "Ingrese una descripción de la mascota": "Enter a description of the pet",
    "Nombre de la mascota": "Pet name",
    "Ej. Perro, Gato": "E.g. Dog, Cat",
    "Ej. Mestizo, Poodle": "E.g. Mixed breed, Poodle",
    "Macho / Hembra": "Male / Female",
    "Descripción...": "Description...",
    "Español": "Spanish",
    "English": "English",
}

def generate_po(filepath, lang_code, translations):
    """Genera el archivo .po con formato estándar GNU gettext."""
    lines = [
        'msgid ""',
        'msgstr ""',
        '"Project-Id-Version: PetLink 1.0\\n"',
        '"Report-Msgid-Bugs-To: \\n"',
        '"POT-Creation-Date: 2026-10-16 19:50-0400\\n"',
        '"PO-Revision-Date: 2026-10-16 19:50-0400\\n"',
        '"Last-Translator: PetLink Team\\n"',
        f'"Language: {lang_code}\\n"',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: 8bit\\n"',
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"',
        "",
    ]
    for msgid, msgstr in translations.items():
        # Escapar comillas dobles y saltos de línea
        clean_id = msgid.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        clean_str = msgstr.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        lines.append(f'msgid "{clean_id}"')
        lines.append(f'msgstr "{clean_str}"')
        lines.append("")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated PO: {filepath}")

def compile_mo(po_dict, mo_filepath):
    """
    Compila un diccionario de cadenas (msgid -> msgstr) al formato binario .mo de GNU gettext.
    """
    # Incluir cabecera vacía estándar
    header_id = ""
    header_str = (
        "Project-Id-Version: PetLink 1.0\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
    )
    full_dict = {header_id: header_str}
    full_dict.update(po_dict)

    # Ordenar por msgid codificado en UTF-8 (requisito estricto del formato MO de gettext)
    keys = sorted(full_dict.keys(), key=lambda k: k.encode("utf-8"))
    num_strings = len(keys)

    orig_bytes = [k.encode("utf-8") + b"\x00" for k in keys]
    trans_bytes = [full_dict[k].encode("utf-8") + b"\x00" for k in keys]

    # Calcular offsets
    # Header: 7 enteros de 4 bytes = 28 bytes
    # Tabla original: num_strings * 2 enteros (longitud, offset) = num_strings * 8 bytes
    # Tabla traducida: num_strings * 2 enteros = num_strings * 8 bytes
    orig_table_offset = 28
    trans_table_offset = orig_table_offset + num_strings * 8
    strings_start_offset = trans_table_offset + num_strings * 8

    # Construir datos de cadenas y tablas
    orig_table = []
    trans_table = []
    current_offset = strings_start_offset

    all_orig_data = b""
    for ob in orig_bytes:
        orig_length = len(ob) - 1 # sin el null byte final
        orig_table.append((orig_length, current_offset))
        all_orig_data += ob
        current_offset += len(ob)

    all_trans_data = b""
    for tb in trans_bytes:
        trans_length = len(tb) - 1
        trans_table.append((trans_length, current_offset))
        all_trans_data += tb
        current_offset += len(tb)

    # Empaquetar todo en formato little-endian
    magic = 0x950412DE
    format_revision = 0
    hash_table_size = 0
    hash_table_offset = 0

    header = struct.pack(
        "<I I I I I I I",
        magic,
        format_revision,
        num_strings,
        orig_table_offset,
        trans_table_offset,
        hash_table_size,
        hash_table_offset,
    )

    orig_table_packed = b"".join(struct.pack("<I I", length, offset) for length, offset in orig_table)
    trans_table_packed = b"".join(struct.pack("<I I", length, offset) for length, offset in trans_table)

    mo_filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(mo_filepath, "wb") as f:
        f.write(header)
        f.write(orig_table_packed)
        f.write(trans_table_packed)
        f.write(all_orig_data)
        f.write(all_trans_data)

    print(f"Compiled MO: {mo_filepath} ({num_strings} entries)")

def main():
    locale_dir = BASE_DIR / "locale"

    # 1. Para inglés (en): traducimos cada msgid a su valor en inglés
    en_po_path = locale_dir / "en" / "LC_MESSAGES" / "django.po"
    en_mo_path = locale_dir / "en" / "LC_MESSAGES" / "django.mo"
    generate_po(en_po_path, "en", TRANSLATIONS)
    compile_mo(TRANSLATIONS, en_mo_path)

    # 2. Para español (es): el msgid y msgstr son idénticos
    es_dict = {k: k for k in TRANSLATIONS.keys()}
    es_po_path = locale_dir / "es" / "LC_MESSAGES" / "django.po"
    es_mo_path = locale_dir / "es" / "LC_MESSAGES" / "django.mo"
    generate_po(es_po_path, "es", es_dict)
    compile_mo(es_dict, es_mo_path)

    print("All translations generated and compiled successfully!")

if __name__ == "__main__":
    main()
