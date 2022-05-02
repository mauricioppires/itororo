"""
    ----------------------------------------------------------------------------
    Autor      : Mauricio P Pires <mauricioppires at gmail dot com>
    Data       : 2020/05/08
    Versao     : 1.0.d
    Programa   : itororo.py
    Observacao : Itororo significa pequena queda dagua.
    ----------------------------------------------------------------------------
    Descricao  : Baixa sequencia de arquivos de midia, com extensao .ts, 
                 para o diretorio atual;
    Linguagem  : Python, versao 3.8;
    ----------------------------------------------------------------------------
    Dependencia: Necessario a instalacao de:
                    - requests
                        > pip install requests
    ----------------------------------------------------------------------------
"""


from datetime import datetime
import fileinput
import os
import pathlib
import requests
import sys


def erro_resumo(numero):
    global contador
    global qtdarq
    global conta_err
    print('-'*80)
    print('<**> Baixados : {}'.format(contador))
    print('<**> Lista    : {}'.format(qtdarq))
    print('\t<**> Linha    : {}'.format(conta_err))
    print('-'*80)
    print('[!!!] Tecla ENTER para fechar o programa. [!!!]')
    espera = input()
    sys.exit(numero)


"""
    ----------------------------------------------------------------------------
    ::  apaga os arquivos de midia .ts apos a concatenacao;
    ----------------------------------------------------------------------------
"""
def apagar_arqs_ts():
    global extensao
    try:
        for arquivo in os.listdir():
            if arquivo.endswith(extensao):
                os.remove(arquivo)
    except Exception as e:
        print('\t[!] <del-file-ts> ERRO: {}'.format(e))
        erro_resumo(1)



"""
    ----------------------------------------------------------------------------
    ::  lê arquivo index.m3u8 fornecido pelo usuario e retorna um arquivo limpo, 
        somente com os links da sequencia da midia.
        entrada: 
            arquivo index.m3u8
        saida: 
            index-m3u8.lst
    ----------------------------------------------------------------------------
"""
def limpar_index_m3u8():
    global arqm3u8
    global arqlista
    global qtdarq
    try:
        if os.path.isfile(arqlista):
            os.remove(arqlista)
        arquivo = open(arqm3u8, 'r')
        novoarquivo = open(arqlista, 'w')
        for linha in arquivo:
            if linha[0:4] != "#EXT":
                novoarquivo.write(linha)
                qtdarq += 1
        arquivo.close()
        novoarquivo.close()
        print('\t[=] total de links: {}'.format(str(qtdarq)))
    except Exception as e:
        print('\t[!] <cls-idx-m3u8> ERRO: {}'.format(e))
        erro_resumo(2)


"""
    ----------------------------------------------------------------------------
    ::  lê nome de arquivo (da lista de arquivos baixados) e retorna o numero.
    ----------------------------------------------------------------------------
"""
def pega_numero(arquivo):
    if len(arquivo) < 14 and len(arquivo) > 16:
        return False
    try:
        numero = arquivo.split('-')
        return int(numero[1])
    except Exception as e:
        print('\t[!] <get-num> ERRO: {}'.format(e))
        erro_resumo(3)

"""
    ----------------------------------------------------------------------------
    ::  Recebe o link do arquivo (.ts) e local + nome do arquivo a ser criado.
    ----------------------------------------------------------------------------
"""
def baixar_arquivo(url, endereco):
    global contador
    global conta_err
    try:
        resposta = requests.get(url.rstrip())
        if resposta.status_code == requests.codes.OK:
            try:
                nn_arquivo = os.path.splitext(endereco)[0] + '.ts'
                #print('***', nn_arquivo)
                #espera = input()
                #with open(endereco, 'wb') as novo_arquivo:
                with open(nn_arquivo, 'wb') as novo_arquivo:
                    for parte in resposta.iter_content(chunk_size=256):
                        novo_arquivo.write(parte)
                contador += 1
            except Exception as e:
                conta_err += str(contador) + '; '
                print('\t[!] <down-file-unique> ERRO: {}'.format(e))
                erro_resumo(4)
        else:
            resposta.raise_for_status()
        print("\t[<] {}\t\t\t\t{}\t\t\t\t{}".format(resposta.status_code,contador,novo_arquivo.name))
    except Exception as e:
        print('\t[!] <down-file-fnct> ERRO: {}'.format(e))
        print('\t[!] Codigo do Erro: {}'.format(resposta.status_code))
        erro_resumo(5)


"""
    ----------------------------------------------------------------------------
    ::  Converte arquivo .ts para .mp4
    ----------------------------------------------------------------------------
"""
# def converter_ts_para_mp4():
    # ## ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "http://dominio/dir1/dir2/index.m3u8" -c copy video.mp4
    # comando2 = 'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i video.ts -c copy video.mp4'
    # os.system(comando2)


"""
    ----------------------------------------------------------------------------
    ::  Limpa diretorio apos os processos
    ----------------------------------------------------------------------------
"""
def limpando_diretorio():
    global arqTMP
    global arqFINAL
    global extensao
    global prefixo
    global arqlista
    try:
        for nome_arq in  os.listdir():
            if nome_arq.endswith(extensao):
                num_seq_arq = pega_numero(nome_arq)
                novo_nome_arq = prefixo + str(num_seq_arq).zfill(3) + "." + extensao
                os.rename(nome_arq, novo_nome_arq)
        comando1 = 'copy /b *.{} {}'.format(extensao,arqTMP)
        os.system(comando1)
        apagar_arqs_ts()
        os.remove(arqlista)
        os.rename(arqTMP, arqFINAL)
    except Exception as e:
        print('\t[!] <cls-dir> ERRO: {}'.format(e))
        erro_resumo(6)


"""
    ----------------------------------------------------------------------------
    ::  Programa Principal
    ----------------------------------------------------------------------------
"""
if __name__ == "__main__":

    # ## GLOBAL
    # --------------------------------------------------------------------------
    arqm3u8   = 'index.m3u8'            # arquivo com os links
    arqlista  = 'index-m3u8.lst'        # arquivo index.m3u8 limpo
    arqTMP    = 'VIDEO.TMP'             # arquivo temporario resultando da concatenacao do arquivos baixados
    arqFINAL  = 'VIDEO.ts'              # arquivo temporario nomeado para ts
    caminho   = os.getcwd()             # Recebe a informação do diretorio atual
    extensao  = 'ts'                    # extensão dos arquivos de midia
    prefixo   = 'video-'                # prefixo do nome pós formatado dos arquivos .ts
    contador  = 0                       # contador para criar ponto de referencia caso aconteca quebra de conexao.
    qtdarq    = 0                       # recebe a quantidade de arquivos que sera baixado;
    conta_err = ''                      # acumulador de erros (numero da linha-link)
    # --------------------------------------------------------------------------
    versao    = '1.0.d'                 # versao
    ano       = '2020'                  # ano
    autor     = 'Mauricio P Pires'      # autor
    # --------------------------------------------------------------------------

    try:
        print('ITORORO - Download de arquivos de midia') # ITORORO: pequena queda dagua
        print('v{}y{}a{}'.format(versao, ano, autor))
        print('\n[+] Preparando lista...')
        limpar_index_m3u8()
        print('\n[+] Baixar arquivos de midia...')
        narquivo = open(arqlista, 'r')
        print('\t[#] Resposta do Servidor\tContador\t\tArquivo')
        inicio = datetime.now()
        for linha in narquivo:
            endereco = linha.split('/')
            baixar_arquivo(linha,endereco[-1].rstrip())
        narquivo.close()
        print('\t[.] Tempo: {}'.format(datetime.now() - inicio))
        print('\n[+] Limpando diretorio ...')
        if contador != qtdarq:
            print('\t[!!] Atenção!\n\tA quantidade de arquivos baixados ({}) difere do total da lista ({}).'.format(contador,qtdarq))
            print('\t[!!] Linha(s): {}'.format(conta_err))
            print('Tecle ENTER para seguir...')
            espera = input()
        limpando_diretorio()
    except Exception as e:
        # conta_err += str(contador) + '; '
        print('\t[!] <main-prog> ERRO: {}'.format(e))
        erro_resumo(7)

"""
    ----------------------------------------------------------------------------
    ::  <mauricioppires at gmail dot com>
    ----------------------------------------------------------------------------
"""
