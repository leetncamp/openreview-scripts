#!/usr/bin/python
import sys, os, shutil
import argparse
import openreview
import ConfigParser
from variables import Variables
from variables import parse_properties

def compile_template(template_path, config):
    '''
    Generates source code from a template file
    '''
    print "compiling template path: ", template_path
    with open(os.path.join(os.path.dirname(__file__), template_path)) as template:
        template_string = template.read()

    for replacement in config:
        template_string = template_string.replace('<<{0}>>'.format(replacement), config[replacement])

    return template_string

def process_params(params, config):
    webfield_src = None
    process_src = None

    if 'web_template' in params:
        webfield_src = compile_template(params.pop('web_template'), config)

    if 'process_template' in params:
        process_src = compile_template(params.pop('process_template'), config)

    return params, webfield_src, process_src

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True)
    parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
    parser.add_argument('--baseurl')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference_dir = os.path.dirname(args.config)

    # load config
    config_file = args.config
    config = parse_properties(config_file, 'config')

    # initialize variables
    variables = Variables()
    variables.init(conference_dir)

    initial_objects = {
        'groups': variables.groups['initial'],
        'invitations': variables.invitations['initial'],
    }

    # replace templates with javascript code, then post the groups/invitations
    for obj_name, openreview_objects in initial_objects.iteritems():

        if obj_name == 'groups':
            class_type = openreview.Group
            post = client.post_group
        if obj_name == 'invitations':
            class_type = openreview.Invitation
            post = client.post_invitation

        for id, params in openreview_objects.iteritems():

            params, webfield_src, process_src = process_params(params, config)
            obj = class_type(id, **params)

            if webfield_src:
                obj.web = webfield_src

            if process_src:
                obj.process = process_src

            post(obj)
            print "posted ", obj.id

if __name__ == '__main__':
    main()



