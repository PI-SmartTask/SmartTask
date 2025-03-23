import os
import sys
import time
import csv
import logging
from typing import Dict, List, Optional, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Formulation')))
from Solver import Solver  # Importação correta do módulo Solver

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class CSPSolver(Solver):
    """
    Solver baseado em CSP (Constraint Satisfaction Problem).
    Utiliza Backtracking básico com Forward Checking para encontrar uma solução.
    """

    def buscar_solucao(self, variaveis: Dict[str, List[str]], restricoes: List[Dict[str, Any]]) -> Optional[Dict[str, str]]:
        inicio = time.time()  # Início do contador de tempo

        def forward_checking(var: str, valor: str, variaveis: Dict[str, List[str]], restricoes: List[Dict[str, Any]]) -> List[tuple]:
            """
            Remove valores inconsistentes do domínio das variáveis futuras após uma atribuição.
            Retorna uma lista dos valores removidos para possível reversão.
            """
            removidos = []

            for restricao in restricoes:
                if var in restricao["variaveis"]:
                    for outra_var in restricao["variaveis"]:
                        if outra_var != var and outra_var in variaveis and len(variaveis[outra_var]) > 1:
                            valores_a_remover = [v for v in variaveis[outra_var] if not self.verificar_consistencia({var: valor, outra_var: v}, [restricao])]
                            for v in valores_a_remover:
                                variaveis[outra_var].remove(v)
                                removidos.append((outra_var, v))

                            # Caso um domínio fique vazio, pare a verificação antecipadamente
                            if not variaveis[outra_var]:
                                return removidos

            return removidos

        def desfazer_forward_checking(removidos: List[tuple], variaveis: Dict[str, List[str]]):
            """Reverte as remoções feitas pelo forward checking."""
            for var, valor in removidos:
                if valor not in variaveis[var]:
                    variaveis[var].append(valor)

        def backtrack(atual: Dict[str, str]) -> Optional[Dict[str, str]]:
            # Verificar se a atribuição está completa
            if len(atual) == len(variaveis):
                logger.info("Solução completa encontrada!")
                return atual

            # Selecionar a próxima variável usando heurística de Menor Domínio (MRV)
            var = self.selecionar_variavel_nao_atribuida(variaveis, atual)
            logger.info(f"Selecionando variável não atribuída: {var}")

            for valor in variaveis[var]:
                logger.info(f"Tentando atribuir {valor} a {var}")
                atual[var] = valor

                if self.verificar_consistencia(atual, restricoes):
                    logger.info(f"Atribuição consistente: {var} = {valor}")

                    # Aplicar forward checking após a atribuição
                    removidos = forward_checking(var, valor, variaveis, restricoes)

                    if not any(not dominio for dominio in variaveis.values()):  # Continuar se todos os domínios têm valores
                        resultado = backtrack(atual)
                        if resultado:
                            return resultado

                    logger.info(f"Desfazendo remoções de forward checking após falha")
                    desfazer_forward_checking(removidos, variaveis)

                logger.info(f"Revertendo atribuição: {var} = {valor}")
                del atual[var]  # Reverter atribuição

            return None

        solucao = backtrack({})

        fim = time.time()
        logger.info(f"Tempo total de execução: {fim - inicio:.2f} segundos")

        if solucao:
            self.salvar_solucao_csv(solucao)
        else:
            logger.warning("Nenhuma solução encontrada.")

        return solucao

    def salvar_solucao_csv(self, solucao: Dict[str, str], filename: str = "schedule_result.csv"):
        """Salva a solução encontrada em um arquivo CSV no formato esperado."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Funcionário", "Dia", "Turno"])

            for key, value in sorted(solucao.items()):
                f, d = key.split('_')[1:]
                writer.writerow([f, d, value])

        logger.info(f"Solução salva em {filename}")

    def selecionar_variavel_nao_atribuida(self, variaveis: Dict[str, List[str]], atual: Dict[str, str]) -> str:
        """Seleciona a variável não atribuída usando uma heurística de menor domínio (MRV)."""
        return min((v for v in variaveis if v not in atual), key=lambda x: len(variaveis[x]))

    def verificar_consistencia(self, atual: Dict[str, str], restricoes: List[Dict[str, Any]]) -> bool:
        """Verifica se a atribuição atual é consistente com as restrições."""
        for restricao in restricoes:
            variaveis_restricao = restricao["variaveis"]
            valores = [atual.get(var, None) for var in variaveis_restricao]

            if all(valores) and not restricao["regra"](valores):
                logger.info(f"Inconsistência detectada: {valores} falham na restrição {restricao.get('descricao', 'sem descrição')}")
                return False

        return True
