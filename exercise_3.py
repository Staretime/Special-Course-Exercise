import nltk
from nltk import pos_tag
import string
from nltk.corpus import stopwords
from nltk.corpus import gutenberg
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt


class Exercise3(object):
    def __init__(self):
        nltk.download('gutenberg')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

    def save_answer(self, file_name, info):
        with open(file_name, "w") as f:
            f.write(str(info))

    def deal(self):
        nltk.corpus.gutenberg.fileids()
        moby_dick = gutenberg.raw("melville-moby_dick.txt")

        # Tokenization Moby Dick
        tokens = nltk.word_tokenize(moby_dick)
        self.save_answer("answer1.txt", tokens)

        # Stop-words filtering: Filters out the stopwords from the above tokens.
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        self.save_answer("answer2.txt", filtered_tokens)

        # POS frequency: The program then counts and displays ... and their total counts (frequency).
        word_tags = pos_tag(filtered_tokens)
        self.save_answer("answer3.txt", word_tags)

        # POS frequency: The program then counts and displays the 5 most ... and their total counts (frequency).
        pos_dict = {}
        punctuations = string.punctuation
        for word, pos in word_tags:
            if word[0] in punctuations:
                continue
            if pos not in pos_dict:
                pos_dict[pos] = 0
            pos_dict[pos] += 1

        sorted_pos_tup = sorted(pos_dict.items(), key=lambda x: x[1], reverse=True)
        pos_string = ""
        for pos, frequency in sorted_pos_tup[:5]:
            pos_string += f"{pos}: {frequency}\n"
        self.save_answer("answer4.txt", pos_string)

        # Lemmatization: Using the pos-tagged tokens, ... the root of “singing”, “singer”, “sings”, “sang”, and “sung” is “sing”.
        lemmatizer = WordNetLemmatizer()
        top_20_tokens = [token for token, _ in word_tags[:20]]
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in top_20_tokens]
        self.save_answer("answer5.txt", lemmatized_tokens)

        # Plotting frequency distribution: At the end, ... and their total occurrences are plotted as a bar chart.
        datearr = list(pos_dict.keys())
        num_masks = list(pos_dict.values())
        fig = plt.figure(figsize=(15, 6))
        plt.xlabel('pos', fontsize=9)
        plt.ylabel('frequency', fontsize=9)
        plt.title('6.Plotting frequency distribution', fontsize=12)
        plt.bar(datearr, num_masks, width=0.3)
        plt.savefig('answer6.jpg', dpi=1000)
        plt.show()


if __name__ == '__main__':
    exercise = Exercise3()
    exercise.deal()
