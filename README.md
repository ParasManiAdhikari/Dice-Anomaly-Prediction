# Softwaretechnik-Projekt Data Science SoSe 2024 - Brought from Gitlab for Job Application Phase

## Team B

## DOD
The dice prediction algorithm, designed to detect whether a die is rolling normally or anomalously, is fully functional with sufficient testing. Additionally, the documentation on the wiki has been thoroughly updated.

## Sprintverteilung Meeting on 23.05.2024

## Review Meeting on 28.05.2024

### Results of Sprint 5
- Improved Consumer efficiency by replacing one-by-one loading with [Batch loading](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/kafka_consumer.py?ref_type=heads#L33).

#### Task #7: Beladung der Staging Area Done
- Implemented a [method](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/kafka_consumer.py?ref_type=heads#L46) that checks for data loss during loading. The process was confirmed as loss-free _(verlustfrei)_ and the contents of the data were verified as identical _(inhaltlich gleich)_.

#### Task #21: Trainings/Test Daten filtern nach Stillzustand und Bewegung
- Data was [cleaned](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/21_clean_data.py?ref_type=heads), removing still datapoints to retain only movement datapoints. Approximately 50k data points were cleaned to around 35k.
- The cleaned database was saved as `cleaned_database.db`.

#### Task #14: Explorative Analyse hinsichtlich der Zielvariablen
- The database, `cleaned_database.db`, was [analyzed](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/other/14_explorative_analyse.py).
- Calculated mean and standard deviation, separating by normal and anomaly.
- Created distribution plots for each characteristic.
- Generated correlation matrices for each label.
- The complete analysis was documented in [analysis.md](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/14_analysis/14_analysis.md).

## Sprintverteilung Meeting on 10.06.2024

## Review Meeting on 14.06.2024

### Results of Sprint 6
#### Task #21: Trainings/Test Daten filtern nach Stillzustand und Bewegung
- The model was improved by:
  1. Adding a label "Stillzustand" as 1 or 0.
  2. Plotting _Stillzustand_ data points against _Bewegung_ data points.
  3. Checking if the change is too quick or corresponds to the number of throws (40).
  4. Ensuring the same number of rolls are shown in the plot.
  5. Adjusting the interval if the plot is incorrect.

#### Task #22: Explorative Analyse mit neuen Daten
- The database, `Training_Zustand.db`, was [analyzed](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/22_analysis/22_explorative_analyse_neuen_data.py).
  - Calculated mean and standard deviation, separating by normal and anomaly.
  - Created distribution plots for each characteristic.
  - Generated correlation matrices for each label.
  - The complete analysis was documented in [22_analysis.md](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/22_analysis/22_analysis.md).

#### Task #17: Initiales Vorhersagemodell trainieren und evaluieren
- [17_Sequential (1).ipynb](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/17_Sequential%20(1).ipynb?ref_type=heads) was created to train and test the data with a Sequential model.
  - The accuracy achieved was 0.67.
  - The initial testing results were positive.

## Sprintverteilung Meeting on 13.06.2024

## Review Meeting on 23.06.2024

### Results of Sprint 7
#### Task #24: Weitere Modelle Trainieren & Evaluieren
- In addition to the [Sequential Model](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/17_Sequential%20(1).ipynb?ref_type=heads) from the previous Sprint, other models were [tested](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/tree/main/23_other_models?ref_type=heads):
  - [Resnet](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/23_other_models/24_ResNet.ipynb?ref_type=heads)
  - [KNeighborsTimeSeriesClassifier](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/23_other_models/24_Kneigbhours.ipynb?ref_type=heads)
  - [Kneighbours, RidgeClassifierCV](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/23_other_models/24_TimeSeriesClassifiers.ipynb?ref_type=heads)
  - [Random Forest](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/24_Randomforest.ipynb?ref_type=heads) with 92% accuracy and faster runtime was chosen as the model for the MVP.

#### Task #23: MVP Ausführen
- A [webpage](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/templates/index.html?ref_type=heads) linked to the [Consumer](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blame/main/MVP.py?ref_type=heads#L101) was created as the platform for the MVP.
- When the "Predict" button is pressed, the prediction for the next 200 data points is [started](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/mvp_clean.py?ref_type=heads#L102).
- [Still data is ignored](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/mvp_clean.py?ref_type=heads#L45).
- The model is used in the MVP to [predict](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blame/main/mvp_clean.py?ref_type=heads#L73) a list of 200 data points.
- The [majority prediction](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blame/main/mvp_clean.py?ref_type=heads#L83) is [displayed](https://git.mylab.th-luebeck.de/zimmermann-projects/swtp/sose24/swtp_ds_24_b/-/blob/main/templates/index.html?ref_type=heads#L89) on the webpage.
- The MVP was tested about 20 times before presentation.
