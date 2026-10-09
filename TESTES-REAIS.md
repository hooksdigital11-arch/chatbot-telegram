# Testes reais do bot de clima

Integração real Telegram → n8n → OpenWeather → Telegram concluída em 09/10/2026, por volta de 11:45–11:46 UTC, usando o bot exclusivo `@hooks_rocketseat_clima_bot` e n8n 2.42.6 isolado.

| Entrada pelo Telegram Desktop | API | Resposta recebida | Execução n8n |
|---|---|---|---|
| São Paulo,SP,BR | 200; 24,39°C | São Paulo: 24°C | 8, success |
| Recife,PE,BR | 200; 28,02°C | Recife: 28°C | 4, success |
| Curitiba,PR,BR | 200; 21,21°C | Curitiba: 21°C | 5, success |
| CidadeInexistenteRocketseat,XX,BR | 404 | Orientação para usar Cidade,UF,BR | 6, success |
| São   Paulo,SP,BR, com espaços externos digitados | 200; 24,39°C | São Paulo: 24°C | 7, success |

As consultas foram normalizadas: acentos removidos, letras minúsculas e espaços consecutivos reduzidos. O Telegram removeu espaços externos ao enviar. Temperaturas arredondadas corretamente. Resultados conferidos na conversa e nos dados persistidos do n8n. Evidência visual arquivada no workspace local.

Uma primeira consulta de São Paulo ficou em execução, sem nenhum nó registrado (execução 3). A repetição padrão passou na execução 8; não se atribui sucesso à execução 3. As duas execuções anteriores à ativação retornaram 401 e não contam como validação de cidade inexistente.

Credenciais protegidas fora do repositório em `~/.config/rocketseat-clima`, com permissões restritas. Nenhuma chave ou token publicado. Proxy permitiu somente POST na rota específica com header secret; o editor não foi exposto.

O ambiente e túnel são temporários para teste, não hospedagem permanente. Após a validação, o webhook Telegram foi removido (confirmado vazio, zero atualizações pendentes), e n8n, proxy e túnel receberam encerramento. A retomada automática dos testes foi desativada. Para o bot responder novamente, é necessário iniciar uma instância n8n e publicar o workflow com as credenciais protegidas.
