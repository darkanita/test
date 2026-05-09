"""
Mi Aplicación - v1.0
IU Digital de Antioquia
"""
from usuarios import Usuario, listar_usuarios

def main():
    print("Bienvenido a Mi Aplicación")
    usuarios = [
        Usuario("Ana", "ana@correo.com"),
        Usuario("Carlos", "carlos@correo.com"),
    ]
    print("\nUsuarios registrados:")
    listar_usuarios(usuarios)

if __name__ == "__main__":
    main()
