# %%
import dspy
import google.generativeai as genai


# Set up the LM
# llama3 = dspy.OllamaLocal(model="llama3:instruct")
gemini = dspy.Google(
    "models/gemini-1.5-flash-latest", api_key="AIzaSyARlu6PRzxIIDcr6eR5UycF26g_P4noIak"
)
dspy.settings.configure(lm=gemini)


dataset = []

import json

with open("data.json", "r") as f:
    data = json.load(f)
    for d in data:
        dataset.append(
            dspy.Example(
                project_1=d["project_1"],
                project_2=d["project_2"],
                should_investigate=d["investigate"],
            ).with_inputs("project_1", "project_2")
        )


# %%
class ShouldInvestigate(dspy.Signature):
    """Decide whether two projects are similar enough to investigate plagiarism."""

    project_1 = dspy.InputField(desc="The first project.")
    project_2 = dspy.InputField(desc="The second project.")
    answer = dspy.OutputField(
        desc="Whether the projects should be investigated. One of 'yes' or 'no'."
    )


cot = dspy.ChainOfThought(ShouldInvestigate)


sample = dataset[0]
pred = cot(project_1=sample.project_1, project_2=sample.project_2)


class fs(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        # self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(ShouldInvestigate)

    def forward(self, project_1, project_2):
        prediction = self.generate_answer(project_1=project_1, project_2=project_2)
        return dspy.Prediction(
            project_1=project_1, project_2=project_2, answer=prediction.answer
        )


if __name__ == "__main__":
    from dspy.teleprompt import BootstrapFewShot

    def validate_answer(example, prediction, trace=None):
        return example.should_investigate == prediction.answer.lower()

    optimizer = BootstrapFewShot(metric=validate_answer)
    optimizer.max_errors = 1
    optimized_cot = optimizer.compile(fs(), trainset=dataset)

    # %%

    from dspy.evaluate import Evaluate

    evaluate = Evaluate(
        metric=validate_answer,
        devset=dataset,
        num_threads=1,
        display_progress=True,
        display_table=10,
    )

    evaluate(optimized_cot)

    optimized_cot.save("optimized_cot.json")

    # %%
