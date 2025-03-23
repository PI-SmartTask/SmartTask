from typing import Dict, List


class Variaveis:
    """
    Classe responsável por criar e armazenar as variáveis e domínios do problema.
    """

    def __init__(self):
        self.variaveis = {}

    def criar_variaveis(self, funcionarios: List[int], dias: int) -> Dict[str, List[str]]:
        """
        Cria variáveis X_{i,j} para cada funcionário i e cada dia j, com os domínios possíveis.
        Exemplo de domínio: ["M", "T", "F", "Fer"].
        """
        self.variaveis = {
            f"X_{i}_{j}": ["M", "T", "F", "Fer"]  # Manhã, Tarde, Folga, Férias
            for i in funcionarios
            for j in range(dias)
        }
        return self.variaveis
