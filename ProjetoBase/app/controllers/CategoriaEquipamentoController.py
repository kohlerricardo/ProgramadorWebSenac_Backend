from sqlmodel import Session,select
from entidades.models import CategoriaEquipamento
from sqlalchemy.exc import OperationalError,IntegrityError
from pydantic import ValidationError
def cadastrar_categoria_equipamento(db: Session, received_categoria: CategoriaEquipamento):
    try:
        categoria = CategoriaEquipamento.model_validate(received_categoria)
        # Operações de banco
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria
    except ValidationError as e:
        # Dados informados não passaram na validação
        raise ValueError("Verifique os dados informados") from e
    except OperationalError as e:
        # Banco caiu ou falha de infraestrutura
        db.rollback() # Limpa a transação pendente
        raise RuntimeError("Falha de conexão com o banco de dados ao tentar cadastrar a categoria.") from e
    except IntegrityError as e:
        # Ex: Tentou cadastrar um nome de categoria que já existe (Unique Constraint)
        db.rollback()
        raise ValueError("Esta categoria já está cadastrada no sistema.") from e

    

def buscar_todas_categoria_equipamento(db:Session):
    try:
        # Operações de banco
        statement = select(CategoriaEquipamento)
        result = db.exec(statement).all()
        return result
    except OperationalError as e:
        # Banco caiu ou falha de infraestrutura
        db.rollback() # Limpa a transação pendente
        raise RuntimeError("Falha de conexão com o banco de dados ao tentar buscar categorias.") from e

def deletar_categoria(db: Session, categoria_id: int):
        try:
            categoria = db.get(CategoriaEquipamento, categoria_id)
            if not categoria:
                raise KeyError(f"Categoria  não encontrada.")
            
            db.delete(categoria)
            db.commit()
            
        except IntegrityError as e:
            db.rollback()
            # Impede a exclusão de categorias que possuem equipamentos vinculados
            raise ValueError("Não é possível deletar esta categoria pois existem equipamentos vinculados a ela.") from e
            
        except OperationalError as e:
            db.rollback()
            raise RuntimeError("Falha de comunicação com o banco de dados.") from e

def atualizar_categoria(db: Session, categoria_id: int, dados_atualizados: CategoriaEquipamento) -> CategoriaEquipamento:
        try:
            
            categoria = db.get(CategoriaEquipamento, categoria_id)
            if not categoria:
                raise KeyError(f"Categoria informada não localizada.")
            
            # Extrai apenas os dados que foram enviados na requisição
            categoria_data = dados_atualizados.model_dump(exclude_unset=True)
            for key, value in categoria_data.items():
                setattr(categoria, key, value)
            
            db.add(categoria)
            db.commit()
            db.refresh(categoria)
            
            return categoria
            
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Erro de integridade nos dados fornecidos.") from e
            
        except OperationalError as e:
            db.rollback()
            raise RuntimeError("Falha de comunicação com o banco de dados.") from e