# GPS2curv
Translates GPS coordinates to curvature file for ChassisSim.

This project goal was to perform conversion from gps location data to curvature file needed in ChassisSim. The project was started when data logger on Tampere Formula Student -19 (TFS19) could not provide accurate acceleration data for ChassisSim software. In order to perform laptime simulations a track curvarure file had to be formed with other means. As the logged gps data seemed to be smooth it was investigated if that could be used to form curvature file.

As ChassisSim doesn't provide any documentation about the file syntax or so the project started with trial and error method. The curvature file is ASCII file with two columns using spaces as separators. The second colum was identified as a cumulative travel easily by it's values. The first colum is curvature as 1/r, where r is the radius of current drive path. It is also important to notice that the direction of the turn is defined by using positive and negative radius values.

The trial and error phase was performed with Matlab/Octave but this more polished version is written with Python 3. The first published version (v1.0) contains conversion from gps coordinates to meters and from meters to ChassisSim type curvature file. As I noticed that when gps data points are close to each other in slow curves they sometimes cause error in curvature file so a xy-plot with curvature vectors is also available for debugging the data.

The filtering of gps data is not included in this project but I did pick data point that are at least 0.5m apart and it worked for me. The track in question was karting track driven with formula student car. In general in the plot you don't want to find curvature vectors on top of each other and all of the vectors should be pointing towards the center of the curve in question.

# v0.01
v0.01 can convert the data as intended and also plots the mentioned plot.
Missing features are input commands for "main()". I have visioned that the commands could be (input filename, optional output filename, optional plotgraph)

Also some additional comments in code should be writen for future generations.

# v1.0
The script has now three arguments and usage is following:
```
usage: GPS2curv.py [-h] [-o] [-p] input

positional arguments:
  input           state input file

optional arguments:
  -h, --help      show this help message and exit
  -o , --output   state output filename
  -p, --plot      plots the track and curvature vectors in it
```
The code it self is ready and will not be changed if there is not any problems during further testing with ChassisSim. Altought I am not developping the script actively I am open to have any comments or questions about it.

# v1.1
Some error messages and handling was added to help debugging if something goes wrong.
Additionally new argument was added to allow user to specify the delimiter of the input file. Usage as follows:
```
usage: GPS2curv.py [-h] [-d] [-o] [-p] input

positional arguments:
  input              state input file

optional arguments:
  -h, --help         show this help message and exit
  -d , --delimiter   specify the delimiter used in the input file
  -o , --output      state output filename
  -p, --plot         plots the track and curvature vectors in it
```

# v1.2
--meters argument added to allow users to input track files already converted to meters. By default program assumes that the file is in gps coordinates. Usage as follows:
```
usage: GPS2curv [-h] [-m] [-d] [-o] [-p] input

positional arguments:
  input              state input file

optional arguments:
  -h, --help         show this help message and exit
  -m, --meters       use if the input file is already in meters
  -d , --delimiter   specify the delimiter used in the input file
  -o , --output      state output filename
  -p, --plot         plots the track and curvature vectors in it
```

# v1.3
Although I mentioned that the data filtering wouldn't be part of this project I still included it as there has not been any problems so far. The calculation is simple as it calculates the norm of vector specified with two points. If the norm is shorter than the specified minimum the script will move to next coordinate as long as the minimum length is satisfied. Usage as follows:
```
usage: GPS2curv [-h] [-m] [-d] [-f] [-o] [-p] input

positional arguments:
  input              state input file

optional arguments:
  -h, --help         show this help message and exit
  -m, --meters       use if the input file is already in meters
  -d , --delimiter   specify the delimiter used in the input file
  -f , --filter      specify minimum distance between two points in meters
  -o , --output      state output filename
  -p, --plot         plots the track and curvature vectors in it

```