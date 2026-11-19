"""Ejecuta las pruebas del programa de reservas de Software FJ."""

import logging
from pathlib import Path

from excepciones import ErrorSistema
from servicios import AlquilerEquipo, AsesoriaEspecializada, Sala
from sistema import SistemaReservas


# El archivo de registro queda en la misma carpeta que main.py.
RUTA_LOG = Path(__file__).with_name("software_fj.log")


def probar(numero, titulo, operacion, *datos, **opciones):
    # Cada prueba recibe una operacion y los datos necesarios para ejecutarla.
    try:
        resultado = operacion(*datos, **opciones)
    except ErrorSistema as error:
        # Mostramos el motivo del rechazo y guardamos el detalle en el registro.
        print(f"{numero:02d}. {titulo} | Rechazada. {error}")
        logging.error("Caso %02d | %s | %s", numero, titulo, error, exc_info=True)
        return False
    else:
        # Este bloque se ejecuta cuando la operacion sale bien.
        detalle = resultado.describir()
        print(f"{numero:02d}. {titulo} | {detalle}")
        logging.info("Caso %02d | %s | %s", numero, titulo, detalle)
        return True
    finally:
        # Dejamos constancia de que la prueba termino, haya salido bien o mal.
        logging.info("Caso %02d | Fin de la operacion", numero)


def main():
    # Preparamos el archivo para guardar los resultados de las pruebas.
    try:
        logging.basicConfig(
            filename=RUTA_LOG,
            encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )
    except OSError as error:
        print(f"No se pudo abrir el archivo de logs: {error}")
        return 1

    sistema = SistemaReservas()
    resultados = []

    print("SOFTWARE FJ | Demostracion de reservas\n")
    logging.info("Inicio de la simulacion")

    # Casos 1 y 2: registrar un cliente valido y rechazar un correo incorrecto.
    resultados.append(probar(
        1, "Registrar cliente valido", sistema.registrar_cliente,
        "C01", "Ana Rodriguez", "1001", "ana@example.com",
    ))
    resultados.append(probar(
        2, "Registrar cliente con correo invalido", sistema.registrar_cliente,
        "C02", "Carlos Mora", "1002", "correo-sin-arroba",
    ))

    # Casos 3 a 6: crear los tres servicios y probar una tarifa incorrecta.
    resultados.append(probar(
        3, "Crear servicio de sala", sistema.registrar_servicio,
        Sala, "S01", "Sala de reuniones", 30000, capacidad=12,
    ))
    resultados.append(probar(
        4, "Crear equipo con tarifa escrita como texto", sistema.registrar_servicio,
        AlquilerEquipo, "E01", "Proyector", "quince mil", unidades=3,
    ))
    resultados.append(probar(
        5, "Crear equipo con tarifa valida", sistema.registrar_servicio,
        AlquilerEquipo, "E01", "Proyector", 15000, unidades=3,
    ))
    resultados.append(probar(
        6, "Crear servicio de asesoria", sistema.registrar_servicio,
        AsesoriaEspecializada, "A01", "Asesoria tecnica", 50000, max_horas=4,
    ))

    # Casos 7 a 10: probar reservas que se pueden confirmar y otras que fallan.
    resultados.append(probar(
        7, "Reservar la sala durante dos horas", sistema.reservar,
        "R01", "C01", "S01", 2, cantidad=4,
    ))
    resultados.append(probar(
        8, "Reservar equipo con duracion negativa", sistema.reservar,
        "R02", "C01", "E01", -2,
    ))
    resultados.append(probar(
        9, "Reservar una sala que ya esta ocupada", sistema.reservar,
        "R03", "C01", "S01", 1,
    ))
    resultados.append(probar(
        10, "Reservar una asesoria con descuento e impuesto", sistema.reservar,
        "R04", "C01", "A01", 2, descuento=10, impuesto=19,
    ))

    # Casos 11 y 12: cancelar una reserva y probar que no se cancela dos veces.
    resultados.append(probar(
        11, "Cancelar la reserva de sala", sistema.cancelar, "R01",
    ))
    resultados.append(probar(
        12, "Cancelar de nuevo la misma reserva", sistema.cancelar, "R01",
    ))

    # Contamos las operaciones que salieron bien y las que fueron rechazadas.
    exitosas = resultados.count(True)
    rechazadas = resultados.count(False)
    resumen = f"{len(resultados)} operaciones | {exitosas} exitosas | {rechazadas} rechazadas"

    logging.info("Fin de la simulacion | %s", resumen)
    print(f"\nResumen: {resumen}")
    print(f"Registro generado: {RUTA_LOG.name}")
    return 0


# Inicia la demostracion cuando ejecutamos main.py.
if __name__ == "__main__":
    raise SystemExit(main())