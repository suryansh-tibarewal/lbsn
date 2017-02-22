import gensim

f = open('interests_list.txt', 'r')
content = f.read()
interests_list = list()
for interest in content.split(','):
    interest = interest.strip()
    interest = interest.replace(" ", "_")
    interests_list.append(interest)
print interests_list
f.close()
model = gensim.models.Word2Vec.load_word2vec_format('word2vec_models/GoogleNews-vectors-negative300.bin', binary=True)
for interest1 in interests_list:
    for interest2 in interests_list:
        value = model.similarity(interest1, interest2)
        print interest1, interest2, value