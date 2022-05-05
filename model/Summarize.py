from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(r'C:\Users\DEV_DN_LOCTV\Desktop\Demo_ThucTap\Summarize\content\checkpoint-65500')
tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\DEV_DN_LOCTV\Desktop\Demo_ThucTap\Summarize\content\checkpoint-65500")

def get_Summarize(sentences):
    inputs = tokenizer(sentences, max_length=512, return_tensors="pt",truncation=True)
    output_sequences = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=512,
        num_beams=4,
        repetition_penalty=1, 
        length_penalty=1, 
        early_stopping=False,
        no_repeat_ngram_size=3
    )
    sentences = tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
    return sentences[0]


