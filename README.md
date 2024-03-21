# Lab 07: Path vector routing simulator

## Overview
In this lab, you’ll write a path vector routing simulator that computes which paths a small set of autonomous systems (ASes) learn based on the relationships between.

### Learning objectives
After completing this lab, you should be able to:
* Compute the advertisements an AS sends to its neighbors
* Compute the path an AS uses to reach a destination

## Getting started
Clone your git repository on a `tigers` server. Your repository contains:
* `simulator.py`: a partially written Python program for simulating path vector routing
* `topologies`: a directory with example network topologies

## Implementing the simulator
The provided code (in `simulator.py`) contains:
* `AutonomousSystem`: a class representing an AS, which keeps track of the AS’s number, prefix, customers, providers, and peers
* `Advertisement`: a class representing a route advertisement, which consists of a prefix and a path (i.e., list) of ASes the advertisement has traversed
* `load_topology`: a function that creates and relates `AutonomousSystem` objects based on topology information provided in a JSON file
* `main`: a main function

Your simulator will propagate advertisements for one prefix at a time; after all advertisements have been propagated for one prefix (and each AS has determined its best path to that prefix), then the simulator will propagate advertisements for the next prefix. 

Your task is to complete the following three functions in the `AutonomousSystem` system class:
* `originate_advertisment` – This function should advertise an AS's own prefix.
* `forward_advertisement` – This function should forward advertisements an AS learns from its neighbors. Refer to the [class notes on AS relationships](https://docs.google.com/document/d/1x4N2hHApi_VbjaNdpJ5Ct5WJSPjptDwCYf1yRL5ZT-s/edit?usp=sharing) for the export polices that conform to valley-free routing. Your `forward_advertisement` function should directly call the `recv_advertisement` function of the AS(es) to which the advertisement is being forwarded to simulate the behavior of sending an advertisement on a network link.
* `recv_advertisement` – This function should process advertisements an AS receives from its neighbors. A shorter path is preferred to a longer path; if two paths have equal length, then the AS may prefer either path. In some cases, advertisements received from neighbors need to be forwarded other neighbors, which should be handled by calling an AS's own `forward_advertisement` function from within the `recv_advertisement` function.

## Testing the simulator
You can use the provided topologies (`linear.json`, `example.json` and `warm-up.json`) to test your simulator. You can run the simulator as follows:
```bash
./simulator.py topologies/TOPOLOGY_FILE
```
replacing `TOPOLOGY_FILE` with the name of one of the JSON files.

For example, your simulator should produce the following output for `linear.json`: 
```
***** Topology *****
AS 1 (11.0.0.0/8): cust=[]; prov=[2]; peer=[]
AS 2 (12.0.0.0/8): cust=[1,3]; prov=[]; peer=[]
AS 3 (13.0.0.0/8): cust=[]; prov=[2]; peer=[]
***** Routes *****
AS 1
        11.0.0.0/8: 
        12.0.0.0/8: 2
        13.0.0.0/8: 2 -> 3
AS 2
        11.0.0.0/8: 1
        12.0.0.0/8: 
        13.0.0.0/8: 3
AS 3
        11.0.0.0/8: 2 -> 1
        12.0.0.0/8: 2
        13.0.0.0/8: 
```

### Topologies
The example topologies are shown below.

#### linear.json
![](topologies/linear.png)

#### example.json
![](topologies/example.png)

#### warm-up.json
![](topologies/warm-up.png)

## Self-assessment
The self-assessment for this lab will be available on Moodle on Friday, March 22nd. Please complete the self-assessment by 11pm on Monday, March 25th.
