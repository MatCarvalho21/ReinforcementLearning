# Reinforcement Learning
Repositório criado para desenvolvimento do trabalho final da disciplina de mestrado Reinforcement Learning.

# References

[MIT Deep Reinforcement Learning Class - Alexander Amini (Youtube)](https://www.youtube.com/watch?v=8JVRbHAVCws)

[Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake (Youtube)](https://www.youtube.com/watch?v=L8ypSXwyBds)

[Hands On Machine Learning - Aurélien Geron (Book)](books/Hands%20On%20Machine%20Learning%20with%20Scikit%20Learn%20and%20TensorFlow.pdf)

[Reinforcement Learning An Introduction - Richard S. Sutton, Andrew Barto (Book) ](books/Reinforcement%20Learning%20An%20Introduction%20-%20Richard%20S.%20Sutton%20and%20Andrew%20G.%20Barto.pdf)


1. Coders:
    - read_data(data, prompt) -> (cleaned_data, used_code)
    - improvement(data, improve_prompt, used_prompt, used_code) -> (cleaned_data, result_code)

2. Reviwer:
    - evaluation(cleaned_data, used_code, score) -> new_prompt
    - make_report(report_prompt, prompt_1, score_1, prompt_2, score_2) -> report

3. Judge:
    - evaluation(report) -> (score)

4. Enviorment:
    - gen_codes(data, prompt_1, prompt_2) -> (cleaned_data_1, code_1, cleaned_data_2, code_2)
    - score(cleaned_data) -> score

    - make_evaluation(cleaned_data, used_code, score) -> new_prompt

    - train_code(initial_prompt_c1, initial_prompt_c2, initial_prompt_r, n_iterations) -> (report, score_loss)

    - train(
        initial_prompt_c1,
        initial_prompt_c2,
        initial_prompt_r,
        report_prompt,
        n_iterations_code,
        n_iterations_report) -> (report, score_report, score_loss_coders)


