"""
From: https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/agglomerative.py
Copyright Notice: Copyright 2019 Nils Reimers
For the Apache License: see APACHE_LICENSE
For the NOTICE file with attributions see: NOTICE.txt in the root directory of this repo

This is a simple application for sentence embeddings: clustering
Sentences are mapped to sentence embeddings and then agglomerative clustering with a threshold is applied.
Modifications:
* Put AMC/AIME problems into the corpus array
* Use a content_id map so we can print the problem name (e.g. 2020 AIME I problem 1) in the clusters instead of the full
problem text
* Output data using json

THIS FILE IS LICENSED UNDER AGPLv3

Copyright (C) 2023 bkf2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import json
import re

embedder = SentenceTransformer('all-MiniLM-L6-v2')

desired_distance_threshold = float(input("Enter the desired distance threshold: "))

# Corpus with sentences
corpus = []
content_id = {}

tests = ["AMC_8", "AMC_10", "AMC_12", "AIME"]
test_types = {}
test_types["AMC_8"] = [""]
test_types["AMC_10"] = ["A", "B"]
test_types["AMC_12"] = ["A", "B"]
test_types["AIME"] = ["I", "II"]

for test in tests:
    for year in range(2010, 2024):
        if(year == 2023 and (test == "AMC_10" or test == "AMC_12")):
            continue
        if(year == 2021 and (test == "AMC_8")):
            continue
        ending = 26
        if(test == "AIME"):
            ending = 16
        for test_type in test_types[test]:
            for num in range(1, ending):
                f = open("problems/" + test + "/" + str(year) + "/" + test_type + "/" + str(num) + ".txt")
                problem_text = f.read()
                f.close()
                if problem_text in content_id:
                    content_id[problem_text].append([test, year, test_type, num])
                else:
                    content_id[problem_text] = [[test, year, test_type, num]]
                    corpus.append(problem_text)
print("embedding corpus")
corpus_embeddings = embedder.encode(corpus)

# Normalize the embeddings to unit length
print("normalizing the embeddings")
corpus_embeddings = corpus_embeddings /  np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)

# Perform kmean clustering
print("performing kmean clustering")
clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=desired_distance_threshold) #, affinity='cosine', linkage='average', distance_threshold=0.4)
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_

clustered_problems = {}
for problem_id, cluster_id in enumerate(cluster_assignment):
    cluster_id = int(cluster_id)
    if cluster_id not in clustered_problems:
        clustered_problems[cluster_id] = []
    curr_problem_info = {}
    for problem_value in content_id[corpus[problem_id]]:
        test, year, test_type, num = problem_value
        if "problem_name" in curr_problem_info:
            curr_problem_info["problem_name"] += " / "
            if test == "AIME":
                curr_problem_info["problem_name"] += str(year) + " " + test + " " + test_type + " Problem " + str(num)
            else:
                curr_problem_info["problem_name"] += str(year) + " " + test + test_type + " Problem " + str(num)
        else:
            if test == "AIME":
                curr_problem_info["problem_name"] = str(year) + " " + test + " " + test_type + " Problem " + str(num)
                curr_problem_info["problem_link"] = "https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_" + test + "_" + test_type + "_Problems#Problem_" + str(num)
            else:
                curr_problem_info["problem_name"] = str(year) + " " + test + test_type + " Problem " + str(num)
                curr_problem_info["problem_link"] = "https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_" + test + test_type + "_Problems#Problem_" + str(num)
    curr_problem_info["problem_name"] = re.sub("_", " ", curr_problem_info["problem_name"])
    clustered_problems[cluster_id].append(curr_problem_info)

try:
    open("results" + str(desired_distance_threshold) + ".json", 'x')
except:
    pass

with open("results" + str(desired_distance_threshold) + ".json", 'w') as f:
    f.write(json.dumps(clustered_problems, indent=4))