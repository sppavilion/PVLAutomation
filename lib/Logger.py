from inspect import getframeinfo, stack
from os import path
import os
import time
import bs4
import sys
import threading

class PVLogger(object):
    def __init__(self, filename='log.html', title='Automation logs'):
        html = """
            <!DOCTYPE html>
            <html lang="en">
              <head>
                  <title>""" + str(title) + """</title>
                  <meta charset="utf-8">
                  <meta http-equiv="refresh" content="10">
                  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
                  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans">
                  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto+Slab">
                  <style>
                      .box {
                        margin: 15px;
                      }
                      body {
                        font-family:Open Sans;
                        font-size:12;
                      }
                      h4 {
                        font-family:Roboto Slab;
                        font-size:14;
                      }
            
                      span.time {color:#00b300;}
                      span.caller {color:#0000b3;}
                      span.debug-message { color:#454545;}
                      span.info-message { color: #000000;}
                      span.warn-message { color:#cca300;font-weight:bold;}
                      span.error-message { color:#FF0000;}
                      span.critical-message { color:#cc0000;font-weight:bold;}
            
                  </style>
              </head>
              <body>
                <div class="box">
                    <div class="card">
                        <div class="card-header">
                            <h4>""" + str(title) + """</h4>
                        </div>
                        <div class="card-block">
                            <table class="table">
                                <tbody>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
              </body>
            </html>
        """
        filebase, file_extension = os.path.splitext(filename)
        if file_extension != ".html":
            print("Invalid filename provided. Please give filename like `abctest.html`")
            sys.exit(1)
        self.lock = threading.Lock()
        self.txt_log_file = filebase + ".log"
        self.html_log_file = filename
        f = open(self.html_log_file, "w+")
        f.write(html)
        f.close()

    def __write_to_file(self, properties):
            self.lock.acquire()
            try:
                with open(self.txt_log_file, "a") as txt:
                    txt.write("[" + str(properties['time']) + "] " + str(properties['caller']) + " " + str(
                        properties['message']) + "\n")
                    txt.close()

                with open(self.html_log_file) as inf:
                    txt = inf.read()
                    soup = bs4.BeautifulSoup(txt, "html.parser")

                tr = soup.new_tag("tr")
                td = soup.new_tag("td")
                timespan = soup.new_tag("span")
                callerspan = soup.new_tag("span")
                message_span = soup.new_tag("span")
                timespan.string = "[" + str(properties['time']) + "] "
                timespan['class'] = 'time'
                callerspan.string = str(properties['caller']) + " "
                callerspan['class'] = 'caller'
                message_span.string = properties['message']
                message_span['class'] = properties['type']
                td.append(timespan)
                td.append(callerspan)
                td.append(message_span)
                tr.append(td)
                soup.tbody.append(tr)

                html = soup.prettify(soup.original_encoding)
                with open(self.html_log_file, "wb") as file:
                    file.write(html)
                    file.close()
            except:
                print ("Exception occured while logging -")
            finally:
                self.lock.release()

    def debug(self, message):
        properties = dict()
        caller = getframeinfo(stack()[1][0])
        file = path.basename(caller.filename)
        properties['time'] = time.ctime()
        if str(caller.function) == "<module>":
            properties['caller'] = file + ":" + str(caller.lineno)
        else:
            properties['caller'] = file + " " + str(caller.function) + "():" + str(caller.lineno)
        properties['message'] = message
        properties['type'] = "debug-message"
        self.__write_to_file(properties)
        return

    def info(self, message):
        properties = dict()
        caller = getframeinfo(stack()[1][0])
        file = path.basename(caller.filename)
        properties['time'] = time.ctime()
        if str(caller.function) == "<module>":
            properties['caller'] = file + ":" + str(caller.lineno)
        else:
            properties['caller'] = file + " " + str(caller.function) + "():" + str(caller.lineno)
        properties['message'] = message
        properties['type'] = "info-message"
        self.__write_to_file(properties)
        return

    def warn(self, message):
        properties = dict()
        caller = getframeinfo(stack()[1][0])
        file = path.basename(caller.filename)
        properties['time'] = time.ctime()
        if str(caller.function) == "<module>":
            properties['caller'] = file + ":" + str(caller.lineno)
        else:
            properties['caller'] = file + " " + str(caller.function) + "():" + str(caller.lineno)
        properties['message'] = message
        properties['type'] = "warn-message"
        self.__write_to_file(properties)
        return

    def error(self, message):
        properties = dict()
        caller = getframeinfo(stack()[1][0])
        file = path.basename(caller.filename)
        properties['time'] = time.ctime()
        if str(caller.function) == "<module>":
            properties['caller'] = file + ":" + str(caller.lineno)
        else:
            properties['caller'] = file + " " + str(caller.function) + "():" + str(caller.lineno)
        properties['message'] = message
        properties['type'] = "error-message"
        self.__write_to_file(properties)
        return

    def critical(self, message):
        properties = dict()
        caller = getframeinfo(stack()[1][0])
        file = path.basename(caller.filename)
        properties['time'] = time.ctime()
        if str(caller.function) == "<module>":
            properties['caller'] = file + ":" + str(caller.lineno)
        else:
            properties['caller'] = file + " " + str(caller.function) + "():" + str(caller.lineno)
        properties['message'] = message
        properties['type'] = "critical-message"
        self.__write_to_file(properties)
        return
