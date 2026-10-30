# Diagnóstico, correções e evidências

[← README](../README.md)

## 1. Notificação aceita, mas invisível

O WhatsApp Web tinha `Notification.permission === "granted"`. Criar `new Notification(...)` chegava ao comando Rust/Tauri, que retornava sucesso. O D-Bus recebia `Notify`, mas não aparecia banner.

A pista foi a identidade: sem `desktop-entry` e com uma identidade inexistente, o banner aparecia; com `desktop-entry=whatsapp`, não. As configurações globais e individuais de banners estavam habilitadas. Nenhuma reinstalação ou limpeza de perfil foi necessária.

O GNOME Shell instalado identificava aplicativos pelo PID, pelo hint desktop-entry ou pelo nome. Para um aplicativo reconhecido, `FdoNotificationDaemonSource._onNameVanished()` destruía a fonte quando o remetente saía do D-Bus. Fontes genéricas não recebiam esse tratamento.

### Teste que isolou a causa

| Teste | Resultado visual confirmado |
|---|---|
| Remetente termina; sem desktop-entry | Banner aparece |
| Remetente termina; desktop-entry=whatsapp | Banner não aparece |
| Remetente termina; identidade inexistente | Banner aparece |
| desktop-entry=whatsapp; conexão mantida por 15 s | Banner aparece |

Em um controle, o GNOME devolveu um ID e fechou a notificação cerca de 6 ms depois. Isso demonstra por que sucesso na chamada não basta.

### Caminho no Pake

`Pake → tauri-plugin-notification → notify-rust → zbus → GNOME`.

O plugin descarta o handle retornado pelo envio. O backend zbus do notify-rust criava uma conexão por envio, e o handle a mantinha viva. Descartá-lo encerrava o remetente, apesar de o aplicativo continuar aberto.

**Patch:** `patches/notify-rust-keep-connection.patch`, já aplicado em `vendor/notify-rust`. Um `OnceLock` mantém uma conexão de sessão compartilhada pelo processo, inclusive depois de o plugin descartar o handle. Esta é uma correção local, não uma alegação de que já foi incorporada upstream. Se a conexão de sessão for substituída após uma falha do barramento, reinicie o aplicativo: este patch não implementa reconexão automática.

### Validação original

Em 28/10/2026, no CachyOS/GNOME Shell 51.1/Wayland:

1. O usuário executou `new Notification(...)` com um título sintético no build corrigido.
2. O banner apareceu.
3. Foi confirmado que o remetente pertencia ao executável corrigido.
4. `NameHasOwner` permaneceu true após 1, 5, 15 e 30 segundos.
5. O usuário enviou uma mensagem de outra conta WhatsApp e confirmou a notificação real.

Não há evidência registrada separadamente sobre a permanência no histórico. A correção no Pake não muda o comportamento de `notify-send` que termina imediatamente; para esse teste isolado, use `notify-send --wait`.

`X-GNOME-UsesNotifications=true` é apenas metadado de integração no launcher deste projeto. O teste com conexão mantida já funcionava sem essa chave; ela não é a explicação da correção.

## 2. Botão X não responde

O usuário confirmou que o X não fazia nada, mas Alt+F4 ocultava a janela. Redimensionar também fazia o X voltar a responder. Isso distinguiu o problema de interação da barra de título do comportamento intencional `hide_on_close=true`.

Tao 0.34.5 inseria uma GtkHeaderBar em um EventBox customizado no Wayland. A adaptação local remove a criação dessa decoração e deixa o GTK fornecer a decoração padrão.

**Patch:** `patches/tao-native-gtk-decorations.patch`, já aplicado em `vendor/tao`. É um recorte adaptado da abordagem upstream, não a aplicação completa do PR 1218. O patch mantém as versões das demais dependências.

O usuário validou o X na nova versão, reabriu pela bandeja e confirmou que o X continuava funcionando na segunda tentativa.

Referências primárias:
- [Tauri #15460: botões sem resposta após restaurar](https://github.com/tauri-apps/tauri/issues/15460), com relato no KDE/Wayland.
- [Tao #1046: decorações customizadas no Wayland](https://github.com/tauri-apps/tao/issues/1046), incluindo relatos sobre GNOME e hide/show.
- [Tao PR #1218: correção de decorações e eventos](https://github.com/tauri-apps/tao/pull/1218).

## 3. Regressão: a barra de título não arrasta a janela

Em 30/10/2026, o usuário relatou que a barra de título não permitia mover a janela. A primeira adaptação do PR 1218 havia removido a decoração customizada, mas não incluía as mudanças de propagação de eventos necessárias para o GTK padrão.

No Tao 0.34.5, os handlers de movimento, pressionamento e soltura do mouse retornavam `glib::Propagation::Stop`. O GTK não recebia esses eventos para executar o arraste nativo da barra. A correção completa essa parte da adaptação: usa `Proceed` e evita o encaminhamento duplicado de eventos ao Tao, preservando os controles da janela.

**Patch:** `patches/tao-gtk-event-propagation.patch`, extraído do commit upstream [`07f3742b`](https://github.com/tauri-apps/tao/commit/07f3742b) / PR 1218 e aplicado sem alterações de conteúdo à cópia local. Foram ajustados apenas os offsets de aplicação. O patch de notificações permanece inalterado.

Validação em 30/10/2026: compilação otimizada concluída com sucesso e patch conferido contra o diff upstream. O usuário confirmou que o arraste funciona antes e depois de ocultar/reabrir, mantendo o X e os cliques dentro do WhatsApp funcionando. A correção é incluída na versão 1.0.2.

## 4. O que foi preservado

- URL `https://web.whatsapp.com` e configuração de janela do aplicativo original.
- Identidade `com.pake.ab7ae24`, para preservar o perfil nas atualizações locais.
- X oculta; bandeja reabre; Sair/Quit encerra.
- DevTools habilitado explicitamente em builds otimizados.

Não foi necessário desabilitar extensões, reinstalar GNOME, apagar dconf, copiar cookies ou editar código do GNOME. Os relatórios públicos omitem nomes de máquina, caminhos pessoais, IDs de processos e conteúdo de conversas.
