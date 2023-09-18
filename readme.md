# what does it do
this is a simple script that checks folders for files that are no older then x and then posts them to a discord webhook so you dont need to manually go check the logs but can get them all in a nice neat message.

# how to use
1. make a config folder and place a config.json in there
2. paste the following code into the json and fill it in (note the double \\ in logfolders, python does not see a single \ as a character)
```
{
"logfolders": ["Example\\folder\\for\\logs],
"webhookurl": "your_webhook_url",
"daystosend": "age_of_files_in_days_to_send_to_webhook",
"daystodelete": "age_of_files_to_delete (can be left blank to disable)",
"maxfilesize": "max_file_size_to_send_in_megabytes"
}
```
3. save config and run script

# disclaimer
scripts are written by an amateur, use at your own risk