from lxml import etree
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import download
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# download('averaged_perceptron_tagger')
tree = etree.parse("news.xml")
root = tree.getroot()
stop_punct = stopwords.words("english") + list(string.punctuation)
lemmatizer = WordNetLemmatizer()
vectorizer = TfidfVectorizer()

head, text = [], []
for value in root.iter("value"):  # to find tags with value.
    if value.attrib["name"] == "head":  # finding "name" attribute with value "head".
        head.append(value.text)  # created headers list
    elif value.attrib["name"] == "text":
        token = word_tokenize(value.text.lower())
        content = [lemmatizer.lemmatize(word, pos="n") for word in token]
        content = [word for word in content if word not in stop_punct]
        content = [word for word in content if pos_tag([word])[0][1] == "NN"]
        value = " ".join(content)
        text.append(value)  # created story list

tfidf_matrix = vectorizer.fit_transform(text)  # created vector for story in all stories
terms = vectorizer.get_feature_names()  # created terms list
document, word = tfidf_matrix.shape  # found Document and terms length

for d in range(document):
    word_dict = {}
    for w in range(word):
        word_dict.update({terms[w]: tfidf_matrix[(d, w)]})  # for each story in document created word score
    result = sorted(word_dict.items(), key=lambda x: (x[1], x[0]), reverse=True)
    print(f"{head[d]}:")
    print(*[k for k, v in result[:5]])
