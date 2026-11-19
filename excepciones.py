"""Errores que el sistema puede manejar durante la simulacion."""

from decimal import Decimal, InvalidOperation


class ErrorSistema(Exception):
    """Error general del programa de reservas."""


class DatoInvalido(ErrorSistema):
    """Falta un dato o se escribio un valor incorrecto."""


class ErrorCalculo(ErrorSistema):
    """No se pudo calcular el costo de la reserva."""


class ServicioNoDisponible(ErrorSistema):
    """El servicio esta deshabilitado o ya tiene una reserva activa."""


class OperacionNoPermitida(ErrorSistema):
    """La accion no se puede realizar en ese momento."""


def decimal_valido(valor, campo):
    # Si falta un dato, indicamos cual hace falta.
    if valor is None:
        raise DatoInvalido(f"Falta el dato obligatorio {campo}.")

    # Intentamos convertir el dato a numero para usarlo en una cuenta.
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError) as error:
        # Mostramos un mensaje claro y conservamos el error original.
        raise DatoInvalido(f"El campo {campo} debe ser numerico.") from error

    if not numero.is_finite():
        raise DatoInvalido(f"El campo {campo} debe ser un numero finito.")

    return numero


def entero_positivo(valor, campo):
    # Las cantidades y las horas deben ser enteros mayores que cero.
    if type(valor) is not int or valor <= 0:
        raise DatoInvalido(f"El campo {campo} debe ser un entero mayor que cero.")

    return valor
