import os
import spacy
import random
import tarfile
from spacy.util import minibatch, compounding


def test_model(text):
    # Load saved trained model
    loaded_model = spacy.load("model_artifacts")
    # Generate prediction
    parsed_text = loaded_model(text)
    # Determine prediction to return
    if parsed_text.cats["pos"] > parsed_text.cats["neg"]:
        prediction = "Positive"
        score = parsed_text.cats["pos"]
    else:
        prediction = "Negative"
        score = parsed_text.cats["neg"]
    print(
        f"Review text: {text}\n"
        f"Predicted sentiment: {prediction}\n"
        f"Score: {score}\n"
    )


def evaluate_model(tokenizer, textcat, test_data: list) -> dict:
    reviews, labels = zip(*test_data)
    reviews = (tokenizer(review) for review in reviews)
    true_positives = 0
    false_positives = 1e-8  # Can't be 0 because of presence in denominator
    true_negatives = 0
    false_negatives = 1e-8
    for i, review in enumerate(textcat.pipe(reviews)):
        true_label = labels[i]["cats"]
        for predicted_label, score in review.cats.items():
            # Every cats dictionary includes both labels. You can get all
            # the info you need with just the pos label.
            if predicted_label == "neg":
                continue
            if score >= 0.5 and true_label["pos"]:
                 true_positives += 1
            elif score >= 0.5 and true_label["neg"]:
                false_positives += 1
            elif score < 0.5 and true_label["neg"]:
                true_negatives += 1
            elif score < 0.5 and true_label["pos"]:
                false_negatives += 1
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    if precision + recall == 0:
        f_score = 0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"precision": precision, "recall": recall, "f-score": f_score}


def train_model(training_data: list, test_data: list, iterations: int = 10):
    # Build pipeline
    nlp = spacy.load("en_core_web_sm")
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.create_pipe("textcat", config={"architecture": "simple_cnn"})
        nlp.add_pipe(textcat, last=True)
    else:
        textcat = nlp.get_pipe("textcat")
    textcat.add_label("pos")
    textcat.add_label("neg")
    # Train only textcat
    training_excluded_pipes = [pipe for pipe in nlp.pipe_names if pipe != "textcat"]
    with nlp.disable_pipes(training_excluded_pipes):
        optimizer = nlp.begin_training()
        # Training loop
        print("Beginning training")
        print("{:>20}{:>20}{:>20}{:>20}".format('Loss', 'Precision', 'Recall', 'F-score'))
        batch_sizes = compounding(4.0, 32.0, 1.001)  # A generator that yields infinite series of input numbers
        for i in range(iterations):
            loss = {}
            random.shuffle(training_data)
            batches = minibatch(training_data, size=batch_sizes)
            for batch in batches:
                text, labels = zip(*batch)
                nlp.update(
                    text,
                    labels,
                    drop=0.2,
                    sgd=optimizer,
                    losses=loss
                )
            with textcat.model.use_params(optimizer.averages):
                evaluation_results = evaluate_model(
                    tokenizer=nlp.tokenizer,
                    textcat=textcat,
                    test_data=test_data
                )
                print("{:>20.5f}{:>20.5f}{:>20.5f}{:>20.5f}".format(loss['textcat'],
                                                                    evaluation_results['precision'],
                                                                    evaluation_results['recall'],
                                                                    evaluation_results['f-score']))
    # Save model
    with nlp.use_params(optimizer.averages):
        nlp.to_disk("model_artifacts")


def load_training_data(
    data_directory: str = "aclImdb/train",
    split: float = 0.8,
    limit: int = 0) -> tuple:
    # Load from files
    reviews = []
    for label in ["pos", "neg"]:
        labeled_directory = f"{data_directory}/{label}"
        for review in os.listdir(labeled_directory):
            if review.endswith(".txt"):
                with open(f"{labeled_directory}/{review}") as f:
                    text = f.read()
                    text = text.replace("<br />", "\n\n")
                    if text.strip():
                        spacy_label = {
                            "cats": {
                                "pos": "pos" == label,
                                "neg": "neg" == label
                            }
                        }
                        reviews.append((text, spacy_label))
    random.shuffle(reviews)
    if limit:
        reviews = reviews[:limit]
    split = int(len(reviews) * split)
    return reviews[:split], reviews[split:]


if __name__ == "__main__":
    os.chdir(os.path.relpath('/Users/dankevich.te/Downloads/'))
    fname = 'aclImdb_v1.tar.gz'
    with tarfile.open(fname, "r:gz") as tar:
        tar.extractall()
        tar.close()
    # train, test = load_training_data(limit=5000)
    # train_model(train, test)
    print("Testing model")
    test_model("I would buy a new iphone")
    # f = open('tweets.txt', 'r')
    # for line in f:
    #     TEXT = line
    #     test_model(TEXT)