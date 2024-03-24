import csv 
import json
import os

def get_reviewer_csv_files(folder_path):
    csv_files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.endswith(".csv"):
            csv_files.append({"reviewer": file, "file_path": file_path})
    return csv_files

def row2json(reviewer, row):
    answer_mappings = json.loads(open("answer_mappings.json").read())

    new_json = {}
    new_json["reviewer"] = reviewer
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
    new_json["qid"] = qid
    new_json["example_id"] = row[9]
    assert int(qid[1:]) >= 1
    assert int(qid[1:]) <= 140
    for benchmark in [
        "complete",
        "error_free",
        "appropriate",
        "harm_extent",
        "harm_likelihood",
        "no_bias",
    ]:
        benchmark_score = int(new_json[benchmark].split()[0])
        assert benchmark_score >= 1
        assert benchmark_score <= 5
        new_json[benchmark] = benchmark_score
    return new_json

def load_data(reviewer_files):
    # load rows
    rows = []
    for reviewer_file_info in reviewer_files:
        csv_file = open(reviewer_file_info["file_path"])
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        reviewer_rows = [(reviewer_file_info["reviewer"], row) for row in csv_reader]
        rows += reviewer_rows

    # load json
    row_errors = 0
    review_jsons = []
    for idx, row in enumerate(rows):
        try:
            assert len(row[1]) >= 7
            row_json = row2json(row[0], row[1])
            row_json["spreadsheet_idx"] = idx + 1
            review_jsons.append(row_json)
        except:
            row_errors += 1
    
    return review_jsons