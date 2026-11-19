# Conectar Instagram (una sola vez, unos 15 minutos)

Estos pasos los haces tú porque requieren tus cuentas y contraseñas. **Nunca pegues el token en un chat**: va directo a los secretos de GitHub.

## 1. Cuenta de Instagram profesional

1. Crea la cuenta (sugerido: `@raroperocierto`; si está tomado, `@raropero.cierto` o `@raroperociertooficial`).
2. Perfil → Menú → Configuración → Tipo de cuenta y herramientas → Cambiar a cuenta profesional → **Creador**.
3. Nombre: Raro Pero Cierto. Bio sugerida: "Un dato raro al día. Y es verdad: siempre con la fuente."

## 2. App de Meta y token

1. Entra en https://developers.facebook.com/apps con tu Facebook y pulsa **Crear app**.
2. Caso de uso: **Administrar mensajes y contenido en Instagram** (API de Instagram con inicio de sesión de Instagram). No necesitas página de Facebook.
3. En la configuración de la API con inicio de sesión de Instagram, pulsa **Agregar cuenta** / **Generar token**, inicia sesión con la cuenta nueva y acepta los permisos de publicación (`instagram_business_content_publish`) y estadísticas (`instagram_business_manage_insights`).
4. Copia el **token** y el **ID de la cuenta de Instagram** que aparece junto a ella.

La app puede quedarse en modo desarrollo: solo publica en tu propia cuenta, así que no necesita revisión de Meta.

## 3. Secretos en GitHub

En el repositorio → Settings → Secrets and variables → Actions → **New repository secret**:

| Nombre | Valor |
| --- | --- |
| `IG_TOKEN` | el token del paso 2 |
| `IG_USER_ID` | el ID de la cuenta del paso 2 |
| `GH_PAT` (opcional, recomendado) | token de GitHub "fine-grained" con acceso solo a este repositorio y permiso **Secrets: Read and write**; sirve para renovar el token de Instagram solo |

Y en Settings → Actions → General → Workflow permissions: **Read and write permissions**.

## 4. Probar

Actions → **Publicar reel del día** → Run workflow → `solo_probar = 1`. Debe decir qué video publicaría. Luego ejecútalo con `0` para la primera publicación real.
