# Korean Superlatives Evaluation

An evaluation of LLM inference on Korean superlative constructions, based on Lee (2018), *A Pragmatic Account of the Relative Readings in Korean Superlatives*.

## Overview

This notebook reproduces the initial classroom-presentation analysis: 900 items, 450 matched pairs (200 diagnostic and 250 control), eight models, two instruction languages, and 14,400 collected responses. The subsequent refined 840-item analysis in the portfolio is a separate version.

## Reproduce

Install `pandas` and `notebook`, then open `korean_superlatives_evaluation.ipynb` from the repository root and run the cells in order. The saved responses support offline analysis without API keys.

## Files

- `benchmark.py`: Korean sentence templates and item identifiers
- `experiment.py`: API request configuration
- `data/`: lexical resources, scale forms, prompts and saved responses

API requests, if separately invoked, require `OPENAI_API_KEY` or `OPENROUTER_API_KEY` as environment variables.

## Author

Hyeongjun Cho, Seoul National University
