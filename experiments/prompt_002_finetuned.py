
CRITERIO_1 = "Demonstrar domínio da norma culta da língua escrita."
CRITERIO_2 = "Compreender a proposta da redação e aplicar conceito das várias áreas de conhecimento para desenvolver o tema, respeitando a forma estrutural do texto dissertativo-argumentativo."
CRITERIO_3 = "Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista."
CRITERIO_4 = "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação."
CRITERIO_5 = "Elaborar a proposta de solução para o problema abordado, mostrando respeito aos valores humanos e considerando a diversidade sociocultura"
END = "\n\n###\n\n"
def make_instance(row):
    redacao = row.texto_original
    tema = row.tema
    titulo = row.titulo

    prompt = f'''Você é um avaliador de redações sobre "{tema}" e deve considerar os critérios a seguir:CRITÉRIO 1. {CRITERIO_1}CRITÉRIO 2. {CRITERIO_2}CRITÉRIO 3. {CRITERIO_3}CRITÉRIO 4. {CRITERIO_4} CRITÉRIO 5. {CRITERIO_5}
            Para cada critério dê uma nota de 0 a 200, descrevendo essa atribuição.
            O título da redação é "{titulo}". Texto: ""{redacao}"".
            A saída deve ser no formato JSON sem aspas duplas no conteúdo dos campos:'''+'''
            {"criterio":(nota, detalhes),
            "avaliacao_geral": cometários gerais sobre o texto,
            "nota_atribuida": soma dos critérios{END}'''
            
    completion = ' {'+f'''
                "criterio_1":({row.comp_lingua_culta}, {CRITERIO_1_NOTA[round_key(row.comp_lingua_culta)]}),
                "criterio_2":({row.comp_proposta}, {CRITERIO_2_NOTA[round_key(row.comp_proposta)]}),
                "criterio_3":({row.comp_argumentacao}, {CRITERIO_3_NOTA[round_key(row.comp_argumentacao)]}),
                "criterio_4":({row.comp_conhecimentos}, {CRITERIO_4_NOTA[round_key(row.comp_conhecimentos)]}),
                "criterio_5":({row.comp_proposta_solucao}, {CRITERIO_5_NOTA[round_key(row.comp_proposta_solucao)]}),
                "avaliacao_geral": {row.comentario_geral}
                "nota_atribuida": {row.nota_real}'''+'}{END}'
    instance = {"prompt": prompt, "completion":completion}
    return instance