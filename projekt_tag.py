# Code made by: seraphritt

import re


def set_up_entrada():
    i = 0
    with open("Entrada.txt") as entrada:
        lines = entrada.readlines()
    while i in range(len(lines)):
        if not lines[i].startswith("("):
            lines.remove(lines[i])
            i = 0
            continue
        i += 1
    projetos = lines[:50]
    proj_dict = {}
    alun_dict = {}
    for i in range(len(projetos)):
        lines_w_re = re.search('(P\w+), (\w+), (\w+)', projetos[i])
        proj_dict[lines_w_re.group(1)] = [lines_w_re.group(2), lines_w_re.group(3)]
        # group (1) = cod. proj. # group (2) = num_vagas # group (3) = min_notas
    alunos = lines[50:]
    for i in range(len(alunos)):
        lines_w_re = re.search('(A\w+).:.(P\w+), (P\w+), (P\w+). .(\w+)', alunos[i])
        alun_dict[lines_w_re.group(1)] = [lines_w_re.group(2), lines_w_re.group(3), lines_w_re.group(4),
                                          lines_w_re.group(5)]
        # group (1) = cod. aluno, group (2-4) = projetos prefenciais, group (5) = nota
    return proj_dict, alun_dict


def troca(candidato_troca, alunos_do_projeto, alunos):
    for i in range(len(alunos_do_projeto)):
        if int(candidato_troca[len(candidato_troca) - 1]) > \
                int(alunos.get(alunos_do_projeto[i])[len(alunos.get(alunos_do_projeto[i])) - 1]):
            # se nota do candidato for maior
            return i
        else:
            return -1


def continua(dict_de_alunos, dict_stable):
    # condicao de parada (se houver aluno sem projeto e que ainda possui preferencias
    for i in range(1, 201):
        if not dict_stable[f"A{i}"]:
            if len(dict_de_alunos[f"A{i}"]) > 1:
                return True
    return False


def gale_shapley(proj, students):
    stable_dict = {}
    dict_def_projects = {}
    vetor_proj_n_completos = []
    contador = 0
    alunos_projeto = []
    cheio = 0
    vazio = 0
    proj_completos = 0
    proj_incompleto = 0
    for keys in students.keys():
        stable_dict[keys] = []
    while continua(students, stable_dict):
        for j in range(1, 201):
            if not stable_dict[f"A{j}"]:    # se houver alunos sem projetos
                if len(students.get(f"A{j}")) > 1:
                    # se aluno tiver preferencias, ou seja, se ele ainda tiver alguma possibilidade de projeto
                    contador += 1
                    if contador % 10 == 0:
                        print("\n\n\n")
                        print(f"[+] Iteracao Num {contador}")
                        for i in range(1, 201):
                            if stable_dict[f"A{i}"]:
                                cheio += 1
                            else:
                                vazio += 1
                        for i in range(1, 51):
                            if proj[f"P{i}"][0] == 0:
                                proj_completos += 1
                            else:
                                vetor_proj_n_completos.append(f"P{i}")
                                proj_incompleto += 1
                        #for i in range(1, 201):
                            #print(f'A{i}: {stable_dict.get(f"A{i}")}')
                        for y in range(1, 51):
                            dict_def_projects[f"P{y}"] = []
                        for i in range(1, 201):
                            for k in range(1, 51):
                                if stable_dict.get(f"A{i}"):
                                    if stable_dict.get(f"A{i}")[0] == f"P{k}":
                                        dict_def_projects[f"P{k}"].append(f"A{i}")
                        print(dict_def_projects)    # printa relacao projeto x aluno
                        print(f"Projetos incompletos: {vetor_proj_n_completos}")
                        print("* numero de alunos com projetos:", cheio)
                        print("* numero de alunos sem projetos:", vazio)
                        print("* numero de projetos completos:", proj_completos)
                        print("* numero de projetos incompletos:", proj_incompleto)
                        cheio = 0
                        vazio = 0
                        proj_completos = 0
                        vetor_proj_n_completos = []
                        proj_incompleto = 0

                    if int(proj.get(students.get(f"A{j}")[0])[0]) > 0 and \
                            int(students.get(f"A{j}")[len(students.get(f"A{j}")) - 1]) >= \
                            int(proj.get(students.get(f"A{j}")[0])[1]):
                        # se houver vaga e nota do aluno for suficiente ou maior
                        stable_dict[f"A{j}"].append(students.get(f"A{j}")[0])     # adiciona projeto
                        proj.get(students.get(f"A{j}")[0])[0] = int(proj.get(students.get(f"A{j}")[0])[0]) - 1
                        # modifica o num de vagas do projeto
                    elif int(students.get(f"A{j}")[len(students.get(f"A{j}")) - 1]) < \
                            int(proj.get(students.get(f"A{j}")[0])[1]):
                        # se nota do aluno for insuficiente (independe de houver vagas ou nao)
                        students.get(f"A{j}").pop(0)
                    elif int(proj.get(students.get(f"A{j}")[0])[0]) == 0 and \
                            int(students.get(f"A{j}")[len(students.get(f"A{j}")) - 1]) >= \
                            int(proj.get(students.get(f"A{j}")[0])[1]):
                        # se não houver vaga e nota do aluno for suficiente ou maior
                        for i in range(1, 201):
                            if stable_dict.get(f"A{i}"):
                                if stable_dict.get(f"A{i}")[0] == students.get(f"A{j}")[0]:    #
                                    alunos_projeto.append(f"A{i}")
                        index = troca(students.get(f"A{j}"), alunos_projeto, students)
                        if index != -1:
                            stable_dict[f"A{j}"].append(students.get(f"A{j}")[0])   # adiciona projeto
                            stable_dict[f"{alunos_projeto[index]}"].pop(0)          # retira projeto do que tem nota mnr
                            students.get(f"{alunos_projeto[index]}").pop(0)
                            alunos_projeto = []
                        else:
                            alunos_projeto = []
                            students.get(f"A{j}").pop(0)
            else:
                continue


dict_projects, dict_students = set_up_entrada()
gale_shapley(dict_projects, dict_students)


