# Bot de clima no Telegram com n8n

Workflow importável que recebe uma mensagem de texto, normaliza o nome da cidade, consulta a API OpenWeather e responde com a temperatura em Celsius. Respostas HTTP inválidas, cidades não encontradas e campos incompletos seguem um caminho de erro com orientação de formato.

## Requisitos

- Uma instância n8n compatível com os nós Telegram, HTTP Request, Code, If e Edit Fields/Set.
- Um bot criado pelo BotFather e uma credencial **Telegram API** configurada no n8n.
- Uma chave OpenWeather configurada no ambiente do n8n como `OPENWEATHER_API_KEY`.

## Importar e configurar

1. Baixe ou clone este repositório.
2. No n8n, importe `workflow-chatbot-telegram.json`.
3. Selecione sua credencial Telegram API nos nós **Telegram Trigger**, **Enviar temperatura** e **Orientar sobre a cidade**.
4. Configure `OPENWEATHER_API_KEY` no ambiente do servidor n8n e reinicie a instância para carregar a variável.
5. Publique/ative o workflow e envie uma cidade ao bot, por exemplo `São Paulo, SP, BR`.

O nó HTTP usa `={{ $env.OPENWEATHER_API_KEY }}` para ler a chave. O acesso a `$env` depende da versão e da configuração da instância. Algumas instalações self-hosted usam `N8N_BLOCK_ENV_ACCESS_IN_NODE` para controlar esse acesso; desativar essa proteção pode expor variáveis de ambiente a expressões de workflows. Não altere essa configuração em uma instância compartilhada ou de produção só para executar este projeto. Para avaliação, prefira uma instância isolada com apenas `OPENWEATHER_API_KEY` disponível, seguindo a política do administrador. O token Telegram fica somente na credencial criptografada do n8n. Nenhum token ou chave real é salvo no JSON ou neste README.

## Comportamento esperado

- Remove espaços duplicados, acentos e diferenças entre maiúsculas/minúsculas antes de enviar a cidade como `queue`.
- Consulta `https://api.openweathermap.org/data/2.5/weather` com unidades métricas e idioma português do Brasil.
- Responde com o nome da cidade e temperatura arredondada em Celsius.
- Em caso de cidade inválida, erro HTTP ou resposta incompleta, responde: `❌ Cidade não encontrada. Use o formato Cidade,UF,BR (ex.: São Paulo,SP,BR).`

## Testes

Na pasta do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Os testes offline conferem normalização, respostas de São Paulo, Recife e Curitiba, arredondamento, falhas e os nós/conexões/variáveis esperados no arquivo de exportação. A exportação inclui o ID do workflow e foi importada por uma instalação isolada do CLI oficial do n8n. Um teste ponta a ponta no Telegram e OpenWeather precisa das credenciais e de uma instância n8n configuradas pelo proprietário da conta.
