# NPX_Reports
A TelegramBot module for NPX reports

## Instalation
First you will need to download or clone this repository and put it on the modules folder.
Then edit the following files:

keys.json
```json
{
    "npx_session": "YOURNPXSESSIONCOOKIE",
    "npx_url": "YOURNPXSERVERURL"
}
```

model.txt
```text
That's some example text
 - You can put some {keywords} on it - 
 \ if you want it to have dinamic data from the API /
 
 Eg.
    The current time is {time}
    
 It will be displayed as:
    The current time is 03:46 (or whatever time it is when you give the command)
```

## KeyWords List
KeyWords for model.txt
```python
{dep_name} = Returns capitalized value for the department's name
{avg_duration} = Returns the avarage duration of the calls
{month_name} = Returns the month name
{time} = Returns the current time in the format HH:MM
{avg_waiting} = Returns the avarage waiting time
{total_time} = Returns the total time of all the calls
{ans_calls} = Returns the amount of answared calls
{total_calls} = Returns the amount of received calls
{day} = Returns the current day of the month
{perc_ans} = Returns the percentage of the answered calls
```

## Usage
Send a message in the chat as in the following example:
```
/npx dp_name
```
Where the `dp_name` is equals to the name of one the call queues.

And you're done! The bot will reply with all the data you wanted.
