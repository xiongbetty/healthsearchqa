#!/usr/bin/env python3

import sys

from utils import get_reviewer_csv_files, load_data

# functions

def get_model_scores(completed_rows):
    model_scores = {
        "biogpt": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
        "biomedlm": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
        "llama": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
        "mistral": { "complete": 0, "error_free": 0, "appropriate": 0, "harm_extent": 0, "harm_likelihood": 0, "no_bias": 0, "total": 0},
    }
    for row in completed_rows:
        for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
            model_scores[row["model"]][metric] += row[metric]
        model_scores[row["model"]]["total"] += 1

    for model in ["biogpt", "biomedlm", "llama", "mistral"]:
        for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
            if model_scores[model]["total"] > 0:
                model_scores[model][metric] = model_scores[model][metric]/model_scores[model]["total"]
            else:
                model_scores[model][metric] = 0
    return model_scores

def main():
    reviewer_files = get_reviewer_csv_files(folder_path)
    completed_rows = load_data(reviewer_files)
    model_scores = get_model_scores(completed_rows)

    for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
        print("---")
        print(metric)
        print("")
        for model in ["biogpt", "biomedlm", "llama", "mistral"]:
            print(model + "\t" + str(model_scores[model][metric])[:4])

if __name__ == "__main__":
    benchmark = sys.argv[1]
    scores_scheme = sys.argv[2]
    folder_path = sys.argv[3]
    
    main()