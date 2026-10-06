# Bot de clima no Telegram com n8n

Workflow importável que recebe o nome de uma cidade no Telegram, consulta a API atual do OpenWeather e devolve a temperatura em Celsius. O fluxo valida a resposta antes de formatá-la e orienta o usuário quando a consulta falha.

## Arquivos

- `workflow-chatbot-telegram.json`: exportação para importar no n8n.
- `weather_logic.py`: funções puras usadas para validar e testar os exemplos sem credenciais.

## Configuração

1. Crie um bot no Telegram pelo BotFather e guarde o token em `TELEGRAM_BOT_TOKEN` no ambiente seguro usado para provisionar sua instância. No n8n, adicione uma credencial **Telegram API** usando esse token; o token fica armazenado na credencial criptografada, não no workflow.
2. Crie uma chave de API no OpenWeather e configure `OPENWEATHER_API_KEY` nas variáveis de ambiente do n8n.
3. Reinicie o n8n para carregar a variável, importe `workflow-chatbot-telegram.json` e selecione a credencial Telegram nos nós **Telegram Trigger**, **Enviar temperatura** e **Orientar sobre a cidade**.
4. Ative o workflow e envie ao bot uma cidade, por exemplo `São Paulo,SP,BR`.

O campo `appid` é lido de `{{$env.OPENWEATHER_API_KEY}}`. `TELEGRAM_BOT_TOKEN` é usado na configuração da credencial Telegram, não como campo do workflow. Nenhuma chave ou token real está incluído nos arquivos.

## Exemplos de resposta

Consulta bem-sucedida:

```text
🌤️ A temperatura em São Paulo é de 24°C.
```

Cidade inválida, falha HTTP ou resposta incompleta:

```text
❌ Cidade não encontrada. Use o formato Cidade,UF,BR (ex.: São Paulo,SP,BR).
```

## Testes locais

Na raiz deste repositório, execute:

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem três cidades de exemplo, normalização de acentos, arredondamento, falha de cidade e a estrutura do workflow. Os testes locais validam a lógica Python e a estrutura do export. O teste ponta a ponta no Telegram/OpenWeather precisa de uma instância n8n e das credenciais configuradas.
