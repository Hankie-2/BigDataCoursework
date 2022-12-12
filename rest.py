from flask import *
import json
import nlp
import modify_text as mt

app = Flask(__name__)


@app.route('/prediction/', methods=['GET'])
def prediction():
    text = str(request.args.get('text'))
    text = text_pred(text)
    data_set = {'text': text}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/summarization/', methods=['GET'])
def summarization():
    text = str(request.args.get('text'))
    text = text_summ(text)
    data_set = {'text': text}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/text-generation/', methods=['GET'])
def text_generation():
    text = str(request.args.get('text'))
    text = text_gen(text)
    data_set = {'text': text}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/fill-mask/', methods=['GET'])
def fill_mask():
    text = str(request.args.get('text'))
    map = mask(text)
    data_set = {'score': map['score'], 'text': map['sequence']}
    json_dump = json.dumps(data_set)
    return json_dump


def mask(text):
    from transformers import pipeline
    unmasker = pipeline('fill-mask', model='bert-base-multilingual-cased')
    unmasker = unmasker(text)
    print(unmasker[0])
    return unmasker[0]


def text_summ(article_text):
    from transformers import AutoTokenizer, EncoderDecoderModel
    model_name = "IlyaGusev/rubert_telegram_headlines"
    tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False, do_basic_tokenize=False,
                                              strip_accents=False)
    model = EncoderDecoderModel.from_pretrained(model_name)

    input_ids = tokenizer(
        [article_text],
        add_special_tokens=True,
        max_length=256,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=64,
        no_repeat_ngram_size=3,
        num_beams=10,
        top_p=0.95
    )[0]

    headline = tokenizer.decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return headline


def text_gen(text):
    from transformers import pipeline
    generator = pipeline('text-generation', model='sberbank-ai/rugpt3large_based_on_gpt2')
    generator = generator(text, max_length=30, num_return_sequences=1)
    return generator[0]['generated_text']


def text_pred(text):
    text = mt.remove_multiple_spaces(text)
    text = mt.remove_stop_words(text)
    text = mt.lemmatize_text(text)

    prediction = nlp.logreg.predict([text])
    return prediction[0]


if __name__ == '__main__':
    app.run(port=8080)