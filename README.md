# Evaluating Korean Superlatives in Language Models

An undergraduate research project at Seoul National University investigating whether large language models distinguish the interpretations of Korean superlative constructions.

## Overview

- 900 initial NLI items generated from 25 templates
- 840 items retained after linguistic review
- 8 language models evaluated under Korean and English instructions
- 14,400 model responses collected

The evaluation compares item-level accuracy with diagnostic and control pair performance to examine whether models distinguish construction-dependent interpretations.

## Repository Structure

- `korean_superlatives_evaluation.ipynb` — Dataset construction and result analysis
- `benchmark.py` — Linguistic templates and item generation
- `experiment.py` — LLM API request configurations
- `data/` — Lexical resources, prompts, and collected responses

## Usage

Open the Jupyter notebook and run the cells in order. The collected responses allow offline analysis without additional API calls.

## Reference

Lee (2018). A Pragmatic Account of the Relative Readings in Korean Superlatives.

## Author

Hyeongjun Cho  
Seoul National University  
Linguistics / Humanities Data Science
