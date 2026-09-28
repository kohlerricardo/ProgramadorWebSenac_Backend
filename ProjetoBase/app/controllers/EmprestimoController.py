from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError

from entidades.models import (
    Emprestimo,
    EmprestimoPublico,
    EnumStatusEmprestimo,
    EnumEquipamento,
    Usuario,
    Equipamento,
)


# ----------------------------------------------------------------------------
# LISTAR EMPRÉSTIMOS
# ----------------------------------------------------------------------------
def buscar_emprestimos(db: Session) -> list[Emprestimo]:
    try:
        return db.exec(select(Emprestimo)).all()
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR EMPRÉSTIMO PELO ID
# ----------------------------------------------------------------------------
def buscar_emprestimo_por_id(db: Session, emprestimo_id: int) -> Emprestimo:
    try:
        emprestimo = db.get(Emprestimo, emprestimo_id)
        if not emprestimo:
            raise KeyError(f"Empréstimo de ID {emprestimo_id} não encontrado.")
        return emprestimo
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR EMPRÉSTIMO
# ----------------------------------------------------------------------------
def cadastrar_emprestimo(db: Session, dados_entrada: EmprestimoPublico) -> Emprestimo:
    try:
        # PASSO 1 — Solicitante existe?
        if not db.get(Usuario, dados_entrada.emprestimo_solicitante_id):
            raise ValueError("Solicitante informado não está cadastrado no sistema.")

        # PASSO 2 — Equipamento existe?
        equipamento = db.get(Equipamento, dados_entrada.emprestimo_equipamento_id)
        if not equipamento:
            raise ValueError("Equipamento informado não está cadastrado no sistema.")

        # PASSO 3 — Regra de negócio: equipamento precisa estar DISPONIVEL
        if equipamento.equipamento_status_equipamento != EnumEquipamento.DISPONIVEL:
            raise ValueError(
                f"Equipamento não está disponível (status atual: "
                f"{equipamento.equipamento_status_equipamento.value})."
            )

        # PASSO 4 — Se aprovador foi informado, ele existe?
        if dados_entrada.emprestimo_aprovador_id and not db.get(
            Usuario, dados_entrada.emprestimo_aprovador_id
        ):
            raise ValueError("Aprovador informado não está cadastrado no sistema.")

        # PASSO 5 — Cria o empréstimo
        novo_emprestimo = Emprestimo(**dados_entrada.model_dump())

        # PASSO 6 — Reserva o equipamento (efeito colateral do negócio)
        equipamento.equipamento_status_equipamento = EnumEquipamento.RESERVADO
        db.add(equipamento)

        # PASSO 7 — Persiste tudo em uma única transação
        db.add(novo_emprestimo)
        db.commit()
        db.refresh(novo_emprestimo)
        return novo_emprestimo

    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro nos dados informados, verifique e tente novamente.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# ATUALIZAR EMPRÉSTIMO
# Contém a lógica de transição de status:
#   APROVADO   -> preenche data de aprovação
#   FINALIZADO -> preenche data de devolução e libera o equipamento
# ----------------------------------------------------------------------------
def atualizar_emprestimo(
    db: Session, emprestimo_id: int, dados_atualizados: EmprestimoPublico
) -> Emprestimo:
    try:
        # PASSO 1 — Confere existência
        emprestimo = db.get(Emprestimo, emprestimo_id)
        if not emprestimo:
            raise KeyError(f"Empréstimo de ID {emprestimo_id} não encontrado.")

        # PASSO 2 — Valida FKs que possam ter sido enviadas
        if dados_atualizados.emprestimo_solicitante_id and not db.get(
            Usuario, dados_atualizados.emprestimo_solicitante_id
        ):
            raise ValueError("Solicitante informado não está cadastrado no sistema.")

        if dados_atualizados.emprestimo_aprovador_id and not db.get(
            Usuario, dados_atualizados.emprestimo_aprovador_id
        ):
            raise ValueError("Aprovador informado não está cadastrado no sistema.")

        if dados_atualizados.emprestimo_equipamento_id and not db.get(
            Equipamento, dados_atualizados.emprestimo_equipamento_id
        ):
            raise ValueError("Equipamento informado não está cadastrado no sistema.")

        # PASSO 3 — Aplica as mudanças enviadas
        for key, value in dados_atualizados.model_dump(exclude_unset=True).items():
            setattr(emprestimo, key, value)

        # PASSO 4 — Efeitos colaterais por mudança de status
        # 4.1 -> APROVADO: registra a data da aprovação (uma única vez)

        if (
            emprestimo.emprestimo_status_emprestimo == EnumStatusEmprestimo.APROVADO
            and emprestimo.emprestimo_data_aprovacao is None
        ):
            emprestimo.emprestimo_data_aprovacao = datetime.utcnow()
        # 4.2 -> RECUSADO: retorna equipamento para disponível
        if (
            emprestimo.emprestimo_status_emprestimo == EnumStatusEmprestimo.RECUSADO
            and emprestimo.emprestimo_data_devolucao is None
        ):
            equipamento = db.get(Equipamento, emprestimo.emprestimo_equipamento_id)
            if equipamento and equipamento.equipamento_status_equipamento == EnumEquipamento.RESERVADO:
                equipamento.equipamento_status_equipamento = EnumEquipamento.DISPONIVEL
                db.add(equipamento)
        # 4.2 -> FINALIZADO: registra devolução e libera o equipamento
        if (
            emprestimo.emprestimo_status_emprestimo == EnumStatusEmprestimo.FINALIZADO
            and emprestimo.emprestimo_data_devolucao is None
        ):
            emprestimo.emprestimo_data_devolucao = datetime.utcnow()
            equipamento = db.get(Equipamento, emprestimo.emprestimo_equipamento_id)
            if equipamento:
                equipamento.equipamento_status_equipamento = EnumEquipamento.DISPONIVEL
                db.add(equipamento)

        # PASSO 5 — Persiste
        db.add(emprestimo)
        db.commit()
        db.refresh(emprestimo)
        return emprestimo

    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados informados.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR EMPRÉSTIMO
# Ao excluir um empréstimo pendente/aprovado, libera o equipamento.
# ----------------------------------------------------------------------------
def deletar_emprestimo(db: Session, emprestimo_id: int) -> None:
    try:
        emprestimo = db.get(Emprestimo, emprestimo_id)
        if not emprestimo:
            raise KeyError(f"Empréstimo de ID {emprestimo_id} não encontrado.")

        # Se o equipamento ainda estava "tomado" por este empréstimo,
        # devolve para DISPONIVEL antes de excluir.
        if emprestimo.emprestimo_status_emprestimo in (
            EnumStatusEmprestimo.PENDENTE,
            EnumStatusEmprestimo.APROVADO,
        ):
            equipamento = db.get(Equipamento, emprestimo.emprestimo_equipamento_id)
            if equipamento:
                equipamento.equipamento_status_equipamento = EnumEquipamento.DISPONIVEL
                db.add(equipamento)

        db.delete(emprestimo)
        db.commit()
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e