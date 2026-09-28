# ============================================================================
# IMPORTAÇÕES
# ----------------------------------------------------------------------------
# Session         -> sessão do SQLModel (uma transação com o banco)
# select          -> construtor de SELECT do SQLModel
# OperationalError-> erros de conexão/indisponibilidade do banco
# IntegrityError  -> violação de constraints (FK, UNIQUE, NOT NULL)
# ============================================================================

from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Equipamento, EquipamentoPublico, CategoriaEquipamento

# ----------------------------------------------------------------------------
# LISTAR EQUIPAMENTOS
# ----------------------------------------------------------------------------
def buscar_equipamentos(db: Session) -> list[Equipamento]:
    try:
        # Monta o SELECT * FROM equipamento
        statement = select(Equipamento)
        # .exec() executa e .all() traz todos os registros como lista
        return db.exec(statement).all()
    except OperationalError as e:
        # Banco inacessível -> erro de infraestrutura (500)
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# BUSCAR UM EQUIPAMENTO PELO ID
# ----------------------------------------------------------------------------
def buscar_equipamento_por_id(db: Session, equipamento_id: int) -> Equipamento:
    try:
        # db.get() busca pela PK; devolve None se não existir
        equipamento = db.get(Equipamento, equipamento_id)
        if not equipamento:
            # KeyError mapeia para 404 na rota
            raise KeyError(f"Equipamento de ID {equipamento_id} não encontrado.")
        return equipamento
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# CADASTRAR EQUIPAMENTO
# ----------------------------------------------------------------------------
def cadastrar_equipamento(db: Session, dados_entrada: EquipamentoPublico) -> Equipamento:
    try:
        # PASSO 1 — Verificação de integridade referencial:
        # a categoria informada realmente existe?
        categoria = db.get(
            CategoriaEquipamento,
            dados_entrada.equipamento_categoria_equipamento_id,
        )
        if not categoria:
            # ValueError mapeia para 400 na rota
            raise ValueError(
                "A categoria de equipamento informada não está cadastrada no sistema."
            )

        # PASSO 2 — Cria a instância do modelo de TABELA a partir do
        # schema público. O default do status (DISPONIVEL) é aplicado aqui.
        novo_equipamento = Equipamento(**dados_entrada.model_dump())

        # PASSO 3 — Persiste: add() marca para inserir, commit() executa
        db.add(novo_equipamento)
        db.commit()
        # refresh() traz de volta os valores gerados pelo banco (ex.: ID)
        db.refresh(novo_equipamento)
        return novo_equipamento

    except IntegrityError as e:
        # Rollback desfaz qualquer alteração parcial da transação
        db.rollback()
        raise ValueError(
            "Erro nos dados informados, verifique e tente novamente."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# ATUALIZAR EQUIPAMENTO
# ----------------------------------------------------------------------------
def atualizar_equipamento(
    db: Session,
    equipamento_id: int,
    dados_atualizados: EquipamentoPublico,
) -> Equipamento:
    try:
        # PASSO 1 — Confirma que o equipamento existe
        equipamento = db.get(Equipamento, equipamento_id)
        if not equipamento:
            raise KeyError(f"Equipamento de ID {equipamento_id} não encontrado.")

        # PASSO 2 — Se a categoria foi informada, valida se ainda existe
        nova_categoria_id = dados_atualizados.equipamento_categoria_equipamento_id
        if nova_categoria_id is not None:
            if not db.get(CategoriaEquipamento, nova_categoria_id):
                raise ValueError("A categoria informada não existe.")

        # PASSO 3 — Aplica apenas os campos enviados (exclude_unset=True).
        # Isso preserva campos que o cliente não quis alterar.
        equipamento_data = dados_atualizados.model_dump(exclude_unset=True)
        for key, value in equipamento_data.items():
            setattr(equipamento, key, value)

        # PASSO 4 — Persiste alterações
        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)
        return equipamento

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Erro de integridade. Verifique se o número de patrimônio já existe."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


# ----------------------------------------------------------------------------
# DELETAR EQUIPAMENTO
# ----------------------------------------------------------------------------
def deletar_equipamento(db: Session, equipamento_id: int) -> None:
    try:
        # PASSO 1 — Confirma existência
        equipamento = db.get(Equipamento, equipamento_id)
        if not equipamento:
            raise KeyError(f"Equipamento de ID {equipamento_id} não encontrado.")

        # PASSO 2 — Remove e efetiva
        db.delete(equipamento)
        db.commit()

    except IntegrityError as e:
        # Se houver empréstimo apontando para este equipamento, a FK barra.
        # Retornamos como ValueError para a rota traduzir em 400.
        db.rollback()
        raise ValueError(
            "Não é possível excluir: existem empréstimos vinculados a este equipamento."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e