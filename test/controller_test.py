import sys
sys.path.append("src")
import unittest
from unittest.mock import patch, MagicMock
from controller.controlador_usuarios import Insertar, Actualizar, Borrar, BuscarPorCedula
from logic.payroll_calculator import Usuario

class TestControladorUsuarios(unittest.TestCase):

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_insertar_usuario_exito(self, mock_obtener_cursor):
        # Caso exitoso
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor

        usuario = Usuario(cedula="12345678", nombre="Juan", salary=1000, days_worked=10, hours_worked=40, commissions=100, overtime_hours=5)
        Insertar(usuario)
        mock_cursor.execute.assert_called_once()  # Verifica que la SQL fue ejecutada
        mock_cursor.connection.commit.assert_called_once()  # Verifica que se hizo commit

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_insertar_usuario_error(self, mock_obtener_cursor):
        # Caso de error al insertar
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Error al insertar el usuario")

        usuario = Usuario(cedula="12345678", nombre="Juan", salary=1000, days_worked=10, hours_worked=40, commissions=100, overtime_hours=5)
        
        with self.assertRaises(Exception):
            Insertar(usuario)
        mock_cursor.connection.rollback.assert_called_once()  # Verifica que se hizo rollback

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_actualizar_usuario_exito(self, mock_obtener_cursor):
        # Caso exitoso
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor

        usuario = Usuario(cedula="12345678", nombre="Juan Actualizado", salary=1100, days_worked=12, hours_worked=45, commissions=150, overtime_hours=7)
        Actualizar(usuario)
        mock_cursor.execute.assert_called_once()  # Verifica que la SQL fue ejecutada
        mock_cursor.connection.commit.assert_called_once()

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_actualizar_usuario_error(self, mock_obtener_cursor):
    # Simulamos el cursor y la excepción
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Error al actualizar el usuario")

        # Simula la conexión
        mock_cursor.connection = MagicMock()
    
        usuario = Usuario(cedula="12345678", nombre="Juan Actualizado", salary=1100, days_worked=12, hours_worked=45, commissions=150, overtime_hours=7)
    
        with self.assertRaises(Exception):
            Actualizar(usuario)
        mock_cursor.connection.rollback.assert_called_once()  # Verifica que se hizo rollback


    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_borrar_usuario_exito(self, mock_obtener_cursor):
        # Caso exitoso
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor

        usuario = Usuario(cedula="12345678", nombre="Juan", salary=1000, days_worked=10, hours_worked=40, commissions=100, overtime_hours=5)
        Borrar(usuario)
        mock_cursor.execute.assert_called_once_with(f"delete from usuarios where cedula = '{usuario.cedula}'")
        mock_cursor.connection.commit.assert_called_once()

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_borrar_usuario_error(self, mock_obtener_cursor):
    # Simulamos el cursor y la excepción
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Error al borrar el usuario")

    # Simula la conexión
        mock_cursor.connection = MagicMock()

        usuario = Usuario(cedula="12345678", nombre="Juan", salary=1000, days_worked=10, hours_worked=40, commissions=100, overtime_hours=5)
    
        with self.assertRaises(Exception):
            Borrar(usuario)
        mock_cursor.connection.rollback.assert_called_once()

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_buscar_por_cedula_exito(self, mock_obtener_cursor):
        # Caso exitoso
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("12345678", "Juan", 1000, 10, 40, 100, 5)

        resultado = BuscarPorCedula("12345678")
        esperado = "El usuario que tiene por cedula: 12345678, nombre: Juan, salario: 1000, dias_trabajados: 10, horas_trabajadas: 40, comisiones: 100, horas_extras: 5"
        self.assertEqual(resultado, esperado)

    @patch('controller.controlador_usuarios.ObtenerCursor')
    def test_buscar_por_cedula_no_existe(self, mock_obtener_cursor):
        # Caso de error (usuario no encontrado)
        mock_cursor = MagicMock()
        mock_obtener_cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        with self.assertRaises(Exception):  # Suponiendo que levantas una excepción si no existe
            BuscarPorCedula("99999999")


if __name__ == '__main__':
    unittest.main()