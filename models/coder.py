import pandas as pd
from pandasai import SmartDataframe
from langchain_community.llms import Ollama

class Coders:
    def __init__(self, model_name:str="llama"):
        """
        Inicializa o Coders com um modelo Ollama local.

        :param model_name: Nome do modelo Ollama local (default: 'llama').
        """
        self.llm = Ollama(model=model_name)

    def read_data(self, data:pd.DataFrame, prompt:str):
        """
        Processa os dados com base em um prompt.

        :param data: DataFrame a ser processado.
        :param prompt: Pergunta ou instrução em linguagem natural.
        :return: Uma tupla (cleaned_data, used_code).
        """
        smart_df = SmartDataframe(data, config={"llm": self.llm}, save_code=True)

        cleaned_data = smart_df.chat(prompt, dataframe_only=True)
        used_code = smart_df.last_code_generated

        return cleaned_data, used_code

    def improvement(self, data:pd.DataFrame, improve_prompt:str, used_prompt:str, used_code:str):
        """
        Melhora os dados ou a análise com base em um novo prompt.

        :param data: DataFrame a ser melhorado.
        :param improve_prompt: Novo prompt para melhorar a análise.
        :param used_prompt: Prompt original usado anteriormente.
        :param used_code: Código gerado anteriormente.
        :return: Uma tupla (cleaned_data, result_code).
        """
        combined_prompt = (
            f"Based on the original prompt: '{used_prompt}'\n"
            f"And the code used:\n{used_code}\n"
            f"Now, perform the following improvement: {improve_prompt}"
        )
        
        smart_df = SmartDataframe(data, config={"llm": self.llm}, save_code=True)

        cleaned_data = smart_df.chat(combined_prompt, dataframe_only=True)
        result_code = smart_df.last_code_generated

        return cleaned_data, result_code
