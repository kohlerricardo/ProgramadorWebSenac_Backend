from sqlmodel import Session,select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Equipamento,EquipamentoPublico, CategoriaEquipamento

def buscar_equipamentos(db:Session)->Equipamento:
    try:
        statement = select(Equipamento)
        equipamentos = db.exec(statement).all()
        return equipamentos
    except OperationalError as e:
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e


def cadastrar_equipamento(db: Session, dados_entrada: EquipamentoPublico) -> Equipamento:
    try:
        # Verifica integridade referencial: a categoria existe?
        categoria = db.get(CategoriaEquipamento, dados_entrada.equipamento_categoria_equipamento_id)
        if not categoria:
            raise ValueError(
                f"A categoria de equipamento informada não está cadastrada no sistema."
            )

        # Valida os dados de entrada.
        # O status DISPONIVEL já é assumido pelo default do próprio modelo SQLModel.
        Equipamento.model_validate(dados_entrada)
        # Cria um objeto do tipo equimento para salvar os dados no banco
        # 
        novo_equipamento = Equipamento(**dados_entrada.model_dump())
        # Salva no banco de dados
        db.add(novo_equipamento)
        db.commit()
        db.refresh(novo_equipamento)

        return novo_equipamento

    except IntegrityError as e:
        db.rollback()
        # Trata violações de dados do banco, como campos Unique
        print(str(e))
        raise ValueError("Erro nos dados informados, verifique e tente novamente") from e
        
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e
        
def atualizar_equipamento(db: Session, equipamento_id: int, dados_atualizados: Equipamento) -> Equipamento:
    try:
        equipamento = db.get(Equipamento, equipamento_id)
        if not equipamento:
            raise KeyError(f"Equipamento de ID {equipamento_id} não encontrado.")
        
        # Se o usuário tentar alterar a categoria, valida se a nova categoria existe
        if dados_atualizados.equipamento_categoria_equipamento_id:
            categoria = db.get(CategoriaEquipamento, dados_atualizados.equipamento_categoria_equipamento_id)
            if not categoria:
                raise ValueError(f"A categoria informada não existe.")
        # Valida os dados de entrada.
        Equipamento.model_validate(dados_atualizados)
        equipamento_data = dados_atualizados.model_dump(exclude_unset=True)
        for key, value in equipamento_data.items():
            setattr(equipamento, key, value)
        
        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)
        
        return equipamento
        
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade. Verifique se o número de patrimônio já existe.") from e
        
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e

def deletar_equipamento(db: Session, equipamento_id: int):
    try:
        equipamento = db.get(Equipamento, equipamento_id)
        if not equipamento:
            raise KeyError(f"Equipamento de ID {equipamento_id} não encontrado.")
        
        db.delete(equipamento)
        db.commit()
        
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e