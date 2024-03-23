import json

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