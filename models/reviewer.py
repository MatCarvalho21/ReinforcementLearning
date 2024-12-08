from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

class Reviewer:
    def __init__(self, model_name, temperature=0.8, num_predict=256):
        self.chain = ChatOllama(
            model=model_name,
            temperature=temperature,
            num_predict=num_predict
        )
        self.parser = StrOutputParser()

    def review(self, context, question):
        response = self.chain.run(context=context, question=question)
        return response


try:
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    chat = ChatOllama(
        model = "llama3.2:3b",
        temperature = 0.4,
        num_predict = 256,
    )
except:
    print("Error initializing ChatOllama, try install Ollama or llama3.2:3b model")
    sys.exit(1)

chain = prompt | chat | StrOutputParser()


