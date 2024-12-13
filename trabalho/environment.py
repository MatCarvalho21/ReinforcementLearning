import pandas as pd
import numpy as np
from rapidfuzz.distance import Levenshtein
from trabalho import Judge, Reviewer, Coder

class Environment:
    """
    Classe que simula um ambiente para treinamento e avaliação de codificadores
    com base em prompts e dados fornecidos.

    A classe envolve geração de códigos por dois codificadores (coder_1 e coder_2), 
    avaliação de pontuações por um juiz (judge) e revisão de códigos por um revisor (reviewer).
    """

    def __init__(self, coder_1:Coder, coder_2:Coder, reviewer:Reviewer, judge:Judge, data_list:list[pd.DataFrame], original_data:pd.DataFrame):
        """
        Inicializa a classe Environment com atributos para os codificadores, revisor, juiz e dados originais.
        """
        self.coder_1 = coder_1
        self.coder_2 = coder_2
        self.reviewer = reviewer
        self.judge = judge
        self.data_list = data_list
        self.original_data = original_data

    def generate_codes(self, data:pd.DataFrame, prompt_coder_1:str, prompt_coder_2:str) -> tuple[pd.DataFrame, str, pd.DataFrame, str]:
        """
        Gera códigos para dois codificadores baseados nos prompts fornecidos.

        Args:
            data (pd.DataFrame): Dados a serem processados pelos codificadores.
            prompt_coder_1 (str): Prompt para o primeiro codificador.
            prompt_coder_2 (str): Prompt para o segundo codificador.

        Returns:
            tuple: Dados limpos e códigos gerados por cada codificador.
        """
        cleaned_data_1, code_1 = self.coder_1.read_data(data, prompt_coder_1)

        cleaned_data_2, code_2 = self.coder_2.improvement(data, prompt_coder_2, prompt_coder_1, code_1)

        return cleaned_data_1, code_1, cleaned_data_2, code_2

    def calculate_score(self, code:str) -> float:
        """
        Calcula a distância média de Levenshtein entre os nomes dos dados originais e dos dados limpos.

        Args:
            cleaned_data (pd.DataFrame): Dados processados por um codificador.

        Returns:
            float: Distância média de Levenshtein.
        """
        prompt = f"""
        Você é um avaliador de códigos, deve avaliar o código abaixo com base na qualidade dos dados limpos.
        Leve também em conta critérios como legibilidade, eficiência e eficácia do código.
        Sua avaliação deve ser uma pontuação entre 0 e 10.
        Sua avaliação deve ser breve e curta, de preferência tendo apenas a pontuação como ponto principal.

        Código:
        {code}

        """

        result = self.reviewer.chat.invoke(prompt)

        return result

    def evaluate_and_update_prompt(self, review_prompt:str, cleaned_data:pd.DataFrame, used_code:str, score:float) -> str:
        """
        Gera um novo prompt com base na avaliação dos dados limpos, código utilizado e pontuação obtida.

        Args:
            cleaned_data (pd.DataFrame): Dados processados por um codificador.
            used_code (str): Código utilizado para gerar os dados limpos.
            score (float): Pontuação obtida na avaliação.

        Returns:
            str: Novo prompt gerado pelo revisor.
        """
        new_prompt = self.reviewer.evaluation(review_prompt, cleaned_data, used_code, score)
        return new_prompt

    def train_codifiers(self,
                        prompt_1:str, prompt_2:str,
                        reviewer_prompt:str,
                        report_prompt:str,
                        iterations:int
                        ) -> tuple[str, tuple[list[float], list[float]]]:
        """
        Treina os codificadores através de várias iterações, ajustando seus prompts com base nas avaliações.

        Args:
            data (pd.DataFrame): Dados originais para treinamento.
            prompt_1 (str): Prompt inicial do primeiro codificador.
            prompt_2 (str): Prompt inicial do segundo codificador.
            reviewer_prompt (str): Prompt utilizado pelo revisor para gerar feedback.
            report_prompt (str): Prompt utilizado para criar o relatório final.
            iterations (int): Número de iterações de treinamento.

        Returns:
            tuple: Relatório gerado, histórico de perdas dos codificadores.
        """
        score_loss_1 = list()
        score_loss_2 = list()

        for _ in range(iterations):
            i = np.random.randint(0, len(self.data_list)-1)
            data = self.data_list[i].copy()

            cleaned_data_1, code_1, cleaned_data_2, code_2 = self.generate_codes(data, prompt_1, prompt_2)

            # Calcula pontuações para ambos os codificadores
            score_1 = self.calculate_score(code_1)
            score_2 = self.calculate_score(code_2)

            # Atualiza os prompts com base nas avaliações
            prompt_1 = self.evaluate_and_update_prompt(reviewer_prompt, cleaned_data_1, code_1, score_1)
            prompt_2 = self.evaluate_and_update_prompt(reviewer_prompt, cleaned_data_2, code_2, score_2)

            # Registra as pontuações
            score_loss_1.append(score_1)
            score_loss_2.append(score_2)

        # Gera relatório final
        report = self.reviewer.make_report(report_prompt, prompt_1, score_1, code_1, prompt_2, score_2, code_2)
        return report, (score_loss_1, score_loss_2)

    def train(self, prompt_1:str, prompt_2:str, reviewer_prompt:str, report_prompt:str, iterations:int):
        """
        Treina os codificadores e avalia os relatórios gerados ao longo de múltiplos ciclos.

        Args:
            data (pd.DataFrame): Dados originais para treinamento.
            prompt_1 (str): Prompt inicial do primeiro codificador.
            prompt_2 (str): Prompt inicial do segundo codificador.
            reviewer_prompt (str): Prompt utilizado pelo revisor para gerar feedback.
            report_prompt (str): Prompt utilizado para criar o relatório final.
            iterations (int): Número de iterações de treinamento dos codificadores.

        Returns:
            tuple: Relatório final, histórico de perdas nos relatórios, histórico de perdas dos codificadores.
        """
        report, scores = self.train_codifiers(prompt_1, prompt_2, reviewer_prompt, report_prompt, iterations)
        report_score = self.judge.evaluation(report)

        return report, report_score, scores
