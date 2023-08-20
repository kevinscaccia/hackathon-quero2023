def make_request(row):
    global output
    redacao = row.texto_original
    tema = row.tema
    titulo = row.titulo

    CRITERIO_1 = "Demonstrar domínio da norma culta da língua escrita."
    CRITERIO_2 = "Compreender a proposta da redação e aplicar conceito das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo."
    CRITERIO_3 = "Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista."
    CRITERIO_4 = "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação."
    CRITERIO_5 = "Elaborar a proposta de solução para o problema abordado, mostrando respeito aos valores humanos e considerando a diversidade sociocultura"

    CRITERIO_1_NOTA = """200 pontos: Excelente domínio da escrita formal da língua portuguesa.
    160 pontos: Bom domínio da escrita formal com poucos desvios gramaticais.
    120 pontos: Domínio mediano da escrita formal, com alguns desvios gramaticais.
    80 pontos: Domínio insuficiente da escrita formal com muitos desvios gramaticais.
    40 pontos: Domínio precário da escrita formal d com diversificados e frequentes desvios gramaticais.
    0 pontos: Desconhecimento da  escrita formal da língua portuguesa."""
    CRITERIO_2_NOTA = """200 pontos:Argumentação consistente, a partir de um repertório sociocultural produtivo e apresenta excelente dominio do texto dissertativo-argumentativo.
    160 pontos: Argumentação consistente e apresenta bom domínio do texto dissertativo-argumentativo, com parágrafos de proposição, argumentação e conclusão.
    120 pontos: Argumentação previsível e apresenta domínio mediano do texto dissertativo-argumentativo, com parágrafos de  proposição, argumentação e conclusão.
    80 pontos: Apresenta domínio insuficiente do texto dissertativo-argumentativo, não atendendo à estrutura com parágrafos de  proposição, argumentação e conclusão. 
    40 pontos: Apresenta o assunto, tangenciando o tema, ou demonstra dominio precário do texto dissertativo-argumentativo, com traços constantes de outros tipos textuais. 
    O pontos: Fuga ao tema/não atendimento à estrutura dissertativo-argumentativa"""
    CRITERIO_3_NOTA = """200 pontos: Apresenta informações, fatos e opiniões relacionados ao tema proposto, de forma consistente e organizada, configurando autoria em defesa de um ponto de vista.
    160 pontos: Informações relacionados ao tema, de forma organizada, com indícios de autoria, em defesa de um ponto de vista.
    120 pontos: informações relacionados ao tema, limitados aos argumentos dos textos motivadores e pouco organizados.
    80 pontos: informações relacionados ao tema, mas desorganizados ou contraditórios e limitados aos argumentos dos textos motivadores.
    40 pontos: informações pouco relacionados ao tema ou incoerentes e sem defesa de um ponto de vista. 
    O pontos: informações, fatos e opioniões não relacionadas ao tema e sem defesa de um ponto de vista"""
    CRITERIO_4_NOTA = """200 pontos: Articula bem as partes do texto e apresenta repertório diversificado de recursos coesivos.
    160 pontos: Articula as partes do texto, com poucas inaquações, e apresenta repertório diversificado de recursos coesivos.
    120 pontos: Articula as partes do texto, de forma mediana, com inadequações, e apresenta repertório pouco diversificado de recursos coesivos.
    80 pontos:Articula as partes do texto, de forma insuficiente, com muitas inaqueações e apresenta repertório limitado de recursos coesivos. 
    40 pontos: Articula as partes do texto de forma precária. 
    O pontos: Não articula as informações."""
    CRITERIO_5_NOTA = """200 pontos: Elabora muito bem proposta de intervenção, detalhada, relacionada ao tema e artivulada à discussão desenvolvida no texto.
    160 pontos: Elabora bem proposta de intervenção relacionada ao tema e articula à discussão desenvolvida no texto.
    120 pontos: Elabora, de forma mediana, proposta de intervenção relacionada ao tema e articulada à discussão desenvolvida no texto.
    80 pontos: Elabora, de forma insuficiente, proposta de intervenção relacionada ao tema, ou não articulada com a discussão desenvolvida no texto. 
    40 pontos: Apresenta proposta de intervenção vaga, precária ou relacionada apenas ao assunto. 
    O pontos: Não apresenta proposta de intervenção ou apresenta proposta não relacionada ao tema ou ao assunto."""

    CONTEXTO_1 = f'''Você é um avaliador de redações e irá avaliar uma redação do assunto {tema} considerando os 5 critérios a seguir:
            CRITÉRIO 1. {CRITERIO_1_NOTA}
            CRITÉRIO 2. {CRITERIO_2_NOTA}
            CRITÉRIO 3. {CRITERIO_3_NOTA}
            CRITÉRIO 4. {CRITERIO_4_NOTA} 
            CRITÉRIO 5. {CRITERIO_5_NOTA}
            Para cada critério deve ser dada uma nota de 0 a 200. Sendo que você deve ser rigoroso!'''
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
            "avaliacao_geral": cometários gerais sobre o texto,
            "nota_atribuida": soma das notas dos critérios
        }

    '''
    EXEMPLO_1 = make_exemplo(0)
    EXEMPLO_2 = make_exemplo(2)

    messages = [{"role": "system", "content": CONTEXTO_1},
                {"role": "assistant", "content": FORMATO_DE_SAIDA},
                {"role": "assistant", "content": EXEMPLO_1},
                {"role": "assistant", "content": EXEMPLO_2},
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
