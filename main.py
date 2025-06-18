import sys
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def lexical_diversity(text):
    tokens = nltk.word_tokenize(text)
    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens)

def preprocess_text(raw_text):
    tokens = nltk.word_tokenize(raw_text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english') and len(word) > 5]
    lemmatizer = WordNetLemmatizer()
    lemmas = set(lemmatizer.lemmatize(token) for token in tokens)
    
    tagged = pos_tag(list(lemmas))
    print("First 20 tagged words:", tagged[:20])
    
    nouns = [word for word, tag in tagged if tag.startswith('NN')]
    print("Total filtered tokens:", len(tokens))
    print("Number of nouns:", len(nouns))
    
    return tokens, nouns

def create_noun_frequency(tokens, nouns):
    noun_counts = Counter(word for word in tokens if word in nouns)
    most_common = noun_counts.most_common(50)
    for word, count in most_common:
        print(word, count)
    return [word for word, count in most_common]

def guessing_game(top_nouns):
    score = 5
    print("Let's play a word guessing game!")
    
    while score >= 0:
        word = random.choice(top_nouns)
        guessed = ["_"] * len(word)
        guessed_letters = set()

        while score >= 0 and "_" in guessed:
            print(" ".join(guessed))
            guess = input("Guess a letter: ").lower()

            if guess == "!":
                print("Game exited.")
                return
            elif guess in guessed_letters:
                print("Already guessed that letter.")
                continue

            guessed_letters.add(guess)

            if guess in word:
                print("Right!")
                score += 1
                for i, char in enumerate(word):
                    if char == guess:
                        guessed[i] = guess
            else:
                print("Sorry, guess again.")
                score -= 1

            print("Score is", score)

        if "_" not in guessed:
            print("You solved it! Word:", word)
        if score < 0:
            print("Game over. Final score:", score)
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide a filename as a system argument.")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    diversity = lexical_diversity(raw_text)
    print(f"Lexical diversity:", diversity)

    tokens, nouns = preprocess_text(raw_text)
    top_nouns = create_noun_frequency(tokens, nouns)
    guessing_game(top_nouns)
