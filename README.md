# Readability Book Parser

Proof of concept for an online book parser that sends articles to Readability.com

## Idea

There are so many great programming books out there for free (see http://resrc.io/list/10/list-of-free-programming-books/). For those that are not downloadable as a PDF, I needed a tool to format them nicely and store them so I can easily pull them up on my tablet or phone.
This little python script does just that. Put in a URL to parse, define a CSS class to look for (ideally some sort of 'table-of-contents' container, and let the script do the rest.

## Usage

Make sure to copy the settings_template.py to create settings.py with your own credentials.

```
python openbook/main.py -u http://openbook.galileocomputing.de/java7/ -c '.main' -t 'Java 7'
```

|Option|Description|
|---|-----------------------------------------------------------------------------------|
| u | URL with table of contents to parse (required)                                    | 
| c | CSS Class or ID to parse, eg. '.main-content' (required)                          |
| t | Tag name in Readability. Defaults to <title> of site if empty.                    |

## Disclaimer

Please note that this is my first ever Python program, so there is probably some room for improvement. Let me know if you find anything obvious! :)

## To Do's

* instead of using Readability for parsing and storing, write own (simple) parser
