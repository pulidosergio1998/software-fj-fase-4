"""Guarda y busca clientes, servicios y reservas."""

from cliente import Cliente
from excepciones import DatoInvalido, OperacionNoPermitida
from reserva import Reserva
from servicios import Servicio


class SistemaReservas:
    def __init__(self):
        # Las listas guardan los datos mientras el programa esta abierto.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, codigo, nombre=None, documento=None, correo=None):
        # La clase Cliente revisa los datos al crear el cliente.
        cliente = Cliente(codigo, nombre, documento, correo)

        for actual in self.__clientes:
            if actual.documento == cliente.documento:
                raise OperacionNoPermitida("Ya existe un cliente con ese documento.")

        self._validar_codigo_nuevo(self.__clientes, cliente.codigo)
        self.__clientes.append(cliente)
        return cliente

    def registrar_servicio(self, tipo, codigo, nombre, tarifa, **detalles):
        # El tipo indica si vamos a crear una sala, un equipo o una asesoria.
        if not isinstance(tipo, type) or not issubclass(tipo, Servicio):
            raise DatoInvalido("El tipo de servicio no es valido.")

        try:
            # Los detalles dependen del servicio, como la capacidad de una sala.
            servicio = tipo(codigo, nombre, tarifa, **detalles)
        except TypeError as error:
            raise DatoInvalido(
                "Falta un dato del servicio o se uso un nombre de dato incorrecto."
            ) from error

        self._validar_codigo_nuevo(self.__servicios, servicio.codigo)
        self.__servicios.append(servicio)
        return servicio

    def reservar(self, codigo, codigo_cliente, codigo_servicio, horas, **opciones):
        # Primero buscamos al cliente y al servicio por sus codigos.
        cliente = self._buscar(self.__clientes, codigo_cliente, "cliente")
        servicio = self._buscar(self.__servicios, codigo_servicio, "servicio")

        reserva = Reserva(codigo, cliente, servicio, horas, **opciones)
        self._validar_codigo_nuevo(self.__reservas, reserva.codigo)

        # La reserva se guarda solo despues de confirmarla.
        reserva.confirmar()
        self.__reservas.append(reserva)
        return reserva

    def cancelar(self, codigo):
        reserva = self._buscar(self.__reservas, codigo, "reserva")
        reserva.cancelar()
        return reserva

    @staticmethod
    def _buscar(elementos, codigo, tipo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatoInvalido(f"El codigo de {tipo} es obligatorio.")

        # Asi podemos encontrar el codigo aunque se escriba en minusculas.
        codigo = codigo.strip().upper()
        for elemento in elementos:
            if elemento.codigo == codigo:
                return elemento

        raise OperacionNoPermitida(f"No se encontro {tipo} con codigo {codigo}.")

    @staticmethod
    def _validar_codigo_nuevo(elementos, codigo):
        # Evitamos guardar dos elementos con el mismo codigo en una lista.
        for elemento in elementos:
            if elemento.codigo == codigo:
                raise OperacionNoPermitida(f"El codigo {codigo} ya esta registrado.")