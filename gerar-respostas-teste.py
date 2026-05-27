#!/usr/bin/env python3
"""Gera respostas de teste variadas e envia pro Apps Script."""

import json
import urllib.request
import random
from datetime import datetime, timezone, timedelta

WEBHOOK = "https://script.google.com/macros/s/AKfycbymfHZmYyT-vLQ7QFdXMKlOED3XuQbsTZgsoYGIAo8mESWLF2WTLiPvb0zxEZfJIRjlFQ/exec"

NOMES = [
    "Ricardo Almeida", "Maria Clara Souza", "Pedro Henrique Santos",
    "Camila Oliveira", "Lucas Ferreira", "Beatriz Costa", "Rafael Gomes",
    "Juliana Martins", "Bruno Lima", "Fernanda Rocha", "Diego Carvalho",
    "Patrícia Nunes", "Thiago Ribeiro", "Amanda Pereira"
]

EMAILS = [
    "ricardo.almeida@gmail.com", "mclara.souza@hotmail.com",
    "pedrohenrique@outlook.com", "camilaoliv@gmail.com",
    "lucas.ferreira88@gmail.com", "bia.costa@gmail.com",
    "rafa.gomes@yahoo.com.br", "ju.martins@gmail.com",
    "brunolima.trader@gmail.com", "fernanda.rch@gmail.com",
    "diego.carvalho@outlook.com", "paty.nunes@gmail.com",
    "thiago.rb@gmail.com", "amandaper@hotmail.com"
]

FONES = [
    "(11) 98765-4321", "(21) 99988-7766", "(31) 98877-6655",
    "(41) 99765-1122", "(51) 98654-3322", "(11) 97123-4567",
    "(85) 98112-3344", "(48) 99225-1188", "(11) 99876-5432",
    "(62) 98711-2233", "(34) 99888-7711", "(81) 98234-5566",
    "(11) 99123-4567", "(19) 98655-4433"
]

MOTIVOS_NPS = [
    "Conteúdo muito sólido, saí com clareza.",
    "Energia e prática, o que eu precisava.",
    "Senti que mudou minha forma de pensar.",
    "Muito além do que eu esperava, parabéns.",
    "Bem feito, com profundidade real.",
    "Conteúdo bom, mas faltou ritmo em alguns momentos.",
    "O melhor evento que já fui nesse tema.",
    "Ajudou demais a destravar onde eu tava parado.",
    "Sacra acertou a mão. Recomendo de olho fechado.",
    "Valeu muito o investimento.",
    "Bem direcionado pra quem é trader de verdade.",
    "Conteúdo aplicado e direto, sem encheção."
]

INSIGHTS = [
    "Entendi que meu problema não é estratégia, é comportamento.",
    "A virada de chave foi sobre gerenciamento de risco.",
    "Percebi que eu tava operando sem plano. Agora não tô mais.",
    "O conceito de identidade do trader mudou tudo pra mim.",
    "Aprendi que disciplina é mais importante que setup.",
    "Achei que ia ver mais setup, mas o ouro foi a parte de mente.",
    "A análise de dados de lançamento abriu minha cabeça.",
    "Saí entendendo que tenho que parar de operar emoção."
]

DESTRAVOU = [
    "Destravou minha relação com perda. Antes era pessoal.",
    "Destravou a forma de planejar a semana.",
    "Destravou minha relação com dinheiro.",
    "Destravou o medo de operar valores maiores.",
    "Destravou minha disciplina pra estudar todo dia.",
    "Clareou que eu tava tentando vencer o mercado, não me adaptar a ele."
]

