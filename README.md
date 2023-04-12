# RAT POISON

## Table of Contents
- [About](#about)
- [Development Setup](#development-setup)
- [Team Members](#team-members)

# About
The current method for processing MRI images to isolate regions of interest of rat brains
requires manual annotations on each individual image. As the number of subjects and images
increases, this process becomes increasingly costly and inefficient. A software solution is
necessary to reduce the processing time. This project seeks to be that solution, leveraging 
an existing atlas, a map of regions of interest, to segment rat brain MRIs autonomously. This
user-friendly interface will allow selecting a group of images for processing and a set of regions
of interest, and a background task will create a binary mask for each of the selected regions of
interest that is exported on completion. Overall, this software solution will require significantly
less manual work and greatly reduce time that is takes to annotate MRIs.

# [Development Setup](#development-setup)
1. Clone the repository using one of the following options:    
    - __[Option 1]__ Using SSH:
        ```
        git clone git@github.com:danielcasto/RAT.git
        ```
    - __[Option 2]__ Using HTTPS:
        ```
        git clone https://github.com/danielcasto/RAT.git
        ```
        
2. Install python and pip. This project was developed and testing using ```Python 3.10.11``` and ```Pip 23.0.1```.

3. Install the required python packages using pip. To do so, run the following command in the top-level directory of the cloned repository:
      ```
      pip install -r requirements.txt
      ```

4. Make any desired changes.

5. Preview your changes using flask by executing the following commands:
      ```
      python main.py
      ```

# Team Members
| Name  | Username |
| ------------- | ------------- |
| Daniel Casto | @danielcasto |
| Cassandra Garzia | @cassandra-garzia |
| Henry Rivero-Vera | @henryriverovera |
| Kevin Vega Gonzalez | @kvega005 |
