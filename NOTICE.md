# ZK-REMOTE: aviso de origen y licencia

ZK-REMOTE es una **versión modificada de [RustDesk](https://github.com/rustdesk/rustdesk)**.

- RustDesk: Copyright © Purslane Tech Pte. Ltd. y colaboradores.
- Licencia: **GNU Affero General Public License v3.0** (ver [`LICENSE`](LICENSE), sin modificar). ZK-REMOTE se distribuye bajo la misma licencia.
- Código fuente de ZK-REMOTE: https://github.com/pruebasjzecpa/zk-remote
- Versión base de upstream: tag `1.5.1`.

"RustDesk" es una marca de sus titulares. ZK-REMOTE no está afiliado a RustDesk ni a Purslane Tech Pte. Ltd.

## Modificaciones respecto de upstream

Todas las modificaciones están aisladas para que los merges con upstream sean simples:

| Archivo | Cambio |
|---|---|
| `src/zk_brand.rs` (nuevo) | Fija el nombre de la aplicación "ZK-REMOTE" (mismo mecanismo que un cliente personalizado) |
| `src/lib.rs`, `src/common.rs` | Una línea cada una para registrar y aplicar `zk_brand` |
| `zk/apply_branding.py` (nuevo) | En la compilación: reemplaza íconos, metadatos del ejecutable y colores, y agrega el link al código fuente en "Acerca de" |
| `zk/branding/` (nuevo) | Logo e íconos de ZK-REMOTE (`zk/tools/make_icons.py` los genera) |
| `zk/msi/License.rtf` (nuevo) | Aviso AGPL que muestra el instalador MSI |
| `.github/workflows/zk-windows.yml` (nuevo) | Compilación de Windows x64 sin firma |
