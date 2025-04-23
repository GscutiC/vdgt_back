from sqlalchemy.types import TypeEngine, TypeDecorator, UserDefinedType
import json
import numpy as np
from sqlalchemy.ext.compiler import compiles

class PGVector(UserDefinedType):
    """PostgreSQL vector type for storing embeddings."""
    
    cache_ok = True

    def __init__(self, dimensions=None):
        self.dimensions = dimensions

    def get_col_spec(self, **kw):
        if self.dimensions is not None:
            return f"vector({self.dimensions})"
        return "vector"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            if isinstance(value, list):
                return json.dumps(value)
            if isinstance(value, np.ndarray):
                return json.dumps(value.tolist())
            return str(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            if isinstance(value, str):
                try:
                    return np.array(json.loads(value))
                except (json.JSONDecodeError, ValueError):
                    return np.array(value.strip('[]').split(','), dtype=float)
            return value
        return process
    # Agrega esto al mismo archivo custom_types.py
@compiles(PGVector, 'postgresql')
def compile_vector(element, compiler, **kw):
    if element.dimensions is not None:
        return f"vector({element.dimensions})"
    return "vector"