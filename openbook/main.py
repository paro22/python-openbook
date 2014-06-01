#!/usr/bin/python

"""
Readability Book Parser
--------------------
Proof of concept for a online book parser that sends articles to Readability.com
"""

import optparse
import book_parser
import readability_client


def get_options():
    """
    Define and retrieve options from the command line
    """

    parser = optparse.OptionParser()
    parser.add_option('-u', help='URL with table of contents to parse (required)', dest='url', action='store_true')
    parser.add_option('-c',
                      help='CSS Class or ID to parse, eg. main-content (required)',
                      dest='css_class',
                      action='store_true')
    parser.add_option('-t',
                      help='Tag name in Readability. Defaults to <title> of site given in option -u if empty.',
                      dest='tag', action='store_true')
    (opts, args) = parser.parse_args()

    # Making sure all mandatory options are set:
    mandatory_options = ['url', 'css_class']
    for m in mandatory_options:
        if not opts.__dict__[m]:
            print "Mandatory options is missing!\n"
            parser.print_help()
            exit(-1)

    return opts, args


def main():
    """
    Main function that starts everything else
    """

    # get options:
    (opts, args) = get_options()
    url = str(args[0]) if opts.url else ""
    css_class = str(args[1]) if opts.css_class else ""
    tag = str(args[2]) if opts.tag else ""

    # start parser:
    bp = book_parser.BookParser(url, css_class, tag)
    url_list = bp.get_links()
    tag_name = bp.get_tag_name()

    # DEBUG (only send part of the links):
    #url_list = url_list[20:21]
    #print url_list

    # send stuff to Readability:
    rc = readability_client.ReadabilityClient(url_list, tag_name)
    rc.send_to_readability()


if __name__ == '__main__':
    main()