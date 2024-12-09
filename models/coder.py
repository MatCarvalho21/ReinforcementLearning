import pandas as pd
from pandasai import SmartDataframe
from langchain_ollama import OllamaLLM

class Coder:
    def __init__(self, model_name:str="llama", temperature:float=0.8, max_tokens:int=256):
        """
        Inicializa o Coders com um modelo Ollama local.

        :param model_name: Nome do modelo Ollama local (default: 'llama').
        """
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

    def read_data(self, data:pd.DataFrame, prompt:str) -> tuple[pd.DataFrame, str]:
        """
        Processa os dados com base em um prompt.

        :param data: DataFrame a ser processado.
        :param prompt: Pergunta ou instrução em linguagem natural.
        :return: Uma tupla (cleaned_data, used_code).
        """
        smart_df = SmartDataframe(data, config={"llm": self.llm,
                                                "custom_whitelisted_dependencies": ["re", "io"]})

        cleaned_data = smart_df.chat(prompt)
        used_code = smart_df.last_code_generated

        del smart_df

        return cleaned_data, used_code

    def improvement(self, data:pd.DataFrame, improve_prompt:str, used_prompt:str, used_code:str) -> tuple[pd.DataFrame, str]:
        """
        Melhora os dados ou a análise com base em um novo prompt.

        :param data: DataFrame a ser melhorado.
        :param improve_prompt: Novo prompt para melhorar a análise.
        :param used_prompt: Prompt original usado anteriormente.
        :param used_code: Código gerado anteriormente.
        :return: Uma tupla (cleaned_data, result_code).
        """
        combined_prompt = (
            f"Baseado em: '{used_prompt}'\n"
            f"E no código usado:\n{used_code}\n"
            f"Tente aplicar as seguintes melhoras ao código se necessário e executar novamente: {improve_prompt}"
        )
        
        smart_df = SmartDataframe(data, config={"llm": self.llm,
                                                "custom_whitelisted_dependencies": ["re", "io"]})

        cleaned_data = smart_df.chat(combined_prompt)
        result_code = smart_df.last_code_generated

        del smart_df

        return cleaned_data, result_code
