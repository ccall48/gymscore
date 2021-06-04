## Gymnastics Scoring web app
View to get a working gymnastics web app scoring system so spectators and
parents can view current scores for their progress in a competition.

I have limited knowledge of exactly how the scoring works 100% at the
moment, hopefully this can be fixed as we go along. If you are proficient
in scoring and wish to contribute then get involved.

*** login auth is not currently implemented. project is not at this stage ***

## Admin user(s)
- create athletes, add and edit/update details.
- create competitions and close old competitions.
- create and add clubs.
- edit/update judges scoring if mistake found.

## Judge user(s)
- add scores for athletes after performance.
- ability to update/edit score for athlete in case of typo.
- ability to add comment to score card.

## User user(s)
These will be athletes and parents competing in the competitions.
- login to view personal progress and scoring for current meeting.
- view past performances and scoring for previous meetings.
- add/update profile picture if desired.
- connect up a dashboard for athletes to track performance metrics?

## Page viewer
Regular viewer of page to be able to view current scoring of competition
whilst in progress. This might also need a frontend connected to an API
so scores can be projected and viewed on screen at apparatus for current
competing group.

# To start the project
clone the repo to your computer and create a python virtual environment.
python v3.8 or greater recommended.

```
git clone https://github.com/ccall48/gymscore.git
```
cd into the cloned repo.
```
python3 -m venv .
```
install python required modules with...
```
pip install -r requirements.txt
```
to initialize db or pre populate a db with some dummy data...
```
flask initdb
or
flask bootstrap
```
to prepare the app to run create file config.json file 
example:
[cpnfig.json example](config.json.sample)


to run the app 

```
python app.py
```
development server should load the app and be available at both
http://localhost:5050/ and http://lan_ip:5050/ on your local network.
