# Questions (Add your questions)
(We can email the authors after we compile all the questions)

1. Why are there so many genres (512 genres)?

     Ans. https://github.com/shenyangHuang/TGB/blob/main/tgb/datasets/dataset_scripts/tgbn-genre.py

     https://www.musicgenreslist.com/

3. How was the dataset collected?

     Ans. Combined [lastfm dataset](https://github.com/eifuentes/lastfm-dataset-1K) and [million songs dataset](http://millionsongdataset.com/). 


5. The average number of genres is 135 for each user. How is this possible?

     Ans. A song can belong to several genres because the weights vary a lot (could be very small) and there are several genres.

7. What is the unit of time in the timestamps column?

     Ans. Unix time. Can convert using in [python](https://www.geeksforgeeks.org/how-to-convert-datetime-to-unix-     timestamp-in-python/)

9. If the timestamps are unix , converting the dates are from 2005 to 2009. Was not supposed to be a month?

     Ans. Mistake in the paper. It is 4 years of data.

11. It says 1000 users in the paper, but there are only 992 users in the tgbn-genre dataset. Why?

     Ans. It is 992. Another typo in the paper.

