# SITTF_GRN

A Scale-Invariant Task Transformation Framework for Gene Regulatory Network Inference from Time-Series Data

## Workflow Overview

The implementation consists of two experimental workflows: **Toy Dataset** and ***E. coli* Dataset**. Each workflow follows three main steps: **Data Generation**, **Data Preparation**, and **Model Training and Evaluation**.

---

## 1. Toy Dataset

The toy dataset is generated according to the experimental settings described in the Table S2 of the Supplementary Materials. These settings include the predefined network sizes, number of networks, number of profiles per structure, and number of time steps.

### 1.1 Data Generation

The ground-truth gene regulatory networks and their corresponding time-series gene expression data are generated using `gene_network.py`.

The generated datasets follow the predefined network structures and experimental settings described in the Supplementary Materials.

### 1.2 Data Preparation

The generated expression trajectories are processed using `gene_toydataset_ann.py`.

This step transforms the raw time-series expression data into the unified feature representation required for supervised learning and subsequently prepares the data for training, validation, and testing.

### 1.3 Model Training and Evaluation

Model training and performance evaluation are conducted using `gene_models_one_run`.

This module trains the selected machine learning models using the prepared datasets and reports the corresponding evaluation metrics.

---

## 2. *E. coli* Dataset

The *E. coli* dataset is generated using **GeneNetWeaver (GNW)**, following the experimental settings described in the Table S3 of the Supplementary Materials.

### 2.1 Data Generation

The gene regulatory networks and corresponding time-series expression data are generated using **GeneNetWeaver**.

The following parameters are used for dataset generation:

| Parameter                                   | Value                                           |
| ------------------------------------------- | ----------------------------------------------- |
| Number of time series                       | 10                                              |
| Duration of each time series                | 1000                                            |
| Number of measured points per time series   | 21                                              |
| Coefficient of noise term                   | 0                                               |
| Noise added after the simulation            | Model of noise in microarrays (used for DREAM4) |
| Normalize after adding noise (as in DREAM4) | Yes                                             |

These settings are applied consistently to generate the *E. coli* time-series datasets used in the experiments.

### 2.2 Data Preparation

After the dataset generation step, `data_converter.py` is used to read the generated data and prepare it for model training.

Due to computational and memory limitations of the available hardware, the dataset provided in this repository is divided into multiple smaller files. The `data_converter.py` script processes these files and converts the data into the format required for model training.

If sufficient computational resources and memory are available, the generated dataset can alternatively be stored and processed as a single file. In this case, the same data preparation procedure can be applied without splitting the dataset into multiple files.

### 2.3 Model Training and Evaluation

Model training and performance evaluation are conducted using `gene_models_one_run`.

This module trains the selected machine learning models on the prepared *E. coli* datasets and reports the corresponding evaluation metrics using the function `get_report`.
