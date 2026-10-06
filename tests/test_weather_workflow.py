import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from weather_logic import montar_resposta, normalizar_cidade  # noqa: E402


class WeatherWorkflowTests(unittest.TestCase):
    def test_normaliza_cidade_com_acentos_e_espacos(self):
        self.assertEqual(normalizar_cidade("  São   Paulo,SP,BR  "), "sao   paulo,sp,br")

    def test_formata_tres_respostas_de_cidades(self):
        exemplos = [
            ({"cod": 200, "name": "São Paulo", "main": {"temp": 23.6}}, "São Paulo,SP,BR", "São Paulo", "24°C"),
            ({"cod": "200", "name": "Recife", "main": {"temp": 28.2}}, "Recife,PE,BR", "Recife", "28°C"),
            ({"name": "Curitiba", "main": {"temp": 16}}, "Curitiba,PR,BR", "Curitiba", "16°C"),
        ]
        for payload, query, city, temperature in exemplos:
            with self.subTest(city=city):
                result = montar_resposta(payload, query)
                self.assertTrue(result["ok"])
                self.assertIn(city, result["message"])
                self.assertIn(temperature, result["message"])

    def test_falha_de_cidade_e_resposta_incompleta_sao_amigaveis(self):
        for payload in ({"cod": 404, "message": "city not found"}, {"cod": 200, "name": "X"}, None):
            with self.subTest(payload=payload):
                result = montar_resposta(payload, "Cidade Inventada,ZZ,BR")
                self.assertFalse(result["ok"])
                self.assertIn("Cidade não encontrada", result["message"])

    def test_exportacao_n8n_tem_gatilho_http_seguro_e_duas_respostas(self):
        workflow_path = ROOT / "workflow-chatbot-telegram.json"
        workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
        nodes = {node["name"]: node for node in workflow["nodes"]}
        self.assertEqual(nodes["Telegram Trigger"]["type"], "n8n-nodes-base.telegramTrigger")
        self.assertEqual(nodes["Consultar OpenWeather"]["parameters"]["url"], "https://api.openweathermap.org/data/2.5/weather")
        query = nodes["Consultar OpenWeather"]["parameters"]["queryParameters"]["parameters"]
        self.assertIn({"name": "appid", "value": "={{ $env.OPENWEATHER_API_KEY }}"}, query)
        self.assertEqual(nodes["Preparar consulta"]["parameters"]["assignments"]["assignments"][0]["name"], "queue")
        self.assertIn("Enviar temperatura", workflow["connections"]["Cidade encontrada?"]["main"][0][0]["node"])
        self.assertIn("Orientar sobre a cidade", workflow["connections"]["Cidade encontrada?"]["main"][1][0]["node"])
        serialized = json.dumps(workflow)
        self.assertNotIn("TELEGRAM_BOT_TOKEN", serialized)
        self.assertNotIn("OPENWEATHER_API_KEY=", serialized)


if __name__ == "__main__":
    unittest.main()
