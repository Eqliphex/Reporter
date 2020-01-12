## Reporter
This project is a responder designed to take case data, observables and  from TheHive, and transform them into a user-defined report based on a Jinja template.  

## Motivation
This project is part of a bachelor-project, which attempts to create an "easy-to-run" Security Operations Center (SOC). This module is inteded for anyone who needs a report generated from an individual case, and send it to customers via E-mail.
 
## Screenshots
Example of init method 
```
    """
    This Reporter class automates the effort of producing a case-report and optionally all of its associated data,
    such as observables and tasks.
    The primary function of this algorithm, is to take a JSON-structure gathered from TheHive's API, and filter it
    as per the provided filter-parameters given on activation.

    The algorithm assumes, that the dataset that's worked on, is either of any primitive type like int and string or
    a specific data structure list or dict, hence the dict- and list-builders.

    In short, the algorithm generates a new filtered tree-structure in JSON-format, which can be N-wide and N-deep.
    """
    def __init__(self):
        Responder.__init__(self)
        self.case_data_filter = ["endDate", "startDate", "title", "createdAt", "caseId", "pap", "tlp", "severity",
                                 "owner", "createdBy", "updatedBy", "summary", "tags", "resolutionStatus",
                                 "impactStatus", "status", "customFields"]
                                 
        self.case_observables_filter = ["data", "dataType", "sighted", "tags", "createdAt",
                    "createdBy", "pap", "tlp", "ioc", "startDate", "status"]
                    
        self.case_tasks_filter = ["caseTasks", "updatedBy", "createdAt", "flag", "description",
              "title", "createdBy", "updatedAt", "order", "status", "group"]
              
              
        self.api_key = self.get_param('config.api_key', None, 'Missing API-key')
        self.https_address = self.get_param('config.https_address', 'localhost')
        self.https_port = self.get_param('config.https_port', 9000, 'Missing thehive port')
        self.smtp_host = self.get_param('config.smtp_host', 'localhost')
        self.smtp_port = self.get_param('config.smtp_port', '25')
        self.mail_from = self.get_param('config.from', None, 'Missing sender email address')
        self.api = TheHiveApi(f"https://{self.https_address}:{self.https_port}", self.api_key)
```
## Features

- Filtering of case data
- Ability to send the generated report to customers 

## Code Example
Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Installation
Provide step by step series of examples and explanations about how to get a development env running.

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests
Describe and show how to run the tests with code examples.

## How to use?
If people like your project they’ll want to learn how they can use it. To do so include step by step guide to use your project.

## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contrbuted in this project. 

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()
