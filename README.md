## New Link Checker using Python

This is a simple script for python that takes a csv file of webpages, and collects all href link on that page and stores the data in a SQLite databse.
When the script is run a 2nd time, it will mark all links that is already in the database as "old" and add the new links into the database.
