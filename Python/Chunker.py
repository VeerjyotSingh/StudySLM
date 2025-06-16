import os
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from tqdm import tqdm
import nltk
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from collections import defaultdict
import json


textDir = "/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text"
textFiles = [f for f in os.listdir(textDir) if f.endswith(".txt")]

print("loading sentence encoder")
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
print("✅ Loaded the Sentence Encoder model")

nltk.download('punkt')
nltk.download('punkt_tab')
print("✅ nltk punkt model donwloaded")



def removeLineBreak(text):
    return text.replace('\n', ' ').replace('\r', ' ')
    

def splitIntoBlocks(text, block_size=2):
    sentences = nltk.sent_tokenize(text)
    blocks = [" ".join(sentences[i:i+block_size]) for i in range(0, len(sentences), block_size)]
    return blocks

def embedBlocks(blocks):
    batchSize = 64
    embeddings = []
    for i in range(0, len(blocks), batchSize):
        batch = blocks[i:i+batchSize]
        vectors = embed(batch).numpy()
        embeddings.append(vectors)
    return np.vstack(embeddings)

def clusterBlocks(embeddings, num_clusters=20):
    clustering = AgglomerativeClustering(n_clusters=num_clusters)
    labels = clustering.fit_predict(embeddings)
    return labels

def groupByCluster(blocks, labels):
    clustered = defaultdict(list)
    for block, label in zip(blocks, labels):
        clustered[label].append(block)
    return [" ".join(group) for group in clustered.values()]


if __name__ == "__main__":
    data = []
    for filename in tqdm(textFiles, desc="Processing NCERT Text files"):
        if filename.endswith(".txt"):
            file = open(textDir+"/"+filename, "r")
            text = file.read()
            text = removeLineBreak(text)

            blocks = splitIntoBlocks(text)
            embeddings = embedBlocks(blocks)
            labels = clusterBlocks(embeddings)
            clustered_texts = groupByCluster(blocks, labels)
            for text in clustered_texts:
                data.append({"vector":[],"text":text})

    with open("chunks.jsonl", "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
