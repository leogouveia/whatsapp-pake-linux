# Problemas comuns

[← README](../README.md)

## Não recebo notificações

Confira a permissão do site, configurações de notificações do WhatsApp e permissões do aplicativo no GNOME. Verifique também o modo Não Perturbe e se está usando o executável desta release, e não um AppImage antigo.

No DevTools, execute e depois volte para outra janela:

```javascript
Notification.permission
setTimeout(() => new Notification("Teste WhatsApp Pake Linux", {
  body: "Teste sintético de notificação"
}), 5000)
```

O retorno de sucesso da API não comprova o banner. Confira visualmente e teste uma mensagem real de outra conta. Não publique cookies, tokens, conteúdo de conversas ou dumps completos do DevTools.

Para diagnosticar D-Bus, limite o monitor a um título de teste:

```bash
dbus-monitor --session "type='method_call',interface='org.freedesktop.Notifications',member='Notify',arg3='Teste WhatsApp Pake Linux'"
```

O monitor mostrará chamadas sintéticas e pode mostrar o encaminhamento interno do GNOME. Encerre com Ctrl+C. Para conferir a conexão original, use o nome único `:1...` do remetente original:

```bash
gdbus call --session --dest org.freedesktop.DBus \
  --object-path /org/freedesktop/DBus \
  --method org.freedesktop.DBus.NameHasOwner ':1.NOME_DO_REMETENTE'
```

## X não encerra o processo

Isso é intencional: X oculta e mantém o aplicativo recebendo mensagens. Use Sair/Quit para encerrar. O defeito corrigido era o X deixar a janela visível e não responder.

## Não vejo o ícone da bandeja no GNOME

GNOME pode precisar de uma extensão de integração AppIndicator. Configure a integração da sua distro. Não desabilite todas as extensões nem apague configurações para testar este projeto. O aplicativo também possui menu Sair/Quit.

## AppImage não abre

Confira a arquitetura x86_64, permissão de execução e a disponibilidade de FUSE no host. Quando FUSE não estiver disponível, experimente a extração suportada pelo AppImage:

```bash
./nome-do-arquivo.AppImage --appimage-extract
./squashfs-root/AppRun
```

O pacote nativo RPM/DEB é preferível quando houver problema de integração com bibliotecas ou gráficos. AppImage ainda depende de partes do sistema, inclusive compatibilidade de glibc.

## GLIBC ou biblioteca não encontrada

Use o instalador gerado para a sua distribuição e uma versão compatível. Não copie bibliotecas do CachyOS para o Fedora. Recompile no sistema de destino seguindo BUILD.md e anexe somente a mensagem de erro relevante ao abrir uma issue.

## DevTools

View → Toggle Developer Tools, Ctrl+Alt+I. A feature `notification-diagnostics` deve estar presente no build; os scripts oficiais a habilitam. Não é a mesma coisa que compilar sem otimização ou incluir todos os símbolos de depuração.

## Remover ou voltar à versão anterior

Use o gerenciador que instalou o aplicativo: `sudo dnf remove whatsapp`, `sudo apt remove whatsapp` ou `sudo pacman -R whatsapp`. O AppImage pode ser removido como um arquivo comum. Não apague manualmente o diretório de perfil para corrigir um pacote.

Para voltar a uma versão anterior, baixe seu instalador em Releases e use o procedimento de downgrade do gerenciador da distro. No Arch: `sudo pacman -U ./pacote-anterior.pkg.tar.zst`. Encerre as instâncias atuais antes de trocar a versão.
