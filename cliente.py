"""Guarda y revisa los datos de cada cliente."""

import re

from entidad import Entidad
from excepciones import DatoInvalido


class Cliente(Entidad):
    def __init__(self, codigo, nombre=None, documento=None, correo=None):
        # Usamos la regla de Entidad para revisar y guardar el codigo.
        super().__init__(codigo)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalido("El nombre del cliente es obligatorio.")

        # El documento se guarda como texto para conservar ceros al inicio.
        if not isinstance(documento, str) or not re.fullmatch(
            r"[0-9]+", documento.strip()
        ):
            raise DatoInvalido("El documento debe contener solo digitos.")

        # Revisamos que el correo tenga usuario, arroba y dominio.
        if not isinstance(correo, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", correo.strip()
        ):
            raise DatoInvalido("El correo debe tener un formato valido.")

        self.__nombre = nombre.strip()
        self.__documento = documento.strip()
        self.__correo = correo.strip()

    # Estas propiedades permiten consultar los datos guardados.
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    def describir(self):
        # Mostramos el codigo sin exponer el documento ni el correo.
        return f"Cliente {self.codigo} registrado"