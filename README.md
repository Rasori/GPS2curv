# GPS2curv
Translates GPS coordinates to curvature file for ChassisSim.

This project goal was to perform conversion from gps location data to curvature file needed in ChassisSim. The project was started when data logger on Tampere Formula Student -19 (TFS19) could not provide accurate acceleration data for ChassisSim software. In order to perform laptime simulations a track curvarure file had to be formed with other means. As the logged gps data seemed to be smooth it was investigated if that could be used to form curvature file.

As ChassisSim doesn't provide any documentation about the file syntax or so the project started with trial and error method. The curvature file is ASCI file with two colums using spaces as separators. The second colum was identified as a cumulative travel easily by it's values. The first colum is curvature as 1/r, where r is the radius of current drive path. It is also important to notice that the direction of the turn is defined by using positive and negative radius values.

The trial and error phase was performed with Matlab/Octave but this more polished version will be written with Python 3. The first puplished version (v1.0) will contain conversion from gps coordinates to meters and from meters to ChassisSim type curvature file. As I noticed that when gps datapoints are close to each other in slow curves they sometimes cause error in curvature file so a xy-plot with curvature vectors will also be in cluded for debugging the data.

The filtering of gps data is not included in this project but I did pick datapoint that are at least 0.5m apart and it worked for me. The track in question was carting track driven with formula student car.

# What's next
v0.01 can convert the data as intended and also plots the mentioned plot.
Missing features are input commands for "main()". I have visioned that the commands could be (input filename, optional output filename, optional plotgraph)

Also some additional comments in code should be writen for future generations.