SENTIMENTO_POS = ["Muito mais confiante", "Muito mais confiante", "Muito mais confiante", "Mais confiante", "Mais confiante", "Igual"]
APLICACAO_OPCOES = ["Sim, várias coisas", "Sim, várias coisas", "Sim, algumas coisas", "Sim, algumas coisas", "Ainda não, mas pretendo aplicar", "Ainda não consegui aplicar"]
APLICACAO_TEXTOS = [
    "Já reduzi o tamanho da posição e tô seguindo o plano.",
    "Apliquei o stop fixo e melhorou meu controle emocional.",
    "Comecei a registrar todo trade num diário.",
    "Já estou estudando 1h por dia antes do mercado abrir.",
    "Mudei meu setup pra menos operações e mais qualidade."
]

EXPECTATIVA = ["Superou muito", "Superou muito", "Superou", "Superou", "Atendeu"]
NETWORKING = ["Excelente", "Excelente", "Boa", "Boa", "Boa", "Média"]
RESULTADOS = ["Resultado financeiro", "Resultado comportamental", "Resultado de gerenciamento"]

PALESTRA_MARCANTE = [
    "A palestra do Sacra sobre identidade. Foi visceral.",
    "Bernardo falando de criativos abriu minha cabeça.",
    "A parte de gerenciamento ficou marcada.",
    "A abertura do evento me arrepiou.",
    "O bloco sobre mindset foi o que mais me marcou."
]

MOMENTO_MARCANTE = [
    "O momento da oração no início.",
    "Quando ele falou da filha. Não tem como não se emocionar.",
    "A energia do grupo no segundo dia.",
    "O networking do almoço.",
    "Quando todo mundo se levantou no encerramento."
]

PROXIMOS_ENCONTROS = [
    "Mais momentos práticos em dupla.",
    "Mais conteúdo de IA aplicada ao trade.",
    "Trazer convidados externos do mercado.",
    "Workshop hands-on de gerenciamento.",
    "Mais tempo de Q&A com o Sacra."
]

FALTOU_OQUE = [
    "Senti falta de mais conteúdo prático sobre IA.",
    "Faltou um pouco de tempo pra perguntas.",
    "Mais material pra estudar depois do evento."
]

FRASES_RESUMO = [
    "Direção.",
    "Transformação real.",
    "Virada de chave.",
    "Hora de assumir responsabilidade.",
    "O começo de uma nova fase.",
    "Despertar.",
    "Recalibragem."
]

ANTES_DEPOIS = [
    "Tava perdido, agora tenho um plano.",
    "Estava operando no improviso, agora tenho método.",
    "Antes operava por impulso. Agora opero por sistema.",
    "Era um trader inseguro. Agora sei o que tô fazendo.",
    "Tava prestes a desistir. Agora sei que vou conseguir."
]

MENSAGEM_SACRA = [
    "Sacra, valeu por jogar limpo. Você mudou minha vida.",
    "Continue assim, mano. O legado tá sendo construído.",
    "Obrigado por compartilhar tanto sem segurar nada.",
    "Você tem uma missão. Tô junto.",
    "Que Deus continue te abençoando. Você é uma referência pra mim.",
    "Sacra, sua história me deu coragem pra continuar.",
    "Gratidão eterna. Continua firme."
]

def pick(lst):
    return random.choice(lst)

