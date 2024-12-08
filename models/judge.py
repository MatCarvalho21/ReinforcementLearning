from pandasai.llm.ollama import Ollama

class Judge:
    """
    Classe para avaliação de relatórios usando um LLM (Large Language Model) com base em um prompt pré-definido.
    """

    def __init__(self, model_name: str = "llama", prompt_file: str = "judge_prompt.txt"):
        """
        Inicializa o Judge com um modelo LLM e um arquivo de prompt.

        Args:
            model_name (str): Nome do modelo a ser usado (padrão: "llama").
            prompt_file (str): Caminho para o arquivo de texto contendo o prompt do juiz.
        """
        self.model = Ollama(model_name)
        self.prompt_file = prompt_file
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        """
        Carrega o prompt do arquivo especificado.

        Returns:
            str: Conteúdo do prompt.
        """
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file '{self.prompt_file}' not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the prompt: {e}")

    def evaluation(self, report: str) -> float:
        """
        Avalia o relatório fornecido com base no modelo LLM e no prompt carregado.

        Args:
            report (str): Relatório a ser avaliado.

        Returns:
            float: Pontuação atribuída pelo LLM.
        """
        # Construção do input para o LLM
        input_text = f"{self.prompt}\n\nRelatório a ser avaliado:\n{report}\n\nPor favor, forneça uma pontuação de 0 a 10:"
        
        # Consulta ao modelo
        try:
            response = self.model.run(input_text)
            score = self._extract_score(response)
            return score
        except Exception as e:
            raise RuntimeError(f"An error occurred during evaluation: {e}")

    def _extract_score(self, response: str) -> float:
        """
        Extrai a pontuação da resposta do modelo.

        Args:
            response (str): Resposta do LLM.

        Returns:
            float: Pontuação extraída.

        Raises:
            ValueError: Se a pontuação não puder ser extraída.
        """
        try:
            # Busca pela pontuação na resposta (assume formato "Pontuação: X")
            for line in response.split("\n"):
                if "Pontuação:" in line:
                    score = float(line.split(":")[1].strip())
                    return score
            raise ValueError("Pontuação não encontrada na resposta.")
        except Exception as e:
            raise ValueError(f"Erro ao extrair a pontuação da resposta: {e}")
