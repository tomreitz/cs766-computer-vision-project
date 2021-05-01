# CS766 Project (Spring 2021)

**Group Members**: [Tom Reitz](https://github.com/tomreitz) (treitz@wisc) and [Zach Baklund](https://github.com/zbaklund) (baklund@wisc)

This page contains documentation and resources for our group project for [CS766](http://pages.cs.wisc.edu/~mohitg/courses/CS766/) (Computer Vision) at [UW-Madison](https://www.wisc.edu/) in Spring 2021. Our project's goal is to detect and quantify facial wrinkles (rhytides) for age estimation.

* [Project Proposal](proposal.md) (due February 24)

* [Midterm Report](midterm-report.md) (due March 24)

* Final Presentation ([Slides](https://docs.google.com/presentation/d/1aJU_h0YStWdd_LNF0Sg-z33jkzOfN0_mpU_Pu-ZvVHo/edit?usp=sharing), [Video](https://www.youtube.com/watch?v=TrRghR6Su7I)) (due April 23 - April 30)

* Final Report (due May 5)

* [This web page](https://tomreitz.github.io/cs766-computer-vision-project/) (due May 5) 

### Summary

In this project, we focus on age estimation based on specific types of rhytides (facial wrinkles) as they appear in different parts of faces. We use edge detection to make rhytide measurements for each rhytide type and construct a feature vector from the measurements for statistical analysis and machine learning prediction.

We tested our pipeline using the [UTKFace dataset](https://susanqq.github.io/UTKFace/). As discussed in our [presentation](https://www.youtube.com/watch?v=TrRghR6Su7I), we found issues with many of the UTKFace images. So we cleaned the dataset, removing many images of poor quality or with occlusions. This cleaned dataset is available [here](https://github.com/tomreitz/cs766-computer-vision-project/tree/main/data/UTKFace-cleaned.zip).

Our code is [here](https://github.com/tomreitz/cs766-computer-vision-project/tree/main/code), with [a README](https://github.com/tomreitz/cs766-computer-vision-project/tree/main/code/README.md) which explains how to run it.

Ultimately, we found that variations in lighting and facial expressions cause enough noise to make this method unreliable for estimating age.
