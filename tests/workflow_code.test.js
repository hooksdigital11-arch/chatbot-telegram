const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const workflow = JSON.parse(
  fs.readFileSync(path.join(__dirname, '..', 'workflow-chatbot-telegram.json'), 'utf8'),
);
const nodes = Object.fromEntries(workflow.nodes.map((node) => [node.name, node]));
const code = nodes['Validar e formatar resposta'].parameters.jsCode;
const queueExpression = nodes['Preparar consulta'].parameters.assignments.assignments[0].value;

function executeCode(payload) {
  const input = { first: () => ({ json: payload }) };
  return new Function('$input', code)(input)[0].json;
}

test('o Code node formata temperatura e nome da cidade', () => {
  const result = executeCode({ cod: 200, name: 'Recife', main: { temp: 24.5 } });
  assert.equal(result.ok, true);
  assert.equal(result.message, '🌤️ A temperatura em Recife é de 25°C.');
});

test('o Code node encaminha respostas inválidas e temperaturas não finitas para erro', () => {
  for (const payload of [
    { cod: 404, message: 'city not found' },
    { cod: 200, name: 'Recife' },
    { cod: 200, name: 'Recife', main: { temp: Number.NaN } },
    { error: 'request failed' },
  ]) {
    const result = executeCode(payload);
    assert.equal(result.ok, false);
    assert.match(result.message, /Cidade não encontrada/);
  }
});

test('o Code node rejeita temperatura ausente, nula ou vazia, mas aceita zero', () => {
  for (const rawTemp of [undefined, null, '', '   ']) {
    const result = executeCode({ cod: 200, name: 'Recife', main: { temp: rawTemp } });
    assert.equal(result.ok, false, `temperatura inválida: ${String(rawTemp)}`);
  }

  const zero = executeCode({ cod: 200, name: 'Recife', main: { temp: 0 } });
  assert.equal(zero.ok, true);
  assert.match(zero.message, /0°C/);
});

test('a expressão que cria queue normaliza acentos e espaços repetidos', () => {
  const expressionBody = queueExpression.slice(3, -2);
  const normalize = new Function('$json', `return (${expressionBody});`);
  assert.equal(
    normalize({ message: { text: '  São   Paulo,  SP, BR  ' } }),
    'sao paulo, sp, br',
  );
});
