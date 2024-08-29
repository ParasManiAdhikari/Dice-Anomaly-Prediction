## Exploratory Data Analysis

## Summary Statistics

| Label    | Characteristic |      Mean |       Min |        Max |       Std |
|----------|----------------|-----------|-----------|------------|-----------|
| normal   | ax             | -0.278    | -1.9968   |  1.9999    |  0.5791   |
| normal   | ay             |  0.183    | -1.9844   |  1.9999    |  0.6410   |
| normal   | az             | -0.014    | -1.9844   |  1.9999    |  0.6180   |
| normal   | gx             | -0.327    | -249.4886 | 250.1298   | 100.2022  |
| normal   | gy             | -8.877    | -248.9008 | 250.1298   |  94.4326  |
| normal   | gz             |  0.361    | -249.4275 | 250.1298   |  94.5689  |
| anomalie | ax             | -0.102    | -1.9844   |  1.9999    |  0.6470   |
| anomalie | ay             | -0.108    | -1.9844   |  1.9999    |  0.6869   |
| anomalie | az             |  0.249    | -1.9844   |  1.9999    |  0.5682   |
| anomalie | gx             | 15.101    | -249.8397 | 250.1298   |  92.3944  |
| anomalie | gy             | -0.941    | -248.1832 | 250.1298   |  92.8154  |
| anomalie | gz             |  7.016    | -249.3588 | 250.1298   |  96.5984  |

### Mean Values

#### For Linear Acceleration (ax, ay, az):

- **ax**: The mean value for both "normal" and "anomalie" classes is negative, with the "normal" class having a more negative mean (-0.278) compared to the "anomalie" class (-0.102).
- **ay**: The "normal" class has a positive mean (0.183), while the "anomalie" class has a negative mean (-0.108), indicating a slight difference in average directions of acceleration in the y-axis. Anomaly having more downward acceleration.
- **az**: The "anomalie" class has a positive mean (0.249), while the "normal" class has a slightly negative mean (-0.014).

#### For Angular Velocity (gx, gy, gz):

- **gx**: The "normal" class has a negative mean (-0.327), while the "anomalie" class has a positive mean (15.101). This difference implies that the dice tends to roll in one direction more frequently in the "anomalie" class compared to the "normal" class.
- **gy**: The "normal" class mean is more negative (-8.877) compared to the "anomalie" class mean (-0.941), suggesting a difference in pitching motion (tilting forward/backward) around the y-axis.
- **gz**: The "normal" class has a slightly positive mean (0.361), whereas the "anomalie" class has a higher positive mean (7.016). This difference implies that the dice tends to roll more frequently in one direction in the "anomalie" class compared to the "normal" class.

### Standard Deviation (Std)

- Both classes exhibit substantial variability in their readings, as indicated by the standard deviation values.
- Angular velocities (gx, gy, gz) generally show higher variability compared to linear accelerations (ax, ay, az).

## Visualizations

### Distribution of ax by Label
![Distribution of ax by Label](22_analysis/ax.png)

### Distribution of ay by Label
![Distribution of ay by Label](22_analysis/ay.png)

### Distribution of az by Label
![Distribution of az by Label](22_analysis/az.png)

### Distribution of gx by Label
![Distribution of gx by Label](22_analysis/gx.png)

### Distribution of gy by Label
![Distribution of gy by Label](22_analysis/gy.png)

### Distribution of gz by Label
![Distribution of gz by Label](22_analysis/gz.png)

### Correlations
### Correlation Matrix for Normal Class
![Correlation Matrix for Normal Class](22_analysis/correlation_normal.png)

### Correlation Matrix for Anomalie Class
![Correlation Matrix for Anomalie Class](22_analysis/correlation_anomaly.png)

## Correlation Analysis

### Normal Class

- **ax** has a weak positive correlation with **ay** (0.124) and a weak negative correlation with **az** (-0.024).
- **gx** has a notable negative correlation with **gz** (-0.129).
- The correlations between other characteristics are relatively weak.

### Anomalie Class

- **ax** has a weak positive correlation with **ay** (0.159) and a weak negative correlation with **az** (-0.154).
- **gx** and **gz** have a positive correlation (0.133), which is higher than in the "normal" class.
- **gy** and **gz** have a positive correlation (0.142), which is slightly higher than in the "normal" class.

- There are some consistent correlations within each class, but overall, the correlations are relatively weak, suggesting that no single characteristic is strongly dependent on another.

## Observation

### Distinctive Mean Values

- There are clear differences in the mean values of some characteristics between the two classes, notably in **ay**, **gx**, and **gz**. These differences could be significant in distinguishing between normal and anomalous rolls.

### Variance and Distribution

- The standard deviations are relatively high for all characteristics, indicating significant variability in the data, especially for the angular velocities.

### Potential Features for Classification

- The differences in the mean values of **ay**, **gx**, and **gz** suggest that these characteristics might be particularly useful for distinguishing between "normal" and "anomalie" classes.