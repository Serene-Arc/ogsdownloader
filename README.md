# OGSDownloader

This is a simple command-line tool I developed to download the SGF files of games from an OGS profile. It will download the records of every available public game on the given profiles.

## Basic Instructions

To use this tool, you will need Python 3.9 or higher. You can see [here](https://www.python.org/downloads/) for how to download and install this for your respective OS. This is a command-line tool, to install it, type the following into the command-line:

```bash
python3 -m pip install ogsdownloader
```

This will install of the requirements and the tool itself. To use it to download all of your own games, enter the following command:

```bash
python3 -m ogsdownloader sgf_files -u <YOUR_USERNAME> -i --authorised
```

This will prompt for your username again, and then your password. Once you've provided your password, you shouldn't have to do so again since the tokens received will be saved in a configuration file and reused.

To download someone else's games, do the following command:

```bash
python3 -m ogsdownloader sgf_files -u <USERNAME>
```

## Arguments and Options

The following is an explanation of the available arguments and options for the tool.

- `destination`
  - The destination to which the files will be downloaded, this is required
  - Folder will be created if it doesn't already exist
- `--authorised`
  - Use user authentication when making requests to OGS
  - This will enable downloading private games from the authenticated person's profile
- `--username`
  - The username to authenticate with i.e. **your username**
- `-c, --config`
  - The config file to use
  - If not supplied, the tool will default to the applications directory
- `-f, --format`
  - The naming scheme for the files
  - By default, it is '{ID}'
  - See [Name Formatting](#name-formatting) below for details
- `-i, --interactive`
  - Whether to use interactive mode, prompting for username and password
  - Only useful when using an authorised instance
- `-s, --sleep`
  - The time to sleep in seconds between making consecutive requests to OGS
  - Defaults to 5 seconds
  - See [Rate Limiting](#rate-limiting) below
- `-u, --user-id`
  - The user ID or username of the profile to download from
  - Can be specified multiple times e.g. `-u 1234 -u 5678`
- `-v, --verbose`
  - Increases the output of the program

## Rate Limiting

OGS will cut off the downloads if too many requests are performed in too short a time. To prevent this, a sleep time is used to spread out the web requests. This is scraping etiquette. **Be polite. Downloading games is not as important as playing them.** OGS prioritises players, as they should. This tool takes traffic from the same servers; you can afford to wait a little longer, so keep the sleep time reasonable.

## Name Formatting

The downloaded files can be titled according to several variables. These are:

- `NAME`
- `ID`
- `START`
- `END`
- `BLACK`
- `WHITE`

To be replaced, these keywords must be surrounded in brackets e.g. `'{ID} {NAME}` will include both the name and the ID in the filename.

Black and white in this case refer to the usernames of the players on the respective sides on the game. Similarly, the 'start' and 'end' variables will produce ISO formatted strings for the start and end of the game. If the game is still in progress at the time of download, then the 'end' variable will be replaced with 'Unknown' instead.