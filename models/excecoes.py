class ReservaInvalidaError(Exception):
    """Reserva inexistente, duplicada ou expirada."""

class TransicaoDeEstadoInvalidaError(Exception):
    """Mudança de status não permitida."""

class PoliticaNaoAtendidaError(Exception):
    """Adotante não atende à política configurada."""

class RepositorioError(Exception):
    """Falha de persistência."""
