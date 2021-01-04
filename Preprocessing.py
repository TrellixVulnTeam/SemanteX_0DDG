import spacy


def clean_data(data):
    print(data)


def get_vector(filtered_tokens):
    filtered_tokens = filtered_tokens[0].vector
    return filtered_tokens


def lemmanization(filtered_tokens):
    lemmas = [
        f"Token: {token} = lemma: {token.lemma_}"
        for token in filtered_tokens
    ]
    return lemmas


def remove_stopwords(tokens):
    filtered_tokens = [token for token in tokens if not token.is_stop]
    return filtered_tokens


def tokenizer_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    token_list = [token for token in doc]
    return token_list


def get_vector(filtered_tokens):
    filtered_tokens = filtered_tokens[0].vector
    return filtered_tokens


def lemmanization(filtered_tokens):
    lemmas = [
        f"Token: {token} = lemma: {token.lemma_}"
        for token in filtered_tokens
    ]
    return lemmas


def remove_stopwords(tokens):
    filtered_tokens = [token for token in tokens if not token.is_stop]
    return filtered_tokens


def tokenizer_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    token_list = [token for token in doc]
    return token_list