#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np

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

def spider_plotting(data):
    metrics = ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]
    models = ["biogpt", "biomedlm", "llama", "mistral"]
    scores = np.array([[data[model][metric] for metric in metrics] for model in models])
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    scores = np.concatenate((scores, scores[:,[0]]), axis=1)
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    for i, (model, score) in enumerate(zip(models, scores)):
        ax.plot(angles, score, linewidth=2, linestyle="solid", label=model)
    ax.set_ylim(2.5, 5)
    ax.set_yticks(np.arange(2, 5.5, 0.5))
    ax.set_yticklabels(np.arange(2, 5.5, 0.5))
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)

    plt.legend(loc="lower center")

def main():
    reviewer_files = get_reviewer_csv_files(folder_path)
    completed_rows = load_data(reviewer_files)
    model_scores = get_model_scores(completed_rows)
    print(model_scores)

    for metric in ["complete", "error_free", "appropriate", "harm_extent", "harm_likelihood", "no_bias"]:
        print("---")
        print(metric)
        print("")
        for model in ["biogpt", "biomedlm", "llama", "mistral"]:
            print(model + "\t" + str(model_scores[model][metric])[:4])

    # plotting
    spider_plotting(model_scores)
    plt.title("Model Comparison")
    plt.savefig("spider_chart.png")

if __name__ == "__main__":
    benchmark = sys.argv[1]
    scores_scheme = sys.argv[2]
    folder_path = sys.argv[3]
    
    main()