"""
Part 3: Measuring Performance

Now that you have drawn the dataflow graph in part 2,
this part will explore how performance of real pipelines
can differ from the theoretical model of dataflow graphs.

We will measure the performance of your pipeline
using your ThroughputHelper and LatencyHelper from HW1.

=== Coding part 1: making the input size and partitioning configurable ===

We would like to measure the throughput and latency of your PART1_PIPELINE,
but first, we need to make it configurable in:
(i) the input size
(ii) the level of parallelism.

Currently, your pipeline should have two inputs, load_input() and load_input_bigger().
You will need to change part1 by making the following additions:

- Make load_input and load_input_bigger take arguments that can be None, like this:

    def load_input(N=None, P=None)

    def load_input_bigger(N=None, P=None)

You will also need to do the same thing to q8_a and q8_b:

    def q8_a(N=None, P=None)

    def q8_b(N=None, P=None)

Here, the argument N = None is an optional parameter that, if specified, gives the size of the input
to be considered, and P = None is an optional parameter that, if specifed, gives the level of parallelism
(number of partitions) in the RDD.

You will need to make both functions work with the new signatures.
Be careful to check that the above changes should preserve the existing functionality of part1
(so python3 part1.py should still give the same output as before!)

Don't make any other changes to the function sigatures.

Once this is done, define a *new* version of the PART_1_PIPELINE, below,
that takes as input the parameters N and P.
(This time, you don't have to consider the None case.)
You should not modify the existing PART_1_PIPELINE.

You may either delete the parts of the code that save the output file, or change these to a different output file like part1-answers-temp.txt.
"""
from pyspark.sql import SparkSession
from pyspark.errors import PySparkRuntimeError
import os, sys

try:
    spark = SparkSession.builder.appName("hw2").getOrCreate()
    sc = spark.sparkContext
except PySparkRuntimeError:
    spark = None
    sc = None

if sc is not None:
    part1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "part1.py")
    sc.addPyFile(part1_path)

from part1 import *


def PART_1_PIPELINE_PARAMETRIC(N, P):
    """
    Parametric version of PART_1_PIPELINE.
    N = input size
    P = number of partitions
    """
    
    rdd = load_input(N=N, P=P)

    q1_out = q1()
    q2_out = q2()
    q4_out = q4(rdd)
    q5_out = q5(rdd)
    q6_out = q6(rdd)
    q7_out = q7(rdd)
    q8a_out = q8_a(N=N, P=P)
    q8b_out = q8_b(N=N, P=P)
    q11_out = q11(rdd)
    q14_out = q14(rdd)
    q16a_out = q16_a()
    q16b_out = q16_b()
    q16c_out = q16_c()
    q20_out = q20()

    return {
        "q1": q1_out,
        "q2": q2_out,
        "q4": q4_out,
        "q5": q5_out,
        "q6": q6_out,
        "q7": q7_out,
        "q8a": q8a_out,
        "q8b": q8b_out,
        "q11": q11_out,
        "q14": q14_out,
        "q16a": q16a_out,
        "q16b": q16b_out,
        "q16c": q16c_out,
        "q20": q20_out
    }


"""
=== Coding part 2: measuring the throughput and latency ===

Now we are ready to measure the throughput and latency.

To start, copy the code for ThroughputHelper and LatencyHelper from HW1 into this file.

Then, please measure the performance of PART1_PIPELINE as a whole
using five levels of parallelism:
- parallelism 1
- parallelism 2
- parallelism 4
- parallelism 8
- parallelism 16

For each level of parallelism, you should measure the throughput and latency as the number of input
items increases, using the following input sizes:
- N = 1, 10, 100, 1000, 10_000, 100_000, 1_000_000.

- Note that the larger sizes may take a while to run (for example, up to 30 minutes). You can try with smaller sizes to test your code first.

You can generate any plots you like (for example, a bar chart or an x-y plot on a log scale,)
but store them in the following 10 files,
where the file name corresponds to the level of parallelism:

output/part3-throughput-1.png
output/part3-throughput-2.png
output/part3-throughput-4.png
output/part3-throughput-8.png
output/part3-throughput-16.png
output/part3-latency-1.png
output/part3-latency-2.png
output/part3-latency-4.png
output/part3-latency-8.png
output/part3-latency-16.png

Clarifying notes:

- To control the level of parallelism, use the N, P parameters in your PART_1_PIPELINE_PARAMETRIC above.

- Make sure you sanity check the output to see if it matches what you would expect! The pipeline should run slower
  for larger input sizes N (in general) and for fewer number of partitions P (in general).

- For throughput, the "number of input items" should be 2 * N -- that is, N input items for load_input, and N for load_input_bigger.

- For latency, please measure the performance of the code on the entire input dataset
(rather than a single input row as we did on HW1).
MapReduce is batch processing, so all input rows are processed as a batch
and the latency of any individual input row is the same as the latency of the entire dataset.
That is why we are assuming the latency will just be the running time of the entire dataset.

- Please set `NUM_RUNS` to `1` if you haven't already. Note that this will make the values for low numbers (like `N=1`, `N=10`, and `N=100`) vary quite unpredictably.
"""

# Copy in ThroughputHelper and LatencyHelper
class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)
        # raise NotImplementedError

    def compare_throughput(self):
        # Measure the throughput of all pipelines
        # and store it in a list in self.throughputs.
        # Make sure to use the NUM_RUNS variable.
        # Also, return the resulting list of throughputs,
        # in **number of items per second.**
        self.throughputs = []
        for i in range(len(self.pipelines)):
            total_time = 0
            for _ in range(NUM_RUNS):
                import time
                start_time = time.time()
                self.pipelines[i]()
                end_time = time.time()
                total_time += (end_time - start_time)
            avg_time = total_time / NUM_RUNS
            throughput = self.sizes[i] / avg_time
            self.throughputs.append(throughput)
        return self.throughputs

    def generate_plot(self, filename):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(self.names, self.throughputs, color='skyblue')
        plt.xlabel('Pipeline')
        plt.ylabel('Throughput (items/second)')
        plt.title('Pipeline Throughput Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        # raise NotImplementedError

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)
        # raise NotImplementedError

    def compare_latency(self):
        # Measure the latency of all pipelines
        # and store it in a list in self.latencies.
        # Also, return the resulting list of latencies,
        # in **milliseconds.**
        self.latencies = []
        for i in range(len(self.pipelines)):
            total_time = 0
            for _ in range(NUM_RUNS):
                import time
                start_time = time.time()
                self.pipelines[i]()
                end_time = time.time()
                total_time += (end_time - start_time)
            avg_time = total_time / NUM_RUNS
            latency = avg_time * 1000 
            self.latencies.append(latency)
        # raise NotImplementedError
        return self.latencies

    def generate_plot(self, filename):
        # Generate a plot for latency using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(self.names, self.latencies, color='salmon')
        plt.xlabel('Pipeline')
        plt.ylabel('Latency (milliseconds)')
        plt.title('Pipeline Latency Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        # raise NotImplementedError

# Insert code to generate plots here as needed
os.makedirs('output', exist_ok=True)
NUM_RUNS = 1
input_sizes = [1, 10, 100, 1000, 10_000, 100_000, 1_000_000]
parallelism_levels = [1, 2, 4, 8, 16]

def pipeline_func(N, P):
    def func():
        PART_1_PIPELINE_PARAMETRIC(N, P)
    return func

"""
=== Reflection part ===

Once this is done, write a reflection and save it in
a text file, output/part3-reflection.txt.

I would like you to think about and answer the following questions:

1. What would we expect from the throughput and latency
of the pipeline, given only the dataflow graph?

Use the information we have seen in class. In particular,
how should throughput and latency change when we double the amount of parallelism?

Please ignore pipeline and task parallelism for this question.
The parallelism we care about here is data parallelism.

2. In practice, does the expectation from question 1
match the performance you see on the actual measurements? Why or why not?

State specific numbers! What was the expected throughput and what was the observed?
What was the expected latency and what was the observed?

3. Finally, use your answers to Q1-Q2 to form a conjecture
as to what differences there are (large or small) between
the theoretical model and the actual runtime.
Name some overheads that might be present in the pipeline
that are not accounted for by our theoretical model of
dataflow graphs that could affect performance.

You should list an explicit conjecture in your reflection, like this:

    Conjecture: I conjecture that ....

You may have different conjectures for different parallelism cases.
For example, for the parallelism=4 case vs the parallelism=16 case,
if you believe that different overheads are relevant for these different scenarios.

=== Grading notes ===

- Don't forget to fill out the entrypoint below before submitting your code!
Running python3 part3.py should work and should re-generate all of your plots in output/.

- You should modify the code for `part1.py` directly. Make sure that your `python3 part1.py` still runs and gets the same output as before!

- Your larger cases may take a while to run, but they should not take any
  longer than 30 minutes (half an hour).
  You should be including only up to N=1_000_000 in the list above,
  make sure you aren't running the N=10_000_000 case.

- In the reflection, please write at least a paragraph for each question. (5 sentences each)

- Please include specific numbers in your reflection (particularly for Q2).

=== Entrypoint ===
"""

if __name__ == '__main__':
    print("Complete part 3. Please use the main function below to generate your plots so that they are regenerated whenever the code is run:")

    print("[add code here]")
    for P in parallelism_levels:
        # Throughput measurement
        th = ThroughputHelper()
        for N in input_sizes:
            th.add_pipeline(f'N={N}', 2 * N, pipeline_func(N, P))
        th.compare_throughput()
        th.generate_plot(f'output/part3-throughput-{P}.png')

        # Latency measurement
        lh = LatencyHelper()
        for N in input_sizes:
            lh.add_pipeline(f'N={N}', pipeline_func(N, P))
        lh.compare_latency()
        lh.generate_plot(f'output/part3-latency-{P}.png')