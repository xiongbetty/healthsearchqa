import csv
import json
import sys

from random import shuffle

# load answer id mappings
answer_mappings = json.loads(open("answer_mappings.json").read())

rows = []
# load csv file
for csv_file_path in sys.argv[1].split(","):
    csv_file = open(csv_file_path)
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    reviewer_rows = [row for row in csv_reader]
    rows += reviewer_rows

def row2json(row):
    new_json = {}
    new_json["complete"] = row[0]
    new_json["error_free"] = row[1]
    new_json["appropriate"] = row[2]
    new_json["harm_extent"] = row[3]
    new_json["harm_likelihood"] = row[4]
    new_json["no_bias"] = row[5]
    new_json["category"] = row[6]
    new_json["question"] = row[7]
    new_json["response"] = row[8]
    question_info = answer_mappings[row[9]]
    model, qid = question_info.split("-")
    assert model in ["biogpt", "biomedlm", "llama", "mistral"]
    new_json["model"] = model
    new_json["medpalm_qid"] = qid
    new_json["qid"] = row[9]
    assert int(qid[1:]) >= 1
    assert int(qid[1:]) <= 140
    for benchmark in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
        benchmark_score = int(new_json[benchmark].split()[0])
        assert benchmark_score >= 1
        assert benchmark_score <= 5
        new_json[benchmark] = benchmark_score
    return new_json

completed_rows = []
error_count = 0
for idx, row in enumerate(rows):
    try:
        assert len(row) >= 7
        row_json = row2json(row)
        row_json["spreadsheet_idx"] = idx + 1
        completed_rows.append(row_json)
        #print(row_json)
    except:
        print(str(idx + 1) + "\t" + str(row[7].split("\n")[-1]) + "\t" + str(row[9]))
        error_count += 1

print("")
print("Info On Rows")
print(f"Completed: {len(completed_rows)}")
print(f"Errors: {error_count}")

# keep track of qids
qid_counts = {}
medpalm_qid_counts = {}
for row in completed_rows:
    medpalm_qid_counts[row["medpalm_qid"]] = medpalm_qid_counts.get(row["medpalm_qid"], 0) + 1

#for qid in medpalm_qid_counts:
    #if medpalm_qid_counts[qid] < 4:
        #print(qid + "\t" + str(medpalm_qid_counts[qid]))

print("")
# review model scores
model_scores = {
    "biogpt": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
    "biomedlm": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
    "llama": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
    "mistral": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
}
shuffle(completed_rows)
seen_qids = set([])
for row in completed_rows:
    #if not row["qid"] in seen_qids:
        #seen_qids.add(row["qid"])
    #else:
        #continue
    for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
        model_scores[row["model"]][metric] += row[metric]
    model_scores[row["model"]]["total"] += 1

for model in ["biogpt", "biomedlm", "llama", "mistral"]:
    for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
        model_scores[model][metric] = model_scores[model][metric]/model_scores[model]["total"]

for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
    print("---")
    print(metric)
    print("")
    for model in ["biogpt", "biomedlm", "llama", "mistral"]:
        print(model + "\t" + str(model_scores[model][metric])[:4])
