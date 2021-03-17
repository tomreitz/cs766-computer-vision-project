We considered several publicly-available face image datasets to use in this project:

[**"Labeled Faces in the Wild" (LFW) dataset**](http://vis-www.cs.umass.edu/lfw/)
- Provides no age information for the images, so we eliminated this from consideration

[**UTKFaces face image dataset**](https://susanqq.github.io/UTKFace/)
- 23,708 images all labeled with  gender, age, and race (encoded in file names)
- Images are all 200x200 pixels in size
- Mostly head-on views of faces, but quality for some is poor (grainy or washed-out images)
- Running facial landmark detection code takes (2.1 secs/image), and faces are identified in 72% of images
- Running code on all 23,708 images could take 3.1 hours

[**IMDB-WIKI face image dataset**](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/)
- 460,723 images from IMDB (actors)
- 62,328 images from Wikipedia (celebrities)
- Dataset includes gender and age for each image, but not race (details are in .mat files in each dataset, which can be converted to CSV using mat.py in this directory)
- Images vary in size, most are at least 200x200 pixels, some much higher
- Some images are poor quality, include multiple faces, are a side-view of a face, or even something like a cartoon, but most are good
- Running facial landmark detection code on takes 1.9 secs per image, and faces are identified in 61% of Wikipedia images and 70% of IMDB images
- Running code on all 460,723 IMDB images could take 64 hours
- Running code on all 62,328 Wikipedia images could take 9.1 hours
