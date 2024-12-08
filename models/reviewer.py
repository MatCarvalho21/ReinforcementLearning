from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

class Reviewer:
    def __init__(self, model_name:str="llama", temperature:float=0.8, max_tokens:int=256):
        self.chat = Ollama(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.output_parser = StrOutputParser()

    def evaluation(self, cleaned_data, used_code, score):
        """
        Avalia os dados limpos e o código utilizado, sugerindo melhorias com base no score.

        :param cleaned_data: Dados limpos após o processamento.
        :param used_code: Código usado para limpar os dados.
        :param score: A pontuação de avaliação da qualidade dos dados limpos.
        :return: Novo prompt sugerido pelo modelo.
        """
        prompt = f"""
        Dados originais: {cleaned_data}
        Código utilizado: {used_code}
        Pontuação de avaliação: {score}
        
        Com base nisso, sugira melhorias no código de limpeza e explique como a qualidade dos dados pode ser aprimorada.
        """
        
        response = self.chat.run(prompt)
        
        return self.output_parser.parse(response)

    def make_report(self, report_prompt, prompt_1, score_1, prompt_2, score_2):
        """
        Gera um relatório detalhado com base nos prompts e scores fornecidos.

        :param report_prompt: Prompt básico para gerar o relatório.
        :param prompt_1: Primeiro prompt utilizado.
        :param score_1: Score para o primeiro prompt.
        :param prompt_2: Segundo prompt utilizado.
        :param score_2: Score para o segundo prompt.
        :return: Relatório gerado.
        """
        report = f"""
        Relatório de Avaliação de Dados:
        
        Prompt 1: {prompt_1}
        Pontuação 1: {score_1}
        
        Prompt 2: {prompt_2}
        Pontuação 2: {score_2}
        
        {report_prompt}
        """
        
        response = self.chat.run(report)
        
        return self.output_parser.parse(response)
