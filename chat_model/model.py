import openai
import os

CRITERIO_1 = "Demonstrar domínio da norma culta da língua escrita."
CRITERIO_2 = "Compreender a proposta da redação e aplicar conceito das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo."
CRITERIO_3 = "Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista."
CRITERIO_4 = "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação."
CRITERIO_5 = "Elaborar a proposta de solução para o problema abordado, mostrando respeito aos valores humanos e considerando a diversidade sociocultura"

openai.api_key = os.environ['OPENAPI_KEY']

def make_request(redacao, tema, titulo):
    CONTEXTO = f'''
    Você é um avaliador de redações e irá pontuar uma redação do assunto {tema} considerando os critérios:
            CRITÉRIO 1. {CRITERIO_1}
            CRITÉRIO 2. {CRITERIO_2}
            CRITÉRIO 3. {CRITERIO_3}
            CRITÉRIO 4. {CRITERIO_4} 
            CRITÉRIO 5. {CRITERIO_5}
            Para cada critério deve ser dada uma nota de 0 a 200, junto com uma descrição do motivo dessa nota.'''
    ENTRADA_REDACAO = f'''O tema da redação é "{tema}" e o escritor deu o título de "{titulo}". Esta é a redação: 
    """{redacao}"""
    '''
    FORMATO_DE_SAIDA = '''A saída deve ser no formato JSON. Não usando aspas duplas no conteúdo dos campos:
        {
            "criterio_1":(nota, detalhes),
            "criterio_2":(nota, detalhes),
            "criterio_3":(nota, detalhes),
            "criterio_4":(nota, detalhes),
            "criterio_5":(nota, detalhes),
            "avaliacao_geral": "cometários gerais sobre o texto",
            "nota_atribuida": "soma das notas dos critérios"
        }'''
    messages = [{"role": "system", "content": CONTEXTO},
                {"role": "user", "content": ENTRADA_REDACAO + FORMATO_DE_SAIDA},
                ]
    #
    #
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4,
        max_tokens=1000,
    )
    output = response.choices[0].message['content'].strip()
    output = eval(output)
    return output


import pandas as pd


dataframe = pd.read_csv('../data/base_redacoes_final.csv')
dataframe = dataframe.rename(columns={'nota_final':'nota_real'})
instancia = dataframe.iloc[0].to_dict()

output = make_request(instancia['texto_original'], instancia['tema'], instancia['titulo'])
print(output)