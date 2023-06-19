import os
import pandas as pd
import ssl

# Desativar verificação do certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

link_exp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_2022.csv'
link_imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_2022.csv'
path_exp = 'EXP_2022.csv'
path_imp = 'IMP_2022.csv'
path_result = ''


def gerar_arquivos_por_estado(df_exportacao, df_importacao, path_result):
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    exportacao_agrupada = df_exportacao.groupby(['CO_NCM', 'CO_MES', 'SG_UF_NCM'])['VL_FOB'].sum().reset_index()

    importacao_agrupada = df_importacao.groupby(['CO_NCM', 'CO_MES', 'SG_UF_NCM'])['VL_FOB'].sum().reset_index()

    # Combinar os valores de exportação e importação em um único DataFrame
    dados_combinados = pd.merge(exportacao_agrupada, importacao_agrupada, on=['CO_NCM', 'CO_MES', 'SG_UF_NCM'],
                                how='outer')

    # Preencher valores NaN com zero
    dados_combinados = dados_combinados.fillna(0)

    # Criar um DataFrame final para cada estado
    for estado in dados_combinados['SG_UF_NCM'].unique():
        dados_estado = pd.DataFrame(
            columns=['NCM'] + [f'{tipo}_{mes}' for mes in meses for tipo in ['Exp', 'Imp', 'Net']])

        dados_estado_filtrados = dados_combinados[dados_combinados['SG_UF_NCM'] == estado]

        for index, row in dados_estado_filtrados.iterrows():
            ncm = str(row['CO_NCM']).rstrip('.0')
            exp_values = [0] * len(meses)
            imp_values = [0] * len(meses)
            net_values = [0] * len(meses)

            mes_index = row['CO_MES'] - 1

            exp_values[mes_index] = row['VL_FOB_x']
            imp_values[mes_index] = row['VL_FOB_y']
            net_values[mes_index] = row['VL_FOB_x'] - row['VL_FOB_y']

            if ncm in dados_estado['NCM'].values:
                # Atualizar os valores existentes
                index_ncm = dados_estado[dados_estado['NCM'] == ncm].index[0]
                dados_estado.loc[index_ncm, [f'Exp_{mes}' for mes in meses]] += exp_values
                dados_estado.loc[index_ncm, [f'Imp_{mes}' for mes in meses]] += imp_values
                dados_estado.loc[index_ncm, [f'Net_{mes}' for mes in meses]] += net_values
            else:
                dados_estado.loc[len(dados_estado)] = [ncm] + exp_values + imp_values + net_values

        nome_arquivo = f'{estado}.csv'

        # Verificar se o caminho do resultado está vazio
        if not path_result:
            path_result = os.getcwd()  # Usar o diretório atual

        # Salvar os dados em um arquivo CSV
        caminho_arquivo = os.path.join(path_result, nome_arquivo)
        dados_estado.to_csv(caminho_arquivo, sep=';', index=False)

        print(f"Arquivo '{caminho_arquivo}' gerado com sucesso!")


if not path_exp or not path_imp:
    df_exportacao = pd.read_csv(link_exp, delimiter=';', quoting=1)
    df_importacao = pd.read_csv(link_imp, delimiter=';', quoting=1)
else:
    df_exportacao = pd.read_csv(path_exp, delimiter=';', quoting=1)
    df_importacao = pd.read_csv(path_imp, delimiter=';', quoting=1)

gerar_arquivos_por_estado(df_exportacao, df_importacao, path_result)
