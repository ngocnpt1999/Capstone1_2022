from unittest import result
import torch
from vncorenlp import VnCoreNLP
from transformers import AutoTokenizer,EncoderDecoderModel,AutoModel,AutoModelForSeq2SeqLM


def text(input_text):
    tokenizer = AutoTokenizer.from_pretrained("./content/checkpoint-52000")
    model = AutoModelForSeq2SeqLM.from_pretrained("./content/checkpoint-52000")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    with torch.no_grad():
        tokenized_text = tokenizer(input_text, truncation=True, padding=True, return_tensors='pt')
    
        source_ids = tokenized_text['input_ids'].to(device, dtype = torch.long)
        source_mask = tokenized_text['attention_mask'].to(device, dtype = torch.long)
    
        generated_ids = model.generate(
        input_ids = source_ids,
        attention_mask = source_mask, 
        max_length=512,
        num_beams=5,
        repetition_penalty=1, 
        length_penalty=1, 
        early_stopping=True,
        no_repeat_ngram_size=2
    )
        pred = tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

    return pred
    
inputtext = "Tôi là sinh_viên trường đại_học Công_nghệ ."
result = text(inputtext)
print(result)