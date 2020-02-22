# Library Management

This Application is designed to manage the books and its buyers from online at library. Library management system is split into two user level access
    - Admin is the one who is responsible for maintainance of purchase of the books by users through the system.
    - User is the normal user who can request for any book from library while searching through library database.

#WHAT IT DOES:

    - An admin can
        ```add```
        ```update```
        ```delete```
    the books to / from library database.
    - An admin can also update the stock of these added books.
    - An user can request for the book which is available, and once it is approved by admin the user can get the book from library. Admin can also reject the request of the user.
    - User can access the books only as long as the stocks are available. Once available stock is exceeded, user can decide later either to wait for it to become available or delete the request.
    - User will be notified
        ```When a ordered book becomes unavailable or rejected or back available```
        ```When a ordered book is approved by admin```
        ```When a book in posession is going to be expired```

#TECHNOLOGY STACK:

    - DJANGO
    - POSTGRES
    - REDIS

#SCHEMA:
 ```https://dbdiagram.io/d/5e37f5939e76504e0ef0f49a```
