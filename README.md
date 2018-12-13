# Installation

## Prerequisites

* `pipenv`
* `docker`
* `docker-compose`

## Setup

1.  Clone the repository
2.  Run `docker-compose build`

## Deploy

3.  Run `docker-compose down; docker-compose up -d`
4.  Add the schema to the database
    1. Enter the docker container with `docker exec -t -i berriesandgoods bash`
    2. `cd` into `berriesandgoods/`
    3. Run `python manage.py migrate`
    4. Run the contents of `default.sql` against the database
5. Open up `localhost` to see the application.

# Reason for Publishing

This is the repository for our project in the course D0018E, Database
Technology, at Luleå University of Technology.

We open source it, as our project is now complete, and we do not see that
anyone will be able to plagiarize our work without other people being able to
trace it back to us. If anyone has a problem with this, please contact us and
we will take it down.

We hope that it can be useful as a learning resource for other people.

# Report

## Executive Summary

Databases are a fundamental part of the way we perceive the web. In order
to practice using one, an E-Commerce website was built. It was decided to
sell berries and related goods.

The technology stack was based on Django on top of a PostgreSQL database. Due
to the problem constraint, the database schema was developed independently, and
then added to Django using its `inspectdb` command.

The service allowed for creating an account, adding items to a basket and
checking out that basket. It featured sorting and search, as well as product
review. It also provided tools for administrators, such as adding, removing
and editing products and orders.

Though this exercise is a good way of learning to work with a database,
it would be highly recommended to use the Django Object-Relational Mapping
tool in a real-world scenario.

## Introduction


The students were tasked with building a web application that was to be
used for e-commerce. The focus was to be placed on the database and server
layers, while constructing a usable website through which the user could
purchase items.

### Requirements


The system should be able to process orders. There should be the concept
of a shopping cart to which a customer can add products, and then check out
with payment. It was strongly recommended that the database be a relational
one. The use of a ORM for creating schemas was disallowed, because the goal
of the assignment was to learn to administer the database.

### Choice of Merchandise


Multiple different suggestions for merchandise were discussed, including
computers and cars. Eventually it was decided, that because the merchandise
itself was \emph{not} the main focus of the project, something less obvious
might as well be chosen. It was decided to sell berries, and in order to
make the variety of items sold a bit more diverse (for a more interesting
project), it was also suggested that related supplies, such as filters and
jars for jam production, would also be sold.

### Technologies

The choice of technologies was very open, which warranted some research into
different technologies. The choices were then made in favor of technologies
that would offer the most learning.

The choice for most of the stack fell on Django, because,

* It is a widely used, tried and tested technology
* Knowing Django could be an advantage in a future career
* Other colleagues told us it would be difficult, due to the constraint
about ORMs.

It was decided to make the application as production ready as possible,
hosting it on a remote server inside docker containers. The
Django server was run using gunicorn, which was then
mirrored using nginx for added robustness.

The choice for the database fell upon PostgreSQL because it
is a popular alternative to MySQL and has been gaining popularity
for many years. It is therefore a good technology to be acquainted with.

## Role Descriptions and Features

A common way to describe desirable features for a software project is to
formulate them in the form of user stories. Such a user story usually follows
the pattern shown below.

```text
As a <Role>  
I want <Feature>  
So that I can have <Benefit>
```

For the E-commerce website there are three kinds of users. Customers, visitors
and administrators. Below, a summary of the roles can be found. For complete
user stories, please refer to the Appendix. Due to lack of time the user
stories are not featured in the standard pattern manner.

### Role: Visitor

A Visitor is any user that is not logged in. Such a visitor is able to list
products, view product information find their current availability. They are
also offered the option of registering an account on the site, thus becoming
a Customer.

### Role: Customer

A Customer is a registered user **without** admin privileges. In order to
access Customer privileges it is required that the Customer is logged in.
A Customer can do everything that a Visitor can do, as well as adding items
to a shopping cart and making orders.

### Role: Admin

A Admin is a registered user **with** admin privileges. In order to access
Admin privileges it is required that the Admin is logged in. An Admin can do
everything that a Customer can do. An Admin can also add, update and remove
Products and Product Types, as well as handling orders.
