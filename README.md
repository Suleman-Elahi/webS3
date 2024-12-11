# webS3

![webS3 UI](https://res.cloudinary.com/suleman/image/upload/v1733921445/webS31.png)

![webS3 Video Player](https://res.cloudinary.com/suleman/image/upload/v1733921445/webS32.png)

A very simple web app to display all files from S3, and maybe view/play/download them.

This is a simple tool to display all files from a S3 bucket and display all the files from it. It can play videos (in video.js player) and display images.

Just set these environment variables and then just run/deploy the app using 

    flask run

Or,

    flask run &

Or you can also use some other WSGI or ASGI server like `gunicorn` or `waitress`. I am using it on Vercel so I don't need that.

If you also want to deploy it on Vercel then you can do that easily. Just click on the following button.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Suleman-Elahi/webS3)

Or, you can also import the Git repository manually. Need to set the following environment variables. 

If you are using the custom domain for the s3 bucket then you must set `BUCKET_DOMAIN` environment otherwise just leave it as it is. Others are mandatory and listed below. 

    BUCKET_DOMAIN    (Optional)
    PGSQL_URI
    AWS_DEFAULT_REGION
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_BUCKET_NAME
    
`PGSQL_URI` can be set to a postgres database in this format: `postgresql://USER:PASSWSORD@HOST:5432/DATABASE` 

If you are using Vercel's free Postgres DB then must append `?sslmode=require` in the end of the database URI above.

Or, if you want to SQLite for temp/local use on PC or VPS then just set `PGSQL_URI` to: `sqlite:///files.db`    (it will not work on Vercel as it gives you read-only system)

I created it for a simple use case of mine.

Feel free to extend it. In future I might add the ability to delete and upload files as well.
