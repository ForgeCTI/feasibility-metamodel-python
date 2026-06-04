# Case studies

This folder contains concrete case studies developed with the CTI Feasibility Metamodel.

Unlike the `examples/` folder, which contains small didactic demonstrations, the case studies are larger scenario-specific models. Each case study may include structured scenario files, Python implementations, diagrams, supporting data, generated outputs, and modelling notes.

| Case study | Description | Status |
|---|---|---|
| `01_case_study` | First CTI feasibility scenario. | Draft |
| `02_case_study` | Second CTI feasibility scenario. | Draft |
| `03_case_study` | Third CTI feasibility scenario. | Draft |
| `04_case_study` | Fourth CTI feasibility scenario. | Draft |
| `05_case_study` | Fifth CTI feasibility scenario. | Draft |

## Suggested workflow

For each case study:

1. Describe the scenario in `README.md`.
2. Encode the scenario in `scenario.yaml`.
3. Implement the scenario using package classes in `implementation.py`.
4. Store raw supporting files in `data/`.
5. Store draw.io or exported diagrams in `diagrams/`.
6. Store generated validation reports, graph exports, or other artifacts in `output/`.
7. Track assumptions and modelling decisions in `notes/`.

## Folder convention

Each case study follows the same structure:

```text
case_studies/<case_study>/
├── README.md
├── scenario.yaml
├── implementation.py
├── data/
├── diagrams/
├── output/
└── notes/
```
