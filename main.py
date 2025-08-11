import os

# Códigos ANSI para colores
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

def imprimir_banner_coloreado(ruta_txt):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        for linea in f:
            if "404" in linea:
                # Insertar color blanco SOLO en la parte 404
                linea = linea.replace("404", f"{WHITE}404{CYAN}")
                print(f"{CYAN}{linea.strip()}{RESET}")
            elif "Not Found" in linea:
                linea = linea.replace("Not Found", f"{WHITE}Not Found{CYAN}")
                print(f"{CYAN}{linea.strip()}{RESET}")
            else:
                print(f"{CYAN}{linea.strip()}{RESET}")

if __name__ == "__main__":
    print("-" * 78)
    imprimir_banner_coloreado("wings.txt")
    print("-" * 78)
    os.system("python3 heven.py")
