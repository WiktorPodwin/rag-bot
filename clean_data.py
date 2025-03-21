from src.operations.database_operations import ChromaDBOperations, DBOperations
from src.core import get_session


if __name__ == "__main__":
    chroma_oper = ChromaDBOperations()
    chroma_oper.remove_chunks()

    session = get_session()
    db_oper = DBOperations(session=session)
    db_oper.clear_table()
