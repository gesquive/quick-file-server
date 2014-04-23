###quick-file-server

Run a quick simple file server to share files

```
Usage: quick-file-server [options]

Options and arguments:
  -r --root-dir <path>              The directory path for the hosted files.
                                        (default: CWD)
  -p --http-port <port>             The port for the server to listen on.
                                        (default: 8080)
  -n --no-dir-list                  Turn off directory listing.
  -u --update                       Checks server for an update, replaces
                                        the current version if there is a
                                        newer version available.
  -h --help                         Prints this message.
  -v --verbose                      Writes all messages to console.
```

#### Notes
Requires python 2.4+

If you make changes to any of the resources, you will need to run compile.py to encode them and update the script.


#### Installation Instructions

Run the following command:
```
SDIR=/usr/local/bin/; wget https://raw.github.com/gesquive/quick-file-server/master/quick-file-server.py -O ${SDIR}/quick-file-server && chmod +x ${SDIR}/quick-file-server
```

Change the value of `SDIR` to change the destination directory.
