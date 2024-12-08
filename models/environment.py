

class Environment():

    def __init__(self):
        self.coder1 = None
        self.coder2 = None
        self.rewier = None
        self.judge = None
        self.original_data = None


    def gen_codes(self, data, prompt_1, prompt_2):
        cleaned_data_1, code_1 = self.coder1.gen_code(data, prompt_1)
        cleaned_data_2, code_2 = self.coder2.gen_code(data, prompt_2)
        return cleaned_data_1, code_1, cleaned_data_2, code_2
    
    def score(self, cleaned_data):
        score = livenshtein_distance(cleaned_data, self.original_data)
        return score
    
    def make_evaluation(self, cleaned_data, used_code, score):
        new_prompt = self.rewier.evaluation(cleaned_data, used_code, score)
        return new_prompt
    
    def train_code(self, data, prompt_1, prompt_2, prompt_rewier, n_it):
        prompt_coder_1 = prompt_1
        prompt_coder_2 = prompt_2
        score_loss_1 = []
        score_loss_2 = []
        for i in range(n_it):
            cleaned_data_1, code_1, cleaned_data_2, code_2 = self.gen_codes(data, prompt_coder_1, prompt_coder_2)
            score_1 = self.score(cleaned_data_1)
            score_2 = self.score(cleaned_data_2)
            prompt_coder_1 = self.make_evaluation(cleaned_data_1, code_1, score_1)
            prompt_coder_2 = self.make_evaluation(cleaned_data_2, code_2, score_2)
            score_1 = self.score(cleaned_data_1)
            score_loss_1.append(score_1)
            score_loss_2.append(score_2)

        report = self.rewier.make_report(prompt_rewier, prompt_coder_1, score_1, prompt_coder_2, score_2)
        return report, (score_loss_1, score_loss_2), 
    
    def gen_report()
    
    def train(self, data, prompt_1, prompt_2):
        pass

    
    make_evaluation(cleaned_data, used_code, score) -> new_prompt
        - gen_codes(data, prompt_1, prompt_2) -> (cleaned_data_1, code_1, cleaned_data_2, code_2)
    - score(cleaned_data) -> score