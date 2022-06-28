# DBL-Data-Challenge-Group23

> "The first data challenge revolves around the question of how you compare the performance of Airlines when they use Twitter as a communication channel. The dataset you will be analyzing consists of a large number of tweets from some airlines, and you will be asked, in a role-playing game, to analyze the data for one of your clients. Your client is KLM (Royal Dutch Airlines), and in this course, KLM is interested in assessing their performance when using Twitter as a communication channel. They are generally interested in comparing their performance to other airlines in general and British Airways in particular. KLM will be represented by A KLM marketeer. The marketeer wonders whether his Twitter team (which tries to respond quickly to incoming tweets) is doing a good job and whether this is useful for the company, particularly in comparison to the British Airways."


!!!! ***THESE FILES WILL NOT RUN UNLESS PROVIDED WITH THE IP AND PASSWORD OF THE SQL SERVER WHICH ARE NOT INLCUDED*** !!!
Instuctions on running a local version are below

This zip file inlcudes python files for making the plots inlcuded in our posterRunning the Main file produces plots based on an inputted month (4 doesn't work as an input because that month is missing from our data).The Categories_sentiment.py and plot_superplot_heatmap_in_plot.py files may need to be run separately on some machines these can be run by simply calling the funtion with the month number as input. The actual data used to produce these graphs is too large to store on github and is therefore left out, a link to the MySQL code to recreate the database can be found here:

[MY SQL zip file](https://tuenl-my.sharepoint.com/:u:/g/personal/p_c_nierop_student_tue_nl/ETyTkx1E7RFEjcv8m4VUWH4BE6jsaQIONQ0sYSf_INAkEw?e=DCfMhd) (Only acessible to those with a TU/e account)

and instructions on installing MySQL locally can be found here:<br>
[Install MSQL](https://www.mysqltutorial.org/install-mysql/) <br>
[Create An Empty Database](https://www.mysqltutorial.org/mysql-create-database/) <br>
[Load a SQL file into the Database](https://www.mysqltutorial.org/how-to-load-sample-database-into-mysql-database-server.aspx)

If a local database is used then lines where the function ["create_engine"](https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector) is called must be edited to point to the local server.

The sentiment analysis used for this can be found on [Hugging Face](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)


