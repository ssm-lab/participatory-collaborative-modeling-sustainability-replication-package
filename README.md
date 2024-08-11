# Replication package

### for the paper _Participatory and Collaborative Modeling of Sustainable Systems: A Systematic Review_.

## About
Sustainability has become a key characteristic of modern systems. Unfortunately, the convoluted nature of sustainability limits its understanding and hinders the design of sustainable systems. Thus, cooperation among a diverse set of stakeholders is paramount to sound sustainability-related decisions. Collaborative modeling has demonstrated benefits in facilitating cooperation between technical experts in engineering problems; but fails to include non-technical stakeholders in the modeling endeavor. In contrast, participatory modeling excels in facilitating high-level modeling among a diverse set of stakeholders, often of non-technical profiles; but fails to generate actionable engineering models. To instigate a convergence between the two disciplines, we systematically survey the field of collaborative and participatory modeling for sustainable systems. By analyzing 24 primary studies (published until June 2024), we identify common challenges, cooperation models, modeling formalisms and tools; and recommend future avenues of research.

## Contents

- `/data` - Data files.
  - `data.xlsx` - Data extraction sheet of the 24 included studies.
  - `QA.xlsx` - Quality scores of the 24 included studies.
- `/scripts` - Analysis scripts for the automated analysis of data.
- `/output` - Results of the analyses as used in the article.

## How to use

### Install requirements
- Install requirements by executing `pip install -r requirements.txt` from the root folder.

### Run analysis
- For publication trends: execute `python .\scripts\publication_trends.py` from the root folder.
- For the quality report: execute `python .\scripts\quality.py` from the root folder.
