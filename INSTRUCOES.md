# Rotina automática do Instagram @sportech (CoolerBag)

Este repositório guarda tudo o que as tarefas automáticas precisam: as fotos, o gerador de artes, os dados do produto, o histórico e os aprendizados. Cada execução começa do zero, então **leia este arquivo inteiro antes de agir**.

O dono quer **tudo 100% automático**. Não peça aprovação, não deixe posts como rascunho e não use etiqueta de link nos stories, porque o Instagram não permite isso na publicação automática. Fale com ele em português do Brasil, de forma simples.

---

## Dados fixos
- Metricool: blogId/brandId **7908479**, fuso **America/Sao_Paulo**, rede **instagram** (perfil @sportech).
- Repositório: `sportech338/sportech-posts` (público). Imagens publicadas em `https://raw.githubusercontent.com/sportech338/sportech-posts/main/posts/<data>/<arquivo>.png`.
- Produto e regras do que pode ou não ser dito: `produto/coolerbag.md`. **Siga as regras de "NÃO afirmar" sempre.**
- Fotos disponíveis: `fotos/fotos.json`. Use só os nomes que estão lá.
- O que já foi postado: `historico.json`.
- Ajustes vindos das métricas: `aprendizados.md`. Eles têm prioridade sobre as sugestões deste arquivo.

---

## ROTINA DIÁRIA (gerar e agendar as 6 publicações)

### 1. Preparar
1. Anexe o repositório com permissão de escrita (add_repo: owner `sportech338`, repo `sportech-posts`, access `push`). Clone com `git clone --depth 1` e entre na pasta. Se o clone for raso, rode `git pull` antes de mexer.
2. Descubra a data-alvo no fuso de São Paulo. Se a execução acontecer **antes das 9h30**, a data-alvo é **hoje**. Se for depois, a data-alvo é **amanhã**, para não agendar no passado.
3. **Confira se os posts dos últimos 2 dias foram publicados.** Use getScheduledPosts de anteontem 00:00 até hoje 23:59 e veja o `status` de cada post. Se algum estiver como `ERROR`, **pare a rotina**: não gere nem agende nada, mande uma notificação ao dono com o `detailedStatus` exato (por exemplo "You have reached your Metricool account limit.") e encerre. O plano grátis do Metricool só publica 20 posts por mês, com o limite zerando no dia 1.
4. Use o Metricool (getScheduledPosts, brandId 7908479, da data-alvo 00:00 até 23:59) para checar o que já está agendado. Se já houver publicações não-rascunho nos horários da rotina, **não duplique**. Agende só o que falta e explique isso no resumo.

### 2. Tipo do dia
Calcule o **dia do ano** da data-alvo (1 a 366).
- **Par = Dia A:** feed às 10h com **carrossel**, às 17h com **post** e às 20h com **carrossel**.
- **Ímpar = Dia B:** feed às 10h com **post**, às 17h com **carrossel** e às 20h com **post**.
- **Stories, todo dia:** 10h, 12h e 18h.
Se `aprendizados.md` mudar formatos ou horários, siga o que estiver lá.

### 3. Planejar o conteúdo
Leia `produto/coolerbag.md`, `fotos/fotos.json`, `historico.json` (os últimos 14 dias) e `aprendizados.md`. Depois escreva `planos/<data>.json` no mesmo formato de `planos/2026-11-06.json`. Esse arquivo é o exemplo completo.

**Variedade (obrigatório):**
- Não repita um **tema** de feed que apareceu nos últimos 7 dias.
- Não use a mesma **foto** como capa ou foto principal de feed em dois dias seguidos.
- Varie os **layouts** de um dia para o outro.
- Os 3 stories do dia devem ter temas diferentes entre si. Um deles deve sempre ser de oferta ou preço.

**Banco de temas** (misture, crie variações e invente outros dentro das regras):
- Cooler tradicional x CoolerBag (peso, mãos livres, praticidade)
- Mãos livres e vai nas costas
- Tamanhos 18, 20 e 23L, quantas latas cabem e o "você sabia" de que a 23L custa só R$ 10 a mais
- Cores (preta, azul, cinza) e "qual é a sua?"
- Dicas para a bebida ficar gelada por mais tempo
- Ocasiões: praia, piscina, churrasco, trilha, camping, viagem de carro, jogo no estádio ou na TV, pescaria, festa, aniversário, show ao ar livre
- Checklist "o que levar para a praia" e "o que levar para o churrasco"
- Perguntas frequentes: posso usar gelo? lanche pode? como limpar? o que vem na caixa?
- Prova social: nota 5,0 com 75 avaliações. Não invente depoimentos.
- Oferta: a partir de R$ 169,90, frete grátis, até 12x, 3% off no Pix
- Bolsos e organização: celular, chaves, garrafinha no bolso lateral
- Datas sazonais: verão, férias, fim de ano e réveillon, Carnaval, Dia dos Pais e outras. Sem inventar promoções: use preço e condições só como estão em `produto/coolerbag.md`.

**Textos:**
- Use português do Brasil, num tom leve, de verão e de rolê com os amigos.
- Títulos nas artes devem ser curtos, com no máximo 6 palavras em `titulo` e 6 em `destaque`. Os textos de apoio devem ter no máximo 2 frases.
- Todo story termina com o CTA **"Link na bio 👆"** ou uma variação, como "Garanta a sua no link da bio 👆". Nunca escreva "toque no link" ou "arraste para cima".
- Legenda do feed: gancho na primeira linha, de 3 a 6 linhas de valor ou benefício, uma pergunta para gerar comentário, o CTA "👉 Link na bio" e de 4 a 8 hashtags, sempre com #coolerbag e #sportech.
- Carrosséis têm de 4 a 7 slides. O primeiro slide é sempre `capa` e o último é sempre `cta`.

