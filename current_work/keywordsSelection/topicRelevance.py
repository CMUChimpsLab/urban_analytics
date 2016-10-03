import gensim, logging
# import word2vec
import numpy as np

topic = [
    ['traffic', 'transport', 'bus', 'escort', 'shuttle', 'megabus', 'taxi', 'uber',
     'lyft', 'authority', 'cab', 'port', 'intersection', 'highway', 'drive', 'transportation',
     '71d', 'avenue', 'driveway', 'lane', 'drove'],
    ['noise', 'noisy', 'quiet', 'loudly', 'loud', 'beep', 'louder', 'silence'],
    ['neighbor', 'neighborhood'],
    ['plaza', 'apartment', 'dorm', 'bedroom'],
    ['shopping', 'market', 'purchase', 'sale', 'wholesale', 'outlet', 'store', 'discount', 'vendor',
     'coupon', 'grocery', 'walmart', 'retail', 'mall', 'procurement', 'nordstrom'],
    ['banquet', 'dine', 'restaurant', 'cafeteria', 'cafe', 'eatery', 'pizzeria', 'ristorante', 'cuisine',
     'steakhouse', 'deli', 'qdoba', 'pasta', 'sushi', 'primantis', 'toast', 'grill', 'delicious', 'menu',
     'chili', 'noodlehead', 'burrito', 'primanti', 'burger', 'bakery', 'cakery', 'spaghetti', 'roast',
     'hibachi', 'falafel', 'dibellas', 'coleslaw', 'chilly', 'brueggers', 'pierogies', 'schmicks', 'seafood', 'mccormick'],
    ['beer', 'cocktail', 'liquor', 'pub', 'bar', 'wine', 'champagne', 'gin', 'vodka', 'martini',
     'whiskey', 'ale', 'lager', 'alcohol', 'tequila', 'tavern', 'bartender', 'hoppy', 'pilsner',
     'bourbon', 'rum', 'fuddle', 'mead', 'yuengling', 'margarita'],
    ['criminal', 'arrest', 'assault', 'robbery', 'shooting', 'crime', 'violent', 'perp', 'gun', 'drag',
     'safety', 'steal'],
    ['basketball', 'nba', 'ballpark', 'coach', 'superbowl', 'baseball', 'hockey', 'ncaa', 'coached',
     'football', 'rebound', 'nfl', 'steeler', 'pitcher', 'tennis', 'golf', 'couch', 'tournament',
     'steelers', 'soccer', 'espn', 'athletics', 'stadium', 'steelersnation', 'mlb', 'dunk'],
    ['therapy', 'surgery', 'lifecare', 'ward', 'upmc', 'medic', 'doctor', 'medicine', 'dentist',
     'patient', 'nursing', 'icu', 'hospital', 'clinical'],
    ['garbage', 'trash', 'scum']
    ]

model = gensim.models.Word2Vec.load('modelOut.txt')
vocab = model.vocab
# vocab = model.get_vocab()

for i in range(11):
    temp = model.most_similar(positive=[topic[i][0]], topn=100000000)
    outValue = {}
    outValue[topic[i][0]] = 1
    for tt in temp:
        outValue[tt[0]] = tt[1]
    for j in range(1,len(topic[i])):
        temp = model.most_similar(positive=[topic[i][j]], topn=100000000)
        outValue[topic[i][j]] = 1
        for tt in temp:
            outValue[tt[0]] = max(outValue[tt[0]],tt[1])
    vocabcnt = 0
    vocabrele = 0
    valueDis = []
    fd = open(format("../txt/wordSimilarity%d.txt" % i),"w")
    for tt in vocab:
        vocabcnt += vocab[tt].count
        vocabrele += vocab[tt].count*outValue[tt]
        valueDis.append(outValue[tt])
        fd.write(tt)
        fd.write(" ")
        fd.write(str(outValue[tt]))
        fd.write("\n")
    fd.close()
    print vocabrele/vocabcnt
    print np.mean(valueDis)
    print np.std(valueDis)
    print "*******************"


