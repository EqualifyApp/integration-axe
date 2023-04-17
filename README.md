# Axe Python Tester 🛡️🐍
Axe Python Tester is a Python-based web accessibility testing tool that uses the powerful [axe-core](https://github.com/dequelabs/axe-core) library to analyze websites and web applications. With this tool, you can quickly identify accessibility issues and get actionable insights to improve the user experience for everyone, including people with disabilities. 🌐♿

[![🏗️📤 Build and publish 🐳 images](https://github.com/EqualifyApp/integration-axe/actions/workflows/containerize.yml/badge.svg)](https://github.com/EqualifyApp/integration-axe/actions/workflows/containerize.yml)

## Overview 🌟

The tool is built with Flask and runs inside a Docker container, making it easy to set up and use in any environment. It comes with everything you need to run accessibility tests, including Google Chrome, ChromeDriver, and the axe-core CLI.

Axe Python Tester is both well-informed and entertaining. You might even say it's a bit like the Sherlock Holmes of web accessibility, with a twist of Monty Python humor. 🔍🐍

## Getting Started 🚀

To get started with Axe Python Tester, follow these simple steps:

_To Work On_

The Flask app will be available at `http://localhost:8083/axe?url=YOUR_URL`, where `YOUR_URL` is the `URL` of the website or web application you'd like to test.

## Configuration ⚙️

You can configure the tool using environment variables in the Dockerfile:

'APP_PORT': The port number on which the Flask app is served. Defaults to 8083.

'PROXY_USERNAME': Your proxy username, if you're using a proxy.

'PROXY_PASSWORD': Your proxy password, if you're using a proxy.

'PROXY_HTTP': The full HTTP proxy URL, including the username and password. This will be used for HTTP requests.

'PROXY_HTTPS': The full HTTPS proxy URL, including the username and password. This will be used for HTTPS requests.

If you don't want to use a proxy, simply comment out or remove the PROXY_HTTP and PROXY_HTTPS environment variables in the Dockerfile.

_TODO_: Auto-detect if docker proxy vars are set and work either way

```
FLASK_APP=axe.py
APP_PORT=8086
PROXY_USERNAME=WhoYouBe?        # Not currently implimented
PROXY_PASSWORD=WhySoSecret?     # Not currently implimented
PROXY_HTTP=http://host:port
PROXY_HTTPS=http://host:port
```

## How It Works 🔎

Axe Python Tester uses the axe-core library to perform accessibility tests. When you send a request to the /axe endpoint with a URL, the tool runs the accessibility tests and returns the results as a JSON object. The results are then transformed based on the header mapping specified in the src/axe.json file, and the transformed response is returned to the client.

**Here is an example of the current transformed response:**

```json
{
"engine_name": "axe-core",
"engine_version": "4.6.3",
"env_orientation_angle": 0,
"env_orientation_type": "landscape-primary",
"env_user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/112.0.5615.49 Safari/537.36",
"env_window_height": 600,
"env_window_width": 800,
"inapplicable": [
    {
        "description": "Ensures every accesskey attribute value is unique",
        "help": "accesskey attribute value should be unique",
        "helpUrl": "https://dequeuniversity.com/rules/axe/4.6/accesskeys?application=webdriverjs",
        "id": "accesskeys",
        "impact": null,
        "nodes": [],
        "tags": [
            "cat.keyboard",
            "best-practice"
        ]
    }
    ],
    "incomplete": [],
    "passes": [
        {
            "description": "Ensures aria-hidden='true' is not present on the document body.",
            "help": "aria-hidden='true' must not be present on the document body",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.6/aria-hidden-body?application=webdriverjs",
            "id": "aria-hidden-body",
            "impact": null,
            "nodes": [
                {
                    "all": [],
                    "any": [
                        {
                            "data": null,
                            "id": "aria-hidden-body",
                            "impact": "critical",
                            "message": "No aria-hidden attribute is present on document body",
                            "relatedNodes": []
                        }
                    ],
                    "html": "<body></body>",
                    "impact": null,
                    "none": [],
                    "target": [
                        "body"
                    ]
                }
            ],
            "tags": [
                "cat.aria",
                "wcag2a",
                "wcag412"
            ]
        }
    ],
    "reporter": "v1",
    "runner_name": "axe",
    "scanned_at": "2023-04-13T22:19:24.878Z",
    "url": "https://exampley.com",
    "violations": [
        {
            "description": "Ensures each HTML document contains a non-empty <title> element",
            "help": "Documents must have <title> element to aid in navigation",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.6/document-title?application=webdriverjs",
            "id": "document-title",
            "impact": "serious",
            "nodes": [
                {
                    "all": [],
                    "any": [
                        {
                            "data": null,
                            "id": "doc-has-title",
                            "impact": "serious",
                            "message": "Document does not have a non-empty <title> element",
                            "relatedNodes": []
                        }
                    ],
                    "failureSummary": "Fix any of the following:\n  Document does not have a non-empty <title> element",
                    "html": "<html class=\"deque-axe-is-ready\"><head></head><body></body><script>document.documentElement.classList.add(\"deque-axe-is-ready\");</script></html>",
                    "impact": "serious",
                    "none": [],
                    "target": [
                        "html"
                    ]
                }
            ],
            "tags": [
                "cat.text-alternatives",
                "wcag2a",
                "wcag242",
                "ACT"
            ]
        },
        {
            "description": "Ensures every HTML document has a lang attribute",
            "help": "<html> element must have a lang attribute",
            "helpUrl": "https://dequeuniversity.com/rules/axe/4.6/html-has-lang?application=webdriverjs",
            "id": "html-has-lang",
            "impact": "serious",
            "nodes": [
                {
                    "all": [],
                    "any": [
                        {
                            "data": {
                                "messageKey": "noLang"
                            },
                            "id": "has-lang",
                            "impact": "serious",
                            "message": "The <html> element does not have a lang attribute",
                            "relatedNodes": []
                        }
                    ],
                    "failureSummary": "Fix any of the following:\n  The <html> element does not have a lang attribute",
                    "html": "<html class=\"deque-axe-is-ready\"><head></head><body></body><script>document.documentElement.classList.add(\"deque-axe-is-ready\");</script></html>",
                    "impact": "serious",
                    "none": [],
                    "target": [
                        "html"
                    ]
                }
            ],
            "tags": [
                "cat.language",
                "wcag2a",
                "wcag311",
                "ACT"
            ]
        }
        ]
        }
```

Now you're all set to start testing your websites and web applications for accessibility issues! Just remember, with great power comes great responsibility. So wield your newfound accessibility testing skills wisely, and make the web a more inclusive place for everyone. 🌍🤗

Happy testing! 🎉