**Layouts disponíveis** (campos comuns: `titulo`, `destaque`, `texto`, `foto`, `foco`, `cta`, `chips`, `preco`, `prefixo`):
- Stories: `story_foto` (foto em tela cheia com texto embaixo), `story_cores` (as 3 cores, sem foto), `story_oferta` (foto e painel de preço), `story_frase` (frase forte com foto redonda).
- Posts: `post_oferta` (foto em cima e preço embaixo), `post_foto` (foto em tela cheia com título), `post_frase` (frase grande com foto em card).
- Slides de carrossel: `capa`, `foto_tag` (foto com etiqueta, que usa `tag`), `foto_numero` (foto com número, que usa `numero`), `tamanhos` (tabela 18, 20 e 23L), `texto` (só texto, com `fundo` `escuro` ou `claro`), `cta` (fechamento com oferta).
- `foco` é a posição vertical do recorte da foto, por exemplo `"20%"` para mostrar mais a parte de cima. Use quando a cabeça ou o produto estiverem cortados.

### 4. Gerar e conferir as artes
1. Rode `python3 gerador/render.py planos/<data>.json`.
2. Se aparecer **"ATENÇÃO"**, encurte o texto daquela arte no plano e gere de novo.
3. **Abra `posts/<data>/previa.png` com a ferramenta Read e confira visualmente.** Veja se há texto cortado ou sobreposto, se a foto ficou mal recortada (cabeça cortada, produto fora do quadro) e se os textos têm erros. Corrija no plano e gere de novo até ficar bom.

### 5. Publicar as imagens
1. Rode `git pull --rebase` e depois `git add planos posts historico.json`.
2. Faça o commit com a mensagem `Posts <data>` e o rodapé de atribuição indicado pelo sistema. Depois rode `git push`.
3. Confira se as URLs abrem, com `curl -s -o /dev/null -w "%{http_code}"` em uma URL de cada publicação, que deve retornar 200. Se der 404, espere 30 segundos e tente de novo, até 5 vezes.

### 6. Agendar no Metricool
Use `posts/<data>/manifesto.json` e chame **createScheduledPost** uma vez por publicação:
- `blogId`: `"7908479"`
- `date`: `<data>T<hora>:00-03:00`
- `info` deve conter:
  - `autoPublish`: true, `draft`: false
  - `providers`: `[{"network":"instagram"}]`
  - `publicationDate`: `{"dateTime":"<data>T<hora>:00","timezone":"America/Sao_Paulo"}`
  - `media`: a lista de URLs do manifesto, na ordem. Um carrossel é um POST com várias imagens.
  - `text`: a legenda. Para **stories, não mande `text`**.
  - `instagramData`: `{"type":"POST"}` para post e carrossel, `{"type":"STORY"}` para story, sempre com `"isAiGenerated": true`, porque as fotos são geradas por IA.
  - `firstCommentText`: "", `hasNotReadNotes`: false, `shortener`: false, `smartLinkData`: `{"ids":[]}`, `descendants`: [], `mediaAltText`: []
- Se der erro, relate exatamente o erro no resumo. Não tente contornar publicando de outro jeito.

### 7. Registrar e avisar
1. Acrescente a data em `historico.json`, com o tipo do dia, os temas, as fotos principais e os IDs do Metricool. Faça commit e push.
2. A última mensagem da execução deve ser um **resumo curto para o dono**, com o que foi agendado em cada horário, o tema e o formato. Inclua também qualquer problema encontrado.

---

## ROTINA SEMANAL (relatório de métricas, toda segunda)

1. Prepare o repositório como no passo 1 da rotina diária.
2. Use o Metricool para ver as métricas disponíveis do Instagram (getAnalyticsAvailableMetrics) e buscar os dados dos **últimos 7 dias** (getAnalyticsDataByMetrics), tanto do perfil (seguidores, alcance, visitas) quanto de cada post, story e carrossel. Use também getBestTimeToPostByNetwork para os próximos 7 dias.
3. Cruze os dados com `historico.json`, usando a data e a hora, para saber o tema e o formato de cada publicação.
4. Escreva o relatório para o dono, curto e em linguagem simples:
   - Resumo da semana: seguidores ganhos, alcance total e engajamento.
   - Os 3 melhores e os 3 piores conteúdos, com o motivo provável.
   - O desempenho por formato (carrossel, post e story) e por horário.
   - O que vai mudar na próxima semana.
   - Nas primeiras 3 semanas, avise que ainda há poucos dados.
5. Atualize `aprendizados.md` com regras objetivas para a rotina diária. Por exemplo: "priorizar carrosséis de dicas", "evitar tema X" ou "trocar o post das 20h para 19h". Só faça mudanças de horário quando houver dados de pelo menos 2 semanas. Faça commit e push.
6. **A cada 2 semanas**, nas segundas em que o número da semana ISO for par, lembre o dono de mandar **10 fotos novas** da CoolerBag. Diga também quais fotos estão mais repetidas, consultando `historico.json`.

---

## Fotos novas (quando o dono mandar numa conversa)
1. Recorte as fotos para tirar textos e selos embutidos.
2. Salve em `fotos/<nome_descritivo>.jpg` e descreva cada uma em `fotos/fotos.json`. Marque `"fundo_branco": true` quando a foto for de produto em fundo branco.
3. Não use fotos de "antes e depois" nem fotos em que apareça a marca de outra empresa, como "WETPACK".
4. Faça commit e push.
