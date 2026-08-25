class DomainError(Exception):
    """Error base del dominio de SUPRDL."""


class EntityNotFoundError(DomainError):
    """La entidad solicitada no existe."""


class RepositoryError(DomainError):
    """Error producido durante una operación de persistencia."""
