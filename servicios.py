"""Servicios de Software FJ y reglas para calcular sus precios."""

from abc import abstractmethod
from decimal import Decimal, DecimalException, ROUND_HALF_UP

from entidad import Entidad
from excepciones import (
    DatoInvalido,
    ErrorCalculo,
    ServicioNoDisponible,
    decimal_valido,
    entero_positivo,
)


class Servicio(Entidad):
    # Aqui van las reglas que comparten los tres servicios.
    def __init__(self, codigo, nombre, tarifa_hora, *, habilitado=True):
        super().__init__(codigo)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalido("El nombre del servicio es obligatorio.")

        if not isinstance(habilitado, bool):
            raise DatoInvalido("El estado del servicio debe ser verdadero o falso.")

        tarifa = decimal_valido(tarifa_hora, "tarifa por hora")
        if tarifa <= 0:
            raise DatoInvalido("La tarifa por hora debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa
        self.__habilitado = habilitado
        self.__reserva_activa = None

    @property
    def disponible(self):
        # El servicio debe estar habilitado y libre de reservas activas.
        return self.__habilitado and self.__reserva_activa is None

    def ocupar(self, codigo_reserva):
        if not self.disponible:
            raise ServicioNoDisponible(
                f"El servicio {self.codigo} no esta disponible."
            )
        self.__reserva_activa = codigo_reserva

    def liberar(self, codigo_reserva):
        # Solo la reserva activa puede liberar el servicio.
        if self.__reserva_activa == codigo_reserva:
            self.__reserva_activa = None

    @abstractmethod
    def validar_parametros(self, horas, cantidad):
        """Revisa que las horas y la cantidad sean mayores que cero."""
        return entero_positivo(horas, "duracion"), entero_positivo(cantidad, "cantidad")

    @abstractmethod
    def calcular_costo(self, horas, *, cantidad=1, descuento=0, impuesto=0):
        """Cada servicio define como calcula el costo."""

    def _calcular_total(self, horas, unidades, descuento, impuesto):
        # Podemos dejar el descuento y el impuesto en cero.
        rebaja = decimal_valido(descuento, "descuento")
        tributo = decimal_valido(impuesto, "impuesto")
        if not 0 <= rebaja <= 100 or not 0 <= tributo <= 100:
            raise ErrorCalculo("El descuento y el impuesto deben estar entre 0 y 100 %.")

        try:
            # Primero se aplica el descuento y luego el impuesto.
            subtotal = self._tarifa_hora * horas * unidades
            total = subtotal * (1 - rebaja / 100) * (1 + tributo / 100)
            return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except DecimalException as error:
            raise ErrorCalculo("No se pudo obtener el valor de la reserva.") from error


class Sala(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, *, capacidad, habilitado=True):
        super().__init__(codigo, nombre, tarifa_hora, habilitado=habilitado)
        self.__capacidad = entero_positivo(capacidad, "capacidad de la sala")

    def describir(self):
        return f"Sala {self.codigo} ({self._nombre}, cupo para {self.__capacidad} personas)"

    def validar_parametros(self, horas, cantidad):
        horas, asistentes = super().validar_parametros(horas, cantidad)
        if asistentes > self.__capacidad:
            raise DatoInvalido("Los asistentes superan la capacidad de la sala.")
        return horas, asistentes

    def calcular_costo(self, horas, *, cantidad=1, descuento=0, impuesto=0):
        horas, _ = self.validar_parametros(horas, cantidad)
        # La sala se cobra por hora, aunque asistan varias personas.
        return self._calcular_total(horas, 1, descuento, impuesto)


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, *, unidades, habilitado=True):
        super().__init__(codigo, nombre, tarifa_hora, habilitado=habilitado)
        self.__unidades = entero_positivo(unidades, "unidades disponibles")

    def describir(self):
        return f"Equipo {self.codigo} ({self._nombre}, {self.__unidades} unidades)"

    def validar_parametros(self, horas, cantidad):
        horas, unidades = super().validar_parametros(horas, cantidad)
        if unidades > self.__unidades:
            raise ServicioNoDisponible("No hay suficientes unidades de ese equipo.")
        return horas, unidades

    def calcular_costo(self, horas, *, cantidad=1, descuento=0, impuesto=0):
        horas, unidades = self.validar_parametros(horas, cantidad)
        # Si se alquilan dos equipos, se cobra por los dos.
        return self._calcular_total(horas, unidades, descuento, impuesto)


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, *, max_horas, habilitado=True):
        super().__init__(codigo, nombre, tarifa_hora, habilitado=habilitado)
        self.__max_horas = entero_positivo(max_horas, "limite de horas de asesoria")

    def describir(self):
        return f"Asesoria {self.codigo} ({self._nombre}, hasta {self.__max_horas} horas)"

    def validar_parametros(self, horas, cantidad):
        horas, participantes = super().validar_parametros(horas, cantidad)
        if participantes != 1 or horas > self.__max_horas:
            raise DatoInvalido(
                f"La asesoria es individual y admite hasta {self.__max_horas} horas."
            )
        return horas, participantes

    def calcular_costo(self, horas, *, cantidad=1, descuento=0, impuesto=0):
        horas, _ = self.validar_parametros(horas, cantidad)
        # La asesoria es individual y se cobra por las horas.
        return self._calcular_total(horas, 1, descuento, impuesto)