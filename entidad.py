"""Reglas que comparten los clientes, los servicios y las reservas."""

from abc import ABC, abstractmethod

from excepciones import DatoInvalido


class Entidad(ABC):
    def __init__(self, codigo):
        # Cada elemento del sistema debe tener un codigo.
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatoInvalido("El codigo de la entidad es obligatorio.")

        # Quitamos los espacios de los extremos y usamos mayusculas.
        self.__codigo = codigo.strip().upper()

    @property
    def codigo(self):
        # Permite consultar el codigo guardado.
        return self.__codigo

    @abstractmethod
    def describir(self):
        """Cada clase debe explicar que representa."""