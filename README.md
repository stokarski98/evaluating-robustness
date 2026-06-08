# Vulnerability of AI-based malware detection methods for Android using manifest files
This repository contains the replication package for the article "Vulnerability of AI-based malware detection methods for Android using manifest files".
The repository contains codes, data, and artifacts that make it possible to reproduce the study.

The model used for the analysis was made available through DrobBox due to its large size. 

## Data
The data file is too large to upload to the repository, so we provide the link:
www.dropbox.com/scl/fi/kka7gawai4oa2tiv74cqi/data.zip?rlkey=5bbcsqxfhx269zf5qnnkc4ia7&st=gljk8gq8&dl=0

- master-list - file containing list of applications SHA256 and Labels (1 - malware, 0 - bening);
- results.json - statistic from our implementation of BERTroid evaluated on test dataset;
- malbert-model.keras - saved MalBERT model;
- manifests - folder containing the manifest files of the applications collected from the AndroZOO database;
- BERTroid-published-datasets - folder containing datasets provided by BERTroid authors;

### Data structure
All results and datasets are included in the data.zip file. 
The data.zip file has the following structure:

- /results - folder containing results.json
- /models - folder containing malbert-model.keras

## Codes
The codes used for analysis can be found in the following files:

- bertroid-analysis.ipynb - jupyter notebook containing BERTroid analysis;
- malbert-analysis.ipynb - jupyter notebook containing MalBERT analysis;
- visualize.py - python file containing the VisualizeXML function used to visualize LIME results;
- obfuscate.py - python file contains the obfuscate_xml implementation. This function is used to randomly obfuscate the Android Manifest.
- models.py - python file containing an implementation of MalBERT;
