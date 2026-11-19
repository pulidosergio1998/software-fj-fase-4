"""Permite procesar, confirmar y cancelar una reserva."""

from cliente import Cliente
from entidad import Entidad
from excepciones import DatoInvalido, OperacionNoPermitida, ServicioNoDisponible
from servicios import Servicio


class Reserva(Entidad):
    def __init__(
        self, codigo, cliente, servicio, horas, *,
        cantidad=1, descuento=0, impuesto=0
    ):
        super().__init__(codigo)

        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatoInvalido("La reserva requiere un cliente y un servicio validos.")

        # Guardamos quien reserva, que servicio quiere y por cuantas horas.
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__cantidad = cantidad
        self.__descuento = descuento
        self.__impuesto = impuesto
        self.__estado = "Pendiente"
        self.__costo = None

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def procesar(self):
        # Primero revisamos el estado de la reserva y si el servicio esta libre.
        if self.__estado != "Pendiente":
            raise OperacionNoPermitida(f"La reserva {self.codigo} no esta pendiente.")

        if not self.__servicio.disponible:
            raise ServicioNoDisponible(
                f"El servicio {self.__servicio.codigo} no esta disponible."
            )

        return self.__servicio.calcular_costo(
            self.__horas,
            cantidad=self.__cantidad,
            descuento=self.__descuento,
            impuesto=self.__impuesto,
        )

    def confirmar(self):
        # Calculamos el costo antes de marcar el servicio como ocupado.
        costo = self.procesar()
        self.__servicio.ocupar(self.codigo)
        self.__costo = costo
        self.__estado = "Confirmada"

    def cancelar(self):
        if self.__estado != "Confirmada":
            raise OperacionNoPermitida(f"La reserva {self.codigo} no esta confirmada.")

        # Al cancelar, dejamos el servicio libre para otra reserva.
        self.__servicio.liberar(self.codigo)
        self.__estado = "Cancelada"

    def describir(self):
        detalle = (
            f"Reserva {self.codigo} {self.__estado.lower()} | "
            f"cliente {self.__cliente.codigo} | servicio {self.__servicio.codigo} | "
            f"{self.__horas} hora(s)"
        )

        if self.__costo is not None and self.__estado == "Confirmada":
            detalle += f" | total: {self.__costo:.2f} COP"

        return detalle