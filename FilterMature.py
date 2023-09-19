import re
import os

def gera_diretorios():
    arq = "saida_MIR_filtradas.fa"
    arquivo_saida = open("ID_MIRNAS", "w")

    l = []

    with open(arq) as arquivo:
        for line in arquivo:
            match = re.search(r'>\w+-(\w+\d+)', line)
            if match:
                id_mirna = match.group(1)
                if id_mirna not in l:
                    l.append(id_mirna)
                    # gera diretório
                    os.mkdir(str(id_mirna))
                    arquivo_saida.write(id_mirna + "\n")
    
    arquivo_saida.close()
    return 1

def gera_familias():
    arq = "ID_MIRNAS"

    with open(arq) as arquivo_1:
        for line_arq in arquivo_1:
            match = re.search(r'(\w+\d+)', line_arq)
            if match:
                id_mirna = match.group(1)
                arquivo_saida = open(str(id_mirna) + "/familia_" + str(id_mirna) + "_mirnas.fa", "a")
                with open("saida_MIR_filtradas.fa") as arquivo:
                    flag = False
                    for line in arquivo:
                        if flag:
                            match1 = re.search(r'^>', line)
                            if match1:
                                flag = False
                            else:
                                arquivo_saida.write(line)

                        match2 = re.search(r'>(\w+)-(\w+\d+)', line)
                        if match2:
                            prefixo_mirna, mirna = match2.group(1), match2.group(2)
                            if mirna == id_mirna:
                                # Novo cabeçalho com a nomenclatura desejada
                                novo_cabecalho = f">{prefixo_mirna}-5p MIMAT0000166 Arabidopsis thaliana {prefixo_mirna}-5p\n"
                                arquivo_saida.write(novo_cabecalho)
                                flag = True
                arquivo_saida.close()

def main():
    finalizou = gera_diretorios()
    if finalizou == 1:
        gera_familias()

if __name__ == "__main__":
    main()

