def make_request(row):

    redacao = row.texto_original
    tema = row.tema
    titulo = row.titulo

    CRITERIO_1 = "Demonstrar domínio da norma culta da língua escrita."
    CRITERIO_2 = "Compreender a proposta da redação e aplicar conceito das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo."
    CRITERIO_3 = "Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista."
    CRITERIO_4 = "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação."
    CRITERIO_5 = "Elaborar a proposta de solução para o problema abordado, mostrando respeito aos valores humanos e considerando a diversidade sociocultura"


    CONTEXTO = f'''Você é um avaliador de redações e irá avaliar uma redação do assunto {tema} considerando os 5 critérios a seguir:
            Critério 1. {CRITERIO_1}
            Critério 2. {CRITERIO_2} 
            Critério 3. {CRITERIO_3}
            Critério 4. {CRITERIO_4} 
            Critério 5. {CRITERIO_5}

            Para cada critério deve ser dada uma nota de 0 a 200. Sendo que você deve ser rigoroso!
            
    '''
    ENTRADA_REDACAO = f'''O tema da redação é "{tema}" e o escritor deu o título de "{titulo}". Esta é a redação: 
    """{redacao}"""
    '''
    FORMATO_DE_SAIDA = '''A saída deve ser no formato JSON, com aspas duplas sem formatc:
        {
            "criterio_1":(nota, detalhes),
            "criterio_2":(nota, detalhes),
            "criterio_3":(nota, detalhes),
            "criterio_4":(nota, detalhes),
            "criterio_5":(nota, detalhes),
            "avaliacao_geral': cometários gerais sobre o texto,
            "nota_final': soma das notas dos critérios
        }

    '''
    EXEMPLO_1 = make_exemplo(0)
    EXEMPLO_2 = make_exemplo(2)

    messages=[ {"role": "system", "content": CONTEXTO},
                {"role": "system", "content": FORMATO_DE_SAIDA},
                {"role": "system", "content": EXEMPLO_1},
                {"role": "system", "content": EXEMPLO_2},
                {"role": "user", "content": ENTRADA_REDACAO},
            ]
        #
        #
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    output = response.choices[0].message['content'].strip()
    output = eval(output)
    return output
    