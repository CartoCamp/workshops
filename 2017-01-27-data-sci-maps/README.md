# Data Science + Maps workshop notes

## Event info

*   Date: Jan 27, 2017
*   Event page: <https://www.meetup.com/CartoCamp/events/236668763/>
*   Hosted by:
    *   Andy Eschbacher (Twitter @MrEPhysics, GitHub @ohasselblad)
    *   Danny Sheehan (Twitter and GitHub @nygeog)

### Schedule

*   2:30 -- Setup
*   3:00 -- Overview of workshop
*   3:10 -- Getting started, toolkit, getting accounts (and API keys), etc.
*   3:30 -- Static and interactive maps
*   3:45 -- Spatial statistics
*   3:50 -- Discussion
*   4:00 -- Open office hours

## Getting setup

We'll work from a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) so we all have the same development environment.

### Clone CartoCamp workshop repo

Clone the CartoCamp workshop repo and move into the directory for today's workshops.

```bash
$ git clone https://github.com/CartoCamp/workshops.git
$ cd workshops/2017-01-27-data-sci-maps
```

### Setup environment

```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ jupyter notebook
```

### requirements.txt:

```text
cartodb==0.8.1
jupyter==1.0.0
numpy==1.12.0
scipy==0.18.1
pandas=0.19.2
requests=2.13.0
```

## Danny's Portion of the workshop
[Link to Danny's Notebooks](https://github.com/CartoDB/cartocamp/tree/master/20170127)
