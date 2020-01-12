## Reporter
This project is a responder designed to take case data, observables and tasks from TheHive, and transform them into a user-defined report based on a Jinja template.  

## Motivation
This project is part of a bachelor-project, which attempts to create an "easy-to-run" Security Operations Center (SOC). This module is inteded for anyone who needs a report generated from an individual case, and send it to customers via E-mail.
 
## Screenshots
Example of data filters: 
```

        self.case_data_filter = ["endDate", "startDate", "title", "createdAt", "caseId", "pap", "tlp", "severity",
                                 "owner", "createdBy", "updatedBy", "summary", "tags", "resolutionStatus",
                                 "impactStatus", "status", "customFields"]
                                 
        self.case_observables_filter = ["data", "dataType", "sighted", "tags", "createdAt",
                    "createdBy", "pap", "tlp", "ioc", "startDate", "status"]
                    
        self.case_tasks_filter = ["caseTasks", "updatedBy", "createdAt", "flag", "description",
              "title", "createdBy", "updatedAt", "order", "status", "group"]
```
## Features

- Filtering of case data
- Ability to send the generated report to customers 


## Installation

# If Cortex is already installed

1. Find responder folder at: 

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
