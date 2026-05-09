"""Módulo de gestión de usuarios."""

class Usuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

def listar_usuarios(usuarios):
    """Muestra la lista de usuarios registrados."""
    for i, u in enumerate(usuarios, 1):
        print(f"  {i}. {u}")
