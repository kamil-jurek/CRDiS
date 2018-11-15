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
The first parameter is `RulesGenerator` object, in case of just detecting changes that 
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
Result of running change detection can be found in the picture below. 
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
Discovered change points contain information about the moment in time when changed
occurred, what is the previous value, how long it lasted and what is the value after
the change. 

And so, for example `attr_1 at: 1500 4.0{694} -> 3.0{110}`
means that in sequence with attribute *attr_1* at moment *1500*
changed value from *4.0* that lasted for *694* units of time to value *3.0* and 
had that value for next *110* units of time.

#### Change Detectors
Following change detection algorithms are implemented:
* Geometric Moving Average - `GeometricMovingAverageDetector`
* CUSUM algorithm - `CusumDetector`
* Page-Hinkley test - `PageHinkleyDetector`
* Z-Score algorithm - `ZScoreDetector`
* ADWIN(ADaptive WINdowing) - `AdwinDetector`


## Mining rules in sequences
Basing on the detected change points rules can be generated generated.
To do that `RuleGenerator` object should me passed to the `OnlineSimulator`.
In the example below `AllRulesGenerator` is used that generates all possible rules.
`target_seq_index` is an index of target sequence - stream of values of attribute 
that we want to observe – attribute that will be placed on the right-hand-side of 
the discovered rule. `window_size` is size od the window in which rules are being generated.
If it is set to *0* the previous change point in target sequence is used as the begin of the
window. `round_to` describes frequency with which rule components are generated.
```python
rules_detector = AllRulesGenerator(target_seq_index=3,
                                   window_size=0,
                                   round_to=100)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            sequences,
                            seq_names
                            )
simulator.run(plot=True, detect_rules=True, predict_seq=False)

```
Discovered rules can be extracted from `OnlineSimulator` using `get_rules_set()` method.
Rules with all theirs statistics (support, confidence, score) can be printed using
`print_rules()` method. Minimal rule support can be passed as parameter.
`print_best_rules` allows to print rules with highest score for each attribute.
```
discovered_rules = simulator.get_rules_sets()
print_rules(discovered_rules, 1)
print_best_rules(discovered_rules)
```
The result of printing best rules can be found below.
```
[attr_1(2.0){400; 81%}, attr_1(3.0){400; 79%}, attr_1(4.0){200; 79%}] ==> attr_4(6.0){500; 81%}
	# rule_support:	5
	# lhs_support:	5
	# confidence:	1.0
	# rule_score:	8750.0
	# occurences:	[1510, 3108, 5020, 7107, 8613]
-----------------------------------------------------------------------------------------------------------
[attr_2(4.0){700; 90%}, attr_2(5.0){200; 89%}, attr_2(1.0){100; 89%}] ==> attr_4(6.0){500; 81%}
	# rule_support:	5
	# lhs_support:	5
	# confidence:	1.0
	# rule_score:	8750.0
	# occurences:	[1510, 3108, 5020, 7107, 8613]
-----------------------------------------------------------------------------------------------------------
[attr_3(1.0){200; 94%}, attr_3(4.0){100; 94%}] ==> attr_4(6.0){500; 81%}
	# rule_support:	5
	# lhs_support:	5
	# confidence:	1.0
	# rule_score:	5250.0
	# occurences:	[1510, 3108, 5020, 7107, 8613]
-----------------------------------------------------------------------------------------------------------
[attr_4(1.0){1000; 0%}] ==> attr_4(6.0){500; 81%}
	# rule_support:	5
	# lhs_support:	5
	# confidence:	1.0
	# rule_score:	8750.0
	# occurences:	[1510, 3108, 5020, 7107, 8613]
```
#### Rules Generators
Following rules generators algorithms are implemented:
* `SimpleRulesGenerator` - allows to generate rules in simple format that contains
information only about changes in attribute values, and can be used, for example,
to understand the reason for changes in the target sequence (e.g.
attr1(2 → 3) ⇒ attr1(3 → 4)).
* `AllRulesGenerator` - generates all possible rules, sorted according to score.
* `ClosedRulesGenerator` - generates only the most specific rule, i.e.
rule that does not subsume any other rules.
* `DiscretizedDatasetGenerator` - allows to generate discretized data set for classical algorithms (Apriori, PrfixSpan, ...)

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
