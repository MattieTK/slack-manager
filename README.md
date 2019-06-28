# slack-manager
A python app for doing Slack stuff via the API that's annoying at scale

Initially this works on doing channel management.

Run the file and it will output a csv of the channels in the workspace. You'll need a Slack API token which you can get from your user or via a legacy app.

You can then import this CSV into Google Sheets or likewise in order to make any edits collaboratively that you might want to. Make edits to the new columns, not the original columms.

You can set new names and archive state currently.

## To come
- [ ] Fix setting status
- [ ] Set topic
- [ ] Set automatic Google sheets export/Slack oauth
