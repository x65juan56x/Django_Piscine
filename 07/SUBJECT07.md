Today’s specific rules
• Today, you’re gonna develop a single site. It will feature articles a user will be able
to consult. Logged-in users will be able to publish new articles or save some in a
favorite list.
• You can name this site as you like and give it the focus you prefer (news, fan fictions,
erotic novellas...).
• You can choose the database you like as long as it is compatible with Django’s LTS
native ORM.
• Your repo will have the form of a single Django LTS project. It will not split in exercises, as usual. Each one will add a functionality to the project. The functionality
and its implementation will be graded.
• Implementing a "hard" url is STRICTLY prohibited. You must refer to the URL’s
name. Either in the views or the templates.
• Implementing a view in the form of a functions is STRICTLY prohibited. You must
only use generic views.
• Remember exercises will be evaluated in project’s order.
• English is the default language of your site. The content of the database can be
anything. If you have a soft spot for ancient greek, go for it.
• You must leave the default administration application.
Don’t waste time on what’s not required!

---

Exercise 00
Exercise 00: Model building - Generic Class
Files to turn in :
Allowed functions :
Create a new project. You can name it and set the application structure as you like.
Think of a logical structure. The easier it is to understand, the easier the evaluation.
Implement the following models:
• Article: Content of the article and a few metadata. It must feature the following
fields:
◦ title: Article’s title. Character chain 64 max size. Non null.
◦ author: Article’s author. References a record of the User model. Non null.
◦ created: Creation’s complete date and time. Must be automatically filled
when created. Non null.
◦ synopsis: Article’s abstract. Character chain. Max size 312. Non null.
◦ content: The article. It’s a text type. Non null.
The __str()__ method must be ’overrode’ to send ’title’
• UserFavouriteArticle: User’s favorite articles. Must feature the following fields:
◦ user: References a record of the User model. Non null.
◦ article: References a record of the Article model. Non null.
The __str()__ method must be overridden to send ’title’ included in the Article
model.
Once all of this is done, we can tackle the real goal of this first exercise.
Using only generic views (except ’View’ that you can’t inherit directly), you must
implement the following functionalities to your site. Each functionality must have its
own URL:
Articles: HTML page displaying every field as an HTML table (except the content) of
every recorded article in the Article table).
The table must have a header indicating the title of each column.
Home: Mandatory URL: ’127.0.0.1:8000’. Redirects to Articles
Login: HTML page displaying a POST type form. Logs an logged-out user thanks to a
username and a password. In case of an error, the page must display a message
describing said error. If successful, the view must redirect to ’Home’.
You must also provide at least five articles examples from three different users. Provide
fixtures if necessary. The article’s content doesn’t matter. Basic ’lorem ipsum’ can be
enough.
No css formatting is required in this exercise.

---

Exercise 01: Generic Class again
Files to turn in :
Allowed functions :
Using only generic views (except ’View’ that you can’t inherit directly), you must
implement the following functionalities to your site. Each functionality must have its
own URL:
Publications: HTML page displaying as HTML tables the fields ’title’, ’synopsis’ and
’created’, of every article recorded in the ’Article’ model whose user is currently logged-in.
For each article, you also must implement a link which URL must include the article’s identification leading to the ’Detail’ functionality of said article.
The table must have a ’header’ indicating the title of each column.
Detail: HTML page displaying every field of a given article located in the database. It
identification must be in the URL.
Field disposition is free.
For each article in the Articles functionality present in the HTML table from the
previous exercise you will also add a link towards this article’s ’Detail’.
Logout: A link logging out a logged in user. You can place the link wherever you want
as long as it is visible and accessible. Once logged out, the user is redirected towards
’Home’.
Favourites: HTML page displaying the titles of the current user’s favorite articles as a
list of links.
Each link - the URL of which must include the article’s identification - must lead
to the article’s ’Detail’ functionality.
You must provide at least one user with at least two different favorite articles.

---

Exercise 02: Generic Class - CreateView
Files to turn in :
Allowed functions :
Using only CreateView, you must implement the following functionalities to your site.
Each functionality must have its own URL:
Register: HTML page featuring a ’POST’ type form allowing a logged out user to create
a new user account.
The form must require the login, a password and a password confirmation. this
form must be accessible to a URL exclusively dedicated to it and ending with
’register’.
Publish: HTML page featuring a ’POST’ type form allowing a logged-in user to publish
a new article. The ’author’ field must not be displayed. It must be completed in
the view during the validation process. You have to use a ’form’ object created
by your view to generate your form (no handwritten <input> tag for the fields in
your form!)
Add a link towards this functionality in the Publications functionality template.
Add to favourite: HTML page containing a ’POST’ type form located in the detail page
of an article. No field must be visible. The ’article’ field must be pre-filled
with the current article ID and during validation, ’user’ field must be filled with
the logged user ID. This mechanism allows to add the current article in the logged
user’s favorite list.

No css formatting is required in this exercise.

Did you know that Django proposes ready-made forms?

---

Exercise 03: Template tags and Filters
Files to turn in :
Allowed functions :
In this exercise, you will create a menu that must be visible from EVERY page of the
site.
Every link in this menu lead to functionalities YOU HAVE ALREADY CREATED. If something is missing, start questioning yourself.
This menu must feature the following elements:
• Home: A link to the ’Home’ functionality (that redirects towards ’Articles’, remember?).
• Last Articles: A link to the ’Article’ functionality. You can adapt the name
of this link according to the theme of you site (but it must be in English!).
• If a user is not registered:
◦ Register: A link to the ’Register’ functionality.
◦ Login: ’Login’ functionality. It’s a little different here, because it’s not just
a link, you must include the whole form IN the menu.
This meams it will be accessible from every page, not only from the dedicated
page you have created.
However, this page must always display error messages if the form is invalid.
• If a user is registered:
◦ Favourites: Link to the ’Favourites’ functionality.
◦ Publications: Link to the ’Publications’ functionality.
◦ Logged as <user>: Simple text indicating that the user is logged. Of course,
<user> must be replaced by the name of the current user.
◦ Logout: ’Logout’ functionality. Now, you have found a place to set up this
link.
Using tags and filters, modify the templates that list every article so that:
• The abstract is reduced to 20 characters maximum. The follow-up must be replaced
by suspension points. You must have an example ready to demonstrate it works.
• The list of articles must be sorted out by date, from the newest to the oldest.
• An additional column mentions how long the article has been published for.
No css formatting is required in this exercise.

---

Exercise 04: Bootstrap
Files to turn in :
Allowed functions :
Using Bootstrap, give your menus the same CSS formatting as the one in the provided
image in today’s resources.

---

Exercise 05: Internationalization
Files to turn in :
Allowed functions :
Translate the whole Articles functionality of the site, as well as the menu (which is
also visible from here) English depending on the prefix in the URL.
For instance:
If my URL is: 127.0.0.1:8000/en/articles, the whole content will be in English.
If this URL is: 127.0.0.1:8000/<??>/articles, the whole content will be in the
language indicated in <this> section of the address.
You won’t have to translate the database content or the site’s name.
The site’s default language must be English.
Add a link allowing to switch language on this page.

---

Exercise 06: Testing
Files to turn in :
Allowed functions :
Using the framework integrated to Django, create the tests allowing to check that the
site behaves as follows:
• favourites views, publications and publish as well as their templates are only
accessible by registered users.
• A registered user cannot access the new user creation form.
• A user cannot add the same article twice in their favorite list.
Your tests must be explicitly named, clearly specifying what they’re testing.
Fix all the errors your tests might have ran into.
