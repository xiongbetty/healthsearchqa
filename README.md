### healthsearchqa
Betty Xiong

### Project description
Organizing physician reviews for visualization in spider plots.

### Instructions to run

# Create a local copy:
In a first step, clone this repository by using `git clone https://github.com/xiongbetty/healthsearchqa.git`.

# Install dependencies: create a conda environment
`conda env create -f env.yml`

`conda activate healthsearchqa`

# Test the implementation
To check the implementation of data visualization, run `python review_worksheets.py <benchmark> <scoring_scheme> <folder_path>` which will plot a spider plot and save the output to `spider_chart.png`

To check the implementation, run `python reviewer_report.py <benchmark> <scoring_scheme> <folder_path>` which will output the average scores given by each reviewer

* `<benchmark>` can refer to: `complete`, `error_free`, `appropriate`, `harm_extent`, `harm_likelihood`, `no_bias`
* `<scoring_scheme>` can refer to how you assign a 5-point Likert scale with the default as `"1,2,3,4,5"`, but can be `"1,1,2,3,3"` where you you condense a 5-point scale to 3 points by merging 1,2 and 4,5
* `<folder_path>` can refer to where your data is assigned

An example command line query for data visualization is `python review_worksheets.py complete "1,2,3,4,5" tests`