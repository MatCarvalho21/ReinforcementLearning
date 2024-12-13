from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

class Judge:
    """
    Classe para avaliação de relatórios usando um LLM (Large Language Model) com base em um prompt pré-definido.
    """

    def __init__(self, prompt:str, model_name:str="llama3.2:3b", temperature:float=0.8, max_tokens:int=256):
        """
        Inicializa o Judge com um modelo LLM e um arquivo de prompt.

        Args:
            model_name (str): Nome do modelo a ser usado (padrão: "llama3.2:3b").
            prompt_file (str): Caminho para o arquivo de texto contendo o prompt do juiz.
            temperature (float): Temperatura para amostragem de tokens (padrão: 0.8).
            max_tokens (int): Número máximo de tokens a serem gerados (padrão: 256).
        """
        self.model = OllamaLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.prompt = prompt
        self.output_parser = StrOutputParser()

    def evaluation(self, report: str) -> float:
        """
        Avalia o relatório fornecido com base no modelo LLM e no prompt carregado.

        Args:
            report (str): Relatório a ser avaliado.

        Returns:
            float: Pontuação atribuída pelo LLM.
        """
        # Construção do input para o LLM
        input_text = f"{self.prompt}\n\nRelatório a ser avaliado:\n{report}\n\nPor favor, seguindo os critérios fornecidos, dê uma pontuação para o relatório:"
        
        # Consulta ao modelo
        try:
            response = self.model.invoke(input_text)
            score = self.output_parser.parse(response)
            return score
        except Exception as e:
            raise RuntimeError(f"An error occurred during evaluation: {e}")

