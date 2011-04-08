## Mozilla Mobile Phonebook README ##

[Atul](http://toolness.com) made this phonebook to scratch two itches:

* Learn how to use [JQuery Mobile](http://jquerymobile.com/).
* Make an offline-capable version of the [Mozilla Phonebook](https://ldap.mozilla.org/phonebook/) with a user interface that's optimized for small screens.

## Why This Isn't Public ##

Very little of the source code contains confidential information; in fact, the only thing that can potentially be considered confidential is the URL to Mozilla's LDAP server in `fetch.py`. It'd be nice to decouple that from the rest of the app, and then make the code public.

## Prerequisites ##

All you need is Python 2.6 or later, which is used to run scripts that talk to LDAP and cache the Phonebook contents as static files. The actual web app consists entirely of static files.

## Usage ##

* Create a file in the root directory of the repository called `config.json`. Paste the following into it and edit as necessary:

<pre>
    {
      "username": "my_username@mozilla.com",
      "password": "my_password"
    }
</pre>

* Run `fetch.py && combine.py`.

* Serve the contents of the `static-files` folder. For local development only, you can use HTTP; for hosting on the Web, make sure it is served over HTTPS with some kind of access control.

## Development ##

When you're hacking on the app's HTML/JS/CSS, make sure you delete the `static-files/cache.manifest` file, which is created by `combine.py`. This will cause the browser to obsolete the application cache and ensure that you're always looking at the latest version of your code when you reload the page.
