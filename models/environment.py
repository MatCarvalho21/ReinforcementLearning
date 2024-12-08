import pandas as pd
from rapidfuzz.distance import Levenshtein

class Environment:
    """
    Classe que simula um ambiente para treinamento e avaliação de codificadores
    com base em prompts e dados fornecidos.

    A classe envolve geração de códigos por dois codificadores (coder_1 e coder_2), 
    avaliação de pontuações por um juiz (judge) e revisão de códigos por um revisor (reviewer).
    """

    def __init__(self):
        """
        Inicializa a classe Environment com atributos para os codificadores, revisor, juiz e dados originais.
        """
        self.coder_1 = None
        self.coder_2 = None
        self.reviewer = None
        self.judge = None
        self.original_data = None

    def generate_codes(self, data, prompt_coder_1, prompt_coder_2):
        """
        Gera códigos para dois codificadores baseados nos prompts fornecidos.

        Args:
            data (pd.DataFrame): Dados a serem processados pelos codificadores.
            prompt_coder_1 (str): Prompt para o primeiro codificador.
            prompt_coder_2 (str): Prompt para o segundo codificador.

        Returns:
            tuple: Dados limpos e códigos gerados por cada codificador.
        """
        cleaned_data_1, code_1 = self.coder_1.gen_code(data, prompt_coder_1)
        cleaned_data_2, code_2 = self.coder_2.gen_code(data, prompt_coder_2)
        return cleaned_data_1, code_1, cleaned_data_2, code_2

    def calculate_score(self, cleaned_data):
        """
        Calcula a distância média de Levenshtein entre os nomes dos dados originais e dos dados limpos.

        Args:
            cleaned_data (pd.DataFrame): Dados processados por um codificador.

        Returns:
            float: Distância média de Levenshtein.
        """
        distances = [
            Levenshtein.distance(original, cleaned)
            for original, cleaned in zip(self.original_data["Name"], cleaned_data["Name"])
        ]
        return sum(distances) / len(distances)

    def evaluate_and_update_prompt(self, cleaned_data, used_code, score):
        """
        Gera um novo prompt com base na avaliação dos dados limpos, código utilizado e pontuação obtida.

        Args:
            cleaned_data (pd.DataFrame): Dados processados por um codificador.
            used_code (str): Código utilizado para gerar os dados limpos.
            score (float): Pontuação obtida na avaliação.

        Returns:
            str: Novo prompt gerado pelo revisor.
        """
        new_prompt = self.reviewer.evaluation(cleaned_data, used_code, score)
        return new_prompt

    def train_codifiers(self, data, prompt_1, prompt_2, reviewer_prompt, report_prompt, iterations):
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
        score_loss_1 = []
        score_loss_2 = []

        for _ in range(iterations):
            cleaned_data_1, code_1, cleaned_data_2, code_2 = self.generate_codes(data, prompt_1, prompt_2)

            # Calcula pontuações para ambos os codificadores
            score_1 = self.calculate_score(cleaned_data_1)
            score_2 = self.calculate_score(cleaned_data_2)

            # Atualiza os prompts com base nas avaliações
            prompt_1 = self.evaluate_and_update_prompt(cleaned_data_1, code_1, score_1)
            prompt_2 = self.evaluate_and_update_prompt(cleaned_data_2, code_2, score_2)

            # Registra as pontuações
            score_loss_1.append(score_1)
            score_loss_2.append(score_2)

        # Gera relatório final
        report = self.reviewer.make_report(reviewer_prompt, prompt_1, score_1, prompt_2, score_2)
        return report, (score_loss_1, score_loss_2)

    def train(self, data, prompt_1, prompt_2, reviewer_prompt, report_prompt, iterations, report_iterations):
        """
        Treina os codificadores e avalia os relatórios gerados ao longo de múltiplos ciclos.

        Args:
            data (pd.DataFrame): Dados originais para treinamento.
            prompt_1 (str): Prompt inicial do primeiro codificador.
            prompt_2 (str): Prompt inicial do segundo codificador.
            reviewer_prompt (str): Prompt utilizado pelo revisor para gerar feedback.
            report_prompt (str): Prompt utilizado para criar o relatório final.
            iterations (int): Número de iterações de treinamento dos codificadores.
            report_iterations (int): Número de iterações de treinamento e avaliação dos relatórios.

        Returns:
            tuple: Relatório final, histórico de perdas nos relatórios, histórico de perdas dos codificadores.
        """
        report_loss = []
        final_report = None
        final_scores_coders = None

        for _ in range(report_iterations):
            report, scores = self.train_codifiers(data, prompt_1, prompt_2, reviewer_prompt, report_prompt, iterations)
            report_score = self.judge.evaluation(report) 
            report_loss.append(report_score)

            final_report = report
            final_scores_coders = scores

        return final_report, report_loss, final_scores_coders
