# My-Top-10-Videogames Webpage

 A full-stack web application that dynamically displays a list of your favorite video game titles. Allows for full CRUD operation of adding new entries, update existing exntries, and deletion.

# Tech Stack

### Front-End

HTML, CSS, Bootstrap for templating, Jinja for rich templates, WTForms for templated forms

### Back-End

Python with Flask Framework for a simple basic backend server. (As of now, this is only locally hosted!)

### Database

SQL Database via sqlalchemy module in python.

### API

This application uses the [IGDB](https://www.igdb.com/) API to get information such as games, titles, and cover art from their database. 


# Demonstration
## Main Page Look
![Example of main page](https://github.com/rinriukato/My-Top-10-Videogames-Webpage/blob/main/sample-images/main-page-example.gif)
Quick example of what the main page looks like. Uses Jinja to dynamically read and display all card templates and places them onto the website. Each card containing a name, release date, your own review, and a summary provided by IGDB

## Create new cards
![Example of Add](https://github.com/rinriukato/My-Top-10-Videogames-Webpage/blob/main/sample-images/add-example.gif)
You can add a new card by pressing the "Add Video Game" button at the bottom. You will be prompted to a short form to search for a video game title. This will make an API call to the IGDB to search for up to 50 titles with that similar name and the will redirect you to the select page so that you can choose the title. (Some titles have deadlinks and will cause 404. This is most likely because IGDB entires are provided by users and they have duplicated/unfinished entires). Next, you will provide a rating and review. Once completed, the main page will now have your new card. Complete with cover, release date, and summary from IGDB. It's position in the list is based on its rating you've provided. 

## Update existing cards
![Example of Update](https://github.com/rinriukato/My-Top-10-Videogames-Webpage/blob/main/sample-images/update-example.gif)
Here is an example of how you can update existing entries. You can update your own rating and review on the card and once finished, it will redirect you back to the main page where the order of the cards will be updated in descending order (number 1 at the bottom).

## Delete existing cards
![Example of Delete](https://github.com/rinriukato/My-Top-10-Videogames-Webpage/blob/main/sample-images/delete-example.gif)
If you had wish to delete a card, simply click the "delete" button on each card and the page will automatically delete that entry from the database and the page will reflect that change.

# Note
Since I am using the IGDB, it requires the usage of Client API keys from Twitch and IGDB. So if you wish to use this project for yourself, refer to this "[Getting Started](https://api-docs.igdb.com/#getting-started)" page on IGDB's API docs. It does require a twitch account, 2FA, and to register an application on the twitch developer portal.
