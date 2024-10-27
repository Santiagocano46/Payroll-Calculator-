import sys
sys.path.append("src")
import unittest
from unittest.mock import patch, MagicMock
from controller.controlador_usuarios import Insertar, Actualizar, Borrar, BuscarPorCedula
from logic.payroll_calculator import Usuario

class TestControladorUsuarios(unittest.TestCase):
