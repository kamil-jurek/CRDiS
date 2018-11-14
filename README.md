# CRDiS Causal Rules Discovery in Data Streams

## Change detection in sequences
The first phase of the proposed approach of finding rules aims at localizing change
points in the sequences of data that can be later used to discover the underlying 
causal structure of data streams.

The input to this phase is the set of *n* input sequences and *n* change detector
objects that implement the specific change detection algorithm. For each sequence
change points can be discovered using different algorithm.
```python
df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
seq_1 = np.array(df['attr_1'])
seq_2 = np.array(df['attr_2'])
seq_4 = np.array(df['attr_4'])
```
In the example below `ZScoreDetector` is being used with `window_size` set to 30:
```python
win_size = 30
detector_1 = ZScoreDetector(window_size = win_size, threshold=3.5)
detector_2 = ZScoreDetector(window_size = win_size, threshold=4.5)
detector_4 = ZScoreDetector(window_size = win_size, threshold=4.5)
```
Later `OnlineSimulator` object is being created. Online Simulator allows to 
simulate streaming data for the purpose of online algorithm experiments.
The first parameter is `RulesDetector` object, in case of just detecting changes that 
parameter is not required. The second parameter is a list of change detector objects.
Third one is a list of sequences and the fourth one is a list of sequences name.
The initialized OnlineSimulator is being started by using `run()` method.
```python
simulator = OnlineSimulator(None,
                            [detector_1, detector_2, detector_4],
                            [seq_1, seq_2, seq_4],
                            ["attr_1", "attr_2", "attr_4"])

simulator.run(plot=True, detect_rules=False)
```
Result of running change detection can be found in the below picture. 
The points of sequence in which changes were detected are marked as red dotted lines. 
![attr_1 result](https://github.com/kamil-jurek/CRDiS/blob/master/plots/readme_plot_attr1_change_detection.png)

```python
detected_change_points = simulator.get_detected_changes()
print_detected_change_points(detected_change_points)

```
The exact output of the change detection mechanism can be got from Online Simulator
using `get_detected_changes()` and printed using `print_detected_change_points()` methods.
For sequence *attr_1* the output is presented below.
```bash
attr_1 at: 420  2.0{407} -> 3.0{409}
attr_1 at: 840  3.0{409} -> 4.0{694}
attr_1 at: 1500 4.0{694} -> 3.0{110}
attr_1 at: 1620 3.0{110} -> 2.0{398}
attr_1 at: 2040 2.0{398} -> 3.0{393}
attr_1 at: 2400 3.0{393} -> 4.0{701}
attr_1 at: 3120 4.0{701} -> 3.0{396}
attr_1 at: 3480 3.0{396} -> 1.0{406}
attr_1 at: 3900 2.0{406} -> 3.0{395}
attr_1 at: 4320 3.0{395} -> 4.0{1026}
attr_1 at: 5340 4.0{1026} -> 2.0{78}
attr_1 at: 5400 4.0{78} -> 2.0{408}
attr_1 at: 5820 2.0{408} -> 3.0{385}
attr_1 at: 6180 3.0{385} -> 4.0{705}
attr_1 at: 6900 4.0{705} -> 3.0{207}
attr_1 at: 7140 3.0{207} -> 2.0{397}
attr_1 at: 7500 2.0{397} -> 4.0{398}
attr_1 at: 7920 3.0{398} -> 4.0{339}
attr_1 at: 8280 4.0{339} -> 1.0{490}
attr_1 at: 8760 4.0{490} -> 1.0{257}

```
 


## Mining rules in sequences

## Prediction using discovered causal rules

## Sequence generator
```
  - python seqgen.py -i configs/config_file -s
  - python plot_sequence.py -i sequences/sequence.csv -s 120000
```

## License

MIT License

Copyright (c) 2018 Kamil Jurek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
