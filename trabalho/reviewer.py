from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

class Reviewer:
    def __init__(self, model_name:str="llama", temperature:float=0.8, max_tokens:int=256):
        self.chat = OllamaLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.output_parser = StrOutputParser()

    def evaluation(self, review_prompt:str, cleaned_data:str, used_code:str, score:int) -> str:
        """
        Avalia os dados limpos e o código utilizado, sugerindo melhorias com base no score.

        :param cleaned_data: Dados limpos após o processamento.
        :param used_code: Código usado para limpar os dados.
        :param score: A pontuação de avaliação da qualidade dos dados limpos.
        :return: Novo prompt sugerido pelo modelo.
        """
        prompt = f"""
        {review_prompt}

        Dados originais: {cleaned_data}
        Código utilizado: {used_code}
        Pontuação de avaliação: {score}
        
        Com base nisso, sugira melhorias no código de limpeza e explique como a qualidade dos dados pode ser aprimorada.
        """
        
        response = self.chat.invoke(prompt)
        
        return self.output_parser.parse(response)

    def make_report(self, report_prompt:str, prompt_1:str, score_1:int, code_1:str, prompt_2:str, score_2:int,  code_2:str) -> str:
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
        {report_prompt}
        
        Prompt 1: {prompt_1}
        Pontuação 1: {score_1}
        Código 1: {code_1}
        
        Prompt 2: {prompt_2}
        Pontuação 2: {score_2}
        Código 2: {code_2}        

        """
        
        response = self.chat.invoke(report)
        
        return self.output_parser.parse(response)
