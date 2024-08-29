# Exploratory Data Analysis

## Summary Statistics

| Label    | Characteristic |      Mean |       Min |        Max |       Std |
|----------|----------------|-----------|-----------|------------|-----------|
| normal   | ax             | -0.108966 | -1.993896 |  1.999939  |  0.513236 |
| normal   | ay             |  0.267385 | -1.990479 |  1.999939  |  0.665310 |
| normal   | az             | -0.369705 | -1.997803 |  1.999939  |  0.665749 |
| normal   | gx             | -5.354914 | -250.083969 | 250.129776 | 110.931369 |
| normal   | gy             | -0.097030 | -249.938934 | 250.129776 |  88.021507 |
| normal   | gz             |  5.721359 | -250.083969 | 250.129776 |  96.627993 |
| anomalie | ax             | -0.068636 | -1.998047 |  1.999939  |  0.697703 |
| anomalie | ay             | -0.038593 | -1.999756 |  1.999939  |  0.815418 |
| anomalie | az             | -0.263810 | -1.996582 |  1.999939  |  0.790793 |
| anomalie | gx             |  4.411096 | -250.068695 | 250.129776 | 108.776759 |
| anomalie | gy             |  1.892581 | -250.083969 | 250.129776 | 102.992537 |
| anomalie | gz             | -3.058389 | -250.076340 | 250.129776 | 101.491491 |

### Mean Values

#### For Linear Acceleration (ax, ay, az):

- **ax**: The mean value for both "normal" and "anomalie" classes is slightly negative, with the "normal" class having a more negative mean (-0.109) compared to the "anomalie" class (-0.069).
- **ay**: The "normal" class has a positive mean (0.267), while the "anomalie" class has a negative mean (-0.039), indicating slight different average directions of acceleration in the y-axis. Anomaly having more downward accelaration.
- **az**: Both classes have a negative mean, but the "normal" class (-0.370) is more negative compared to the "anomalie" class (-0.264).

#### For Angular Velocity (gx, gy, gz):

- **gx**: The "normal" class has a negative mean (-5.355), while the "anomalie" class has a positive mean (4.411). This difference implies that the dice tends to roll in one direction more frequently in the "normal" class compared to the "anomalie" class.
- **gy**: The "normal" class mean is close to zero (-0.097), indicating a relatively balanced distribution of pitching motion (tilting forward/backward) around the y-axis.  the "anomalie" class mean is positive (1.893), suggesting a tendency for forward pitching motion.
- **gz**: The "normal" class has a positive mean (5.721), whereas the "anomalie" class has a negative mean (-3.058). This difference implies that the dice tends to roll in one direction more frequently in the "normal" class compared to the "anomalie" class.

### Standard Deviation (Std)

- Both classes exhibit substantial variability in their readings, as indicated by the standard deviation values.
- Angular velocities (gx, gy, gz) generally show higher variability compared to linear accelerations (ax, ay, az).


## Visualizations

### Distribution of ax by Label
![Distribution of ax by Label](analysis/ax.png)

### Distribution of ay by Label
![Distribution of ay by Label](analysis/ay.png)

### Distribution of az by Label
![Distribution of ay by Label](analysis/az.png)

### Distribution of gx by Label
![Distribution of ay by Label](analysis/gx.png)

### Distribution of gy by Label
![Distribution of ay by Label](analysis/gy.png)

### Distribution of gz by Label
![Distribution of ay by Label](analysis/gz.png)


### Correlations
### Correlation Matrix for Normal Class
![Correlation Matrix for Normal Class](analysis/correlation%20normal.png)

### Correlation Matrix for Anomalie Class
![Correlation Matrix for Anomalie Class](analysis/correlation_anomaly.png)

## Correlation Analysis

### Normal Class

- **ax** has a weak negative correlation with **ay** (-0.139) and a weak positive correlation with **az** (0.186).
- **gx** has a notable negative correlation with **gz** (-0.240).
- The correlations between other characteristics are relatively weak.

### Anomalie Class

- **ax** has weak positive correlations with both **ay** (0.050) and **az** (0.111).
- **gx** and **gz** have a moderate negative correlation (-0.108), similar to the "normal" class but slightly weaker.
- **gy** and **gz** have a positive correlation (0.112), which is slightly higher than in the "normal" class.


- There are some consistent correlations within each class, but overall, the correlations are relatively weak, suggesting that no single characteristic is strongly dependent on another.

## Observation

### Distinctive Mean Values

- There are clear differences in the mean values of some characteristics between the two classes, notably in **ay**, **gx**, and **gz**. These differences could be significant in distinguishing between normal and anomalous rolls.

### Variance and Distribution

- The standard deviations are relatively high for all characteristics, indicating significant variability in the data, especially for the angular velocities.

### Potential Features for Classification

- The differences in the mean values of **ay**, **gx**, and **gz** suggest that these characteristics might be particularly useful for distinguishing between "normal" and "anomalie" classes.




