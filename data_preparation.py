import string
import numpy as np
from collections import Counter


class data_preparation:
    def __init__(self,reviews, labels):
        reviews = open(reviews, 'r')
        labels = open(labels,'r')
        self.reviews  = list(map(lambda x:x[:-1], reviews.readlines()))
        self.labels = list(map(lambda x:x[:-1], labels.readlines()))
        self.remove_punctuation()
        self.word_to_count()
        self.word_ratio()
        self.word2index_mapper = {}
        for i,word in enumerate(set(self.total_count.keys())):
            self.word2index_mapper[word] = i



    def remove_punctuation(self):
        self.reviews = [r.translate(str.maketrans('','',string.punctuation)) for r in self.reviews]
        self.labels = [r.translate(str.maketrans('','',string.punctuation)) for r in self.labels]

    def word_to_count(self):
        self.postive_count = Counter()
        self.negative_count = Counter()
        self.total_count = Counter()

        for i in range(len(self.reviews)):
            print('\r{}'.format(i),end="")
            if self.labels[i] == 'positive':
                for word in self.reviews[i].split(' '):
                    self.postive_count[word]+=1
                    self.total_count[word]+=1
            else:
                for word in self.reviews[i].split(' '):
                    self.negative_count[word]+=1
                    self.total_count[word]+=1

    def word_ratio(self):
        self.word_ratio = Counter()

        for term,count in list(self.total_count.most_common()):
            if (count > 100):
                self.word_ratio[term] = np.log(self.postive_count[term] / float(self.negative_count[term]+1))
        # print()
        # print(self.word_ratio['the'])
        # print(self.word_ratio['superb'])
        # print(self.word_ratio['insult'])


    def get_input_data(self,start=0,to=-1):
        input_data = []
        row = np.zeros((1, len(self.word2index_mapper)))

        i = 0

        for review in self.reviews[start:to]:
            row *= 0
            print('\rReview: {}'.format(i), end="")
            i+=1
            for word in review.split(" "):
                row[0][self.word2index_mapper.get(word)]=1

            input_data.append(row.copy())

        return np.array(np.squeeze(input_data))
    def get_output_data(self,start=0,to=-1):
        target_data = []

        for label in self.labels[start:to]:
            if (label == 'positive'):
                target_data.append([1,0])
            else:
                target_data.append([0,1])


        return np.array(target_data)


