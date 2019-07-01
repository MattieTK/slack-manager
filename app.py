#!/usr/bin/env python3

import os
import logging
import slack
import ssl as ssl_lib
import certifi
import json
import csv
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

slacktoken = os.getenv('SLACKTOKEN')

client = slack.WebClient(token=slacktoken)


def readChannels():
    file = open("./output/channels.csv", "w+", newline="\n", encoding="utf-8")
    channel_list = client.channels_list()
    fieldnames = ['members', 'is_channel', 'creator', 'id', 'name', 'is_org_shared', 'is_member', 'is_general', 'is_archived',
                  'is_private', 'is_mpim', 'purpose', 'is_shared', 'num_members', 'name_normalized', 'topic', 'created', 'previous_names', 'unlinked']
    writer = csv.writer(file, delimiter=",", quotechar='"',
                        quoting=csv.QUOTE_ALL)
    writer.writerow(['ID', 'Name', 'Purpose', 'Topic',
                     'Archived', 'New Name', 'To Archive', 'New Purpose'])
    for channel in channel_list['channels']:
        chanlist = [channel['id'], channel['name'], channel['purpose']['value'].replace('\n', '\\n'), channel['topic']['value'],
                    channel['is_archived']]
        writer.writerow(chanlist)
    file.close()


def writeChannels():
    print('This will write the channels, are you sure? y/N')
    start = input('')
    if start is not "y":
        return
    print('Do you want to confirm every action? Y/n')
    confirm = input('')
    if confirm is not "n":
        confirm = True
    file = open("./output/channels.csv", "r")
    reader = csv.DictReader(file)
    rownum = 0
    for row in reader:
        if rownum == 0:
            rownum += 1
            continue
        channelID = row['ID']
        authData = client.auth_test()
        print('Running on channel %s' % (row['Name']))
        #
        # Change Name
        #
        try:
            if row['New Name']:
                print("Renaming %s to %s" % (row['Name'], row['New Name']))
                if confirmCheck(confirm):
                    try:
                        client.channels_rename(channel=channelID, name=row['New Name'])
                    except slack.errors.SlackApiError:
                        print(slack.errors.SlackApiError)
                        pass
        except KeyError:
            pass
        #
        # Change Archive state
        #
        try:
            if row['To Archive'] == "TRUE":
                print("Archiving %s" %
                      (row['ID']))
                if confirmCheck(confirm):
                    try:
                        client.channels_archive(channel=channelID)
                    except slack.errors.SlackApiError:
                        print(slack.errors.SlackApiError)
                        pass
        except KeyError:
            pass
        #
        # Change Purpose
        #
        try:
            if row['New Purpose']:
                print("Purpose of channel: %s changing to : %s" %
                      (row['Purpose'], row['New Purpose']))
                if confirmCheck(confirm):
                    members = client.conversations_members(channel=channelID)
                    if authData['user_id'] not in (members['members']):
                        part = True
                        client.conversations_join(channel=channelID)
                    try:
                        client.channels_setPurpose(
                            channel=channelID, purpose=row['New Purpose'])
                    except slack.errors.SlackApiError:
                        print(slack.errors.SlackApiError)
                        pass
                    if part:
                        client.conversations_leave(channel=channelID)
        except KeyError:
            pass
        #
        # Change Topic
        #
        try:
            if row['New Topic']:
                print("Topic of channel: %s changing to : %s" %
                      (row['Topic'], row['New Topic']))
                if confirmCheck(confirm):
                    members = client.conversations_members(channel=channelID)
                    if authData['user_id'] not in (members['members']):
                        part = True
                        client.conversations_join(channel=channelID)
                    try:
                        client.channels_setTopic(
                            channel=channelID, topic=row['New Topic'])
                    except slack.errors.SlackApiError:
                        print(slack.errors.SlackApiError)
                        pass
                    if part:
                        client.conversations_leave(channel=channelID)
        except KeyError:
            pass
    file.close()

def confirmCheck(confirm):
    if confirm == True:
        print("Confirm? y/N")
        prompt = input('')
        if prompt in {True, 'y', 'Y', 'yes'}:
            return True
        else:
            return False

# readChannels()
writeChannels()
