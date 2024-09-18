# UN-General-Debate-Analysis-SDGs
This project analyzes the UN General Debate Corpus from 1970 to 2023. It includes exploratory data analysis (EDA), predictive modeling, and data visualizations focusing on uncovering insights from political speeches and their connection to global challenges.

<table align="center" name="fig3">
    <tr align="center">
                    <td><img src="./assets/images/un.jpg" alt="Snellius"></td>
            </tr>
            <tr align="left">
                <td colspan="2"><b>Figure 1.</b> United Nations General Debate Corpus 1946-2023 | <a href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/0TJX8Y">Dataset </a></td>
    </tr>
</table>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/danilotpnta/UN-General-Debate-Analysis-SDGs/blob/main/notebook.ipynb)

## Setup Instructions

### 1. Clone the repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/danilotpnta/UN-General-Debate-Analysis-SDGs.git
cd UN-General-Debate-Analysis-SDGs
```

### 2. Create the Conda environment

Create the Conda environment using the provided `environment.yml` file. This will install all the necessary dependencies, including Python 3.9, JupyterLab, and various data analysis and visualization libraries.

```bash
conda env create -f environment.yml
```

### 3. Activate the environment

Once the environment is created, activate it with the following command:

```bash
conda activate debates_analysis
```

### 4. Download the data 

The project includes a script to download files from the Dataverse repository. You can run this script to download the raw data needed for the analysis. The data will be saved in the `data/raw/` directory.

```bash
python utils/dataverse_downloader.py
```

### 5. Start JupyterLab

To run the notebook, launch JupyterLab or Jupyter Notebook:

```bash
jupyter lab
```

This will open a new tab in your browser. You can navigate to the `notebook.ipynb` file and start running the cells.

### 6. Running the Notebook

Open the `notebook.ipynb` file in Jupyter and run the cells. The notebook will guide you through the exploratory and predictive analysis of the UN General Debate dataset.
