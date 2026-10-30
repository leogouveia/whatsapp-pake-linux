# Origem e histórico dos fontes

[← README](../README.md)

Este repositório nasceu de um diagnóstico local em 28/10/2026. Não é um fork com todo o histórico Git do Pake: é um snapshot dos fontes distribuídos no pacote npm `pake-cli@3.17.7`, adaptado para uma aplicação WhatsApp específica.

| Componente | Base |
|---|---|
| Aplicativo | Pake CLI 3.17.7, https://github.com/tw93/Pake |
| Tauri | 2.10.2 |
| Plugin de notificações | 2.3.3 |
| notify-rust | 4.12.0; cópia local modificada |
| Tao | 0.34.5; cópia local modificada |
| CLI de empacotamento | @tauri-apps/cli 2.10.1 |

As versões transitivas estão documentadas no Cargo.lock. Os diretórios vendor incluem os avisos de licença dos crates de origem.

## Alterações sobre o snapshot

1. Configuração fixa do WhatsApp Web, identidade original `com.pake.ab7ae24`, janela 1100×760, bandeja ativa e ocultar ao fechar.
2. notify-rust: conexão D-Bus persistente; diff em patches/notify-rust-keep-connection.patch.
3. Tao: uso de decoração GTK padrão no Wayland; diff em patches/tao-native-gtk-decorations.patch.
4. Pake: feature notification-diagnostics para `tauri/devtools`; gate do item de menu e do handler alterado para aceitar essa feature em builds otimizados.
5. Remoção da dependência na configuração temporária `.pake` do CLI: scripts usam os arquivos versionados em src-tauri, sem a feature cli-build.
6. Página local mínima em web-assets para o bundle; a janela real navega para WhatsApp Web.
7. Nome/versão/descrição do projeto, templates de launcher e configurações DEB/RPM/AppImage.
8. Receita Arch, workflows, checksums e documentação pública.

A primeira validação de notificações ocorreu em um build local 1.0.0, depois empacotado como 1.0.0-2 junto da correção de janela. A primeira versão deste repositório é 1.0.1. O binário local antigo não é rotulado como se fosse um build de CI para todas as distros.

A configuração original foi recuperada do aplicativo instalado e de metadados de build. Nenhum perfil do WhatsApp, cookie, token, mensagem, cache de navegação ou log de sessão foi incluído no repositório.

Os relatórios locais foram reescritos para remover caminhos de usuário e identificadores de sessão. A evidência preservada está em DIAGNOSTICS.md.

Ícones de outros aplicativos e formatos de empacotamento fora do Linux foram removidos do snapshot para manter o repositório focado; os fontes multiplataforma das dependências vendorizadas foram preservados.

Em 30/10/2026, a adaptação de eventos do PR 1218 foi completada com patches/tao-gtk-event-propagation.patch para corrigir a regressão no arraste da barra de título.
