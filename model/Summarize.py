from summarizer import Summarizer,TransformerSummarizer
model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")


def get_correct_sum(text,input_len):
    text = str(text)
    full = ''.join(model(text, min_length=input_len))
    return full
