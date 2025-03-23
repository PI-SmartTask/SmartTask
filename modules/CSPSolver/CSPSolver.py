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



class CSPSolver:
    def buscar_solucao(self, variaveis, restricoes):
        """
        Método principal que inicia o processo de busca para encontrar uma solução.
        Args:
            variaveis (dict): Variáveis e seus respectivos domínios.
            restricoes (list): Lista de restrições a serem satisfeitas.
        Returns:
            dict or None: Uma solução que satisfaz todas as restrições ou None se nenhuma solução for encontrada.
        """
        restricoes_por_var = self._organizar_restricoes_por_variavel(restricoes)
        atribuicao = {}
        logging.info("Iniciando busca com propagação de restrições...")
        return self._backtrack(variaveis, restricoes_por_var, atribuicao)

    def _organizar_restricoes_por_variavel(self, restricoes):
        """
        Organiza as restrições por variável, para facilitar a busca.
        Args:
            restricoes (list): Lista de restrições.
        Returns:
            dict: Um dicionário com as variáveis como chaves e as restrições relacionadas como valores.
        """
        restricoes_por_var = {}
        for restricao in restricoes:
            for var in restricao["variaveis"]:
                if var not in restricoes_por_var:
                    restricoes_por_var[var] = []
                restricoes_por_var[var].append(restricao)
        return restricoes_por_var

    def _backtrack(self, variaveis, restricoes_por_var, atribuicao):
        """
        Implementa o algoritmo de backtracking.
        """
        if len(atribuicao) == len(variaveis):
            return atribuicao

        var = self._escolher_variavel_nao_atribuida(variaveis, atribuicao)
        for valor in variaveis[var]:
            if self._verificar_consistencia(var, valor, atribuicao, restricoes_por_var):
                atribuicao[var] = valor
                resultado = self._backtrack(variaveis, restricoes_por_var, atribuicao)
                if resultado is not None:
                    return resultado
                del atribuicao[var]

        return None

    def _escolher_variavel_nao_atribuida(self, variaveis, atribuicao):
        """
        Escolhe a próxima variável não atribuída.
        """
        for var in variaveis.keys():
            if var not in atribuicao:
                return var
        return None

    def _verificar_consistencia(self, var, valor, atribuicao, restricoes_por_var):
        """
        Verifica se a atribuição atual é consistente com as restrições.
        """
        atribuicao_temporaria = atribuicao.copy()
        atribuicao_temporaria[var] = valor

        for restricao in restricoes_por_var.get(var, []):
            funcao = restricao["regra"]
            variaveis_da_restricao = restricao["variaveis"]

            valores = [atribuicao_temporaria.get(v, None) for v in variaveis_da_restricao]

            # Verificar se a quantidade de argumentos corresponde ao esperado na função
            if None not in valores:
                try:
                    # Ajuste: usar a quantidade correta de argumentos
                    if not funcao(*valores):
                        return False
                except TypeError as e:
                    logging.error(f"Erro de argumentos na restrição '{restricao['nome']}': {e}")
                    return False

        return True

