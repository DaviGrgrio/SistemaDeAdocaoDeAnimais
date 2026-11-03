from cli import main


def rodar(tmp_path, *args):
    return main(["--dados", str(tmp_path), *args])


def cadastrar_basico(tmp_path):
    rodar(tmp_path, "cadastrar-animal", "--tipo", "cachorro", "--nome", "Rex", "--sexo", "MACHO",
          "--idade-meses", "24", "--porte", "M", "--raca", "SRD", "--passeio", "alta")
    rodar(tmp_path, "cadastrar-adotante", "--nome", "Ana", "--idade", "30", "--moradia", "casa",
          "--area", "80", "--experiencia")
    rodar(tmp_path, "cadastrar-adotante", "--nome", "Bia", "--idade", "25", "--moradia", "apto",
          "--area", "40")


def test_fluxo_cadastrar_reservar_adotar(tmp_path, capsys):
    cadastrar_basico(tmp_path)
    assert rodar(tmp_path, "reservar", "--animal", "1", "--adotante", "1") == 0
    assert rodar(tmp_path, "adotar", "--animal", "1", "--adotante", "1") == 0
    assert "CONTRATO" in capsys.readouterr().out


def test_reserva_persiste_entre_execucoes(tmp_path):
    cadastrar_basico(tmp_path)
    assert rodar(tmp_path, "reservar", "--animal", "1", "--adotante", "1") == 0
    # nova execução: a reserva continua ativa, então outra reserva deve falhar
    assert rodar(tmp_path, "reservar", "--animal", "1", "--adotante", "2") == 1


def test_comando_com_erro_retorna_1(tmp_path):
    assert rodar(tmp_path, "reservar", "--animal", "99", "--adotante", "1") == 1
