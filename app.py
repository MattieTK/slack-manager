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
                     'Archived', 'New Name', 'To Archive'])
    for channel in channel_list['channels']:
        chanlist = [channel['id'], channel['name'], channel['purpose']['value'].replace('\n', '\\n'), channel['topic']['value'],
                    channel['is_archived']]
        writer.writerow(chanlist)
    file.close()


def writeChannels():
    print('This will write the channels, are you sure? y/N')
    prompt = input('')
    if prompt is not "y":
        exit()
    file = open("./output/clean-times.csv", "r")
    reader = csv.reader(file)
    rownum = 0
    for row in reader:
        if rownum == 0:
            rownum += 1
            continue
        channelID = row[0]
        print(row)
        try:
            if row[5]:
                print("Renaming %s to %s?" % (row[1], row[5]))
                # prompt = input('')
                # if prompt is "y":
                try:
                    client.channels_rename(channel=channelID, name=row[5])
                except slack.errors.SlackApiError:
                    pass
        except IndexError:
            pass
        try:
            if row[6] == "TRUE":
                print("Archiving %s?" %
                      (row[1]))
                # prompt = input('')
                # if prompt is "y":
                try:
                    client.channels_archive(channel=channelID)
                except slack.errors.SlackApiError:
                    pass
        except IndexError:
            pass
        # This is broken until you can join/part
        # try:
        #     if row[7]:
        #         print("Purpose of channel: %s changing to : %s" %
        #               (row[2], row[7]))
        #         # prompt = input('')
        #         # if prompt is "y":
        #         try:
        #             client.channels_setPurpose(
        #                 channel=channelID, purpose=row[7])
        #         except slack.errors.SlackApiError:
        #             pass
        # except IndexError:
        #     pass
    file.close()


readChannels()
writeChannels()