def build_response(i):
    """Gera uma resposta plausível."""
    # NPS: maioria 9-10, alguns 7-8, raros mais baixos
    r = random.random()
    if r < 0.65: nps = random.randint(9, 10)
    elif r < 0.90: nps = random.randint(7, 8)
    else: nps = random.randint(4, 6)

    aplic = pick(APLICACAO_OPCOES)
    quer_lista = random.random() < 0.75
    sentiu_falta = random.random() < 0.30

    # Avaliações 1-5 com média alta
    def aval(): return random.choices([3, 4, 5], weights=[5, 30, 65])[0]

    submitted = (datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 48), minutes=random.randint(0, 59))).isoformat()

    responses = {
        # Identificação (agora coletada no começo do formulário)
        "nome": NOMES[i % len(NOMES)],
        "email": EMAILS[i % len(EMAILS)],
        "telefone": FONES[i % len(FONES)],
        "nps": nps,
        "nps_motivo": pick(MOTIVOS_NPS),
        "expectativa": pick(EXPECTATIVA),
        "avaliacao_pontos_conteudo": aval(),
        "avaliacao_pontos_clareza": aval(),
        "avaliacao_pontos_aplicabilidade": aval(),
        "avaliacao_pontos_organizacao": aval(),
        "avaliacao_pontos_palestrantes": aval(),
        "avaliacao_pontos_energia": aval(),
        "avaliacao_pontos_network": aval(),
        "avaliacao_pontos_estrutura": aval(),
        "avaliacao_pontos_tempo": aval(),
        "avaliacao_pontos_suporte": aval(),
        "insight": pick(INSIGHTS),
        "destravou": pick(DESTRAVOU),
        "sentimento_pos": pick(SENTIMENTO_POS),
        "aplicacao": aplic,
        "palestra_marcante": pick(PALESTRA_MARCANTE),
        "momento_marcante": pick(MOMENTO_MARCANTE),
        "proximos_encontros": pick(PROXIMOS_ENCONTROS),
        "faltou": "Sim" if sentiu_falta else "Não",
        "networking_exp": pick(NETWORKING),
        "frase_resumo": pick(FRASES_RESUMO),
        "antes_depois": pick(ANTES_DEPOIS),
        "autoriza_depoimento": random.choice(["Sim", "Sim", "Sim", "Não"]),
        "mensagem_sacra": pick(MENSAGEM_SACRA),
        "obrigado": "",
        "lista_espera": "Sim, quero entrar" if quer_lista else "Agora não"
    }

    # Follow-ups condicionais
    if aplic in ["Sim, várias coisas", "Sim, algumas coisas"]:
        responses["aplicacao_oque"] = pick(APLICACAO_TEXTOS)

    if sentiu_falta:
        responses["faltou_oque"] = pick(FALTOU_OQUE)

    # Múltipla escolha de resultados
    qtd_resultados = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
    resultados = random.sample(RESULTADOS, qtd_resultados)
    responses["resultados"] = " | ".join(resultados)
    if "Resultado financeiro" in resultados:
        responses["resultados_financeiro"] = random.choice([
            "Fiz +R$ 8 mil no último mês.",
            "Recuperei tudo que tinha perdido em 3 semanas.",
            "Primeiros R$ 2.500 de lucro consistente.",
            "+R$ 15k em 6 semanas."
        ])
    if "Resultado comportamental" in resultados:
        responses["resultados_comportamental"] = random.choice([
            "Parei de operar por impulso.",
            "Tô mais calmo, mais paciente.",
            "Aprendi a aceitar perda sem entrar em tilt."
        ])
    if "Resultado de gerenciamento" in resultados:
        responses["resultados_gerenciamento"] = random.choice([
            "Defino stop antes de entrar e respeito.",
            "Reduzi muito o tamanho das operações, e melhorou tudo.",
            "Tô seguindo o plano de risco do evento à risca."
        ])

    if quer_lista:
        responses["waitlist_confirmado"] = ""

    return {
        "event": "Imersão GKT Legado",
        "startedAt": submitted,
        "submittedAt": submitted,
        "userAgent": "teste-script-python",
        "responses": responses
    }


def main():
    n = 20
    print(f"Enviando {n} respostas de teste pra planilha...\n")
    for i in range(n):
        payload = build_response(i)
        req = urllib.request.Request(
            WEBHOOK,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'text/plain'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                r.read()
            nome = payload['responses'].get('nome', '—')
            nps = payload['responses']['nps']
            lista = '★' if payload['responses'].get('lista_espera') == 'Sim, quero entrar' else ' '
            print(f"  {i+1:>2}/{n}  NPS {nps:>2}  {lista}  {nome}")
        except Exception as e:
            print(f"  {i+1:>2}/{n}  ERRO: {e}")
    print("\nPronto! Atualiza o dashboard pra ver os dados.")


if __name__ == "__main__":
    main()
