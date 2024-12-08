from pandasai import PandasAI
from pandasai.llm.ollama import Ollama
import pandas as pd

class Coders:
    def __init__(self, model_name:str="llama"):
        """
        Inicializa o Coders com um modelo Ollama local.

        :param model_name: Nome do modelo Ollama local (default: 'llama').
        """
        self.llm = Ollama(model_name=model_name)
        self.pandas_ai = PandasAI(self.llm, save_code=True)

    def read_data(self, data:pd.DataFrame, prompt:str):
        """
        Processa os dados com base em um prompt.

        :param data: DataFrame a ser processado.
        :param prompt: Pergunta ou instrução em linguagem natural.
        :return: Uma tupla (cleaned_data, used_code).
        """
        cleaned_data = self.pandas_ai.run(data, prompt=prompt)
        used_code = self.pandas_ai._last_code_generated
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
        cleaned_data = self.pandas_ai.run(data, prompt=combined_prompt)
        result_code = self.pandas_ai._last_code_generated
        return cleaned_data, result_code
