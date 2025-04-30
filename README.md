# MultiManage

<img src="images/MultiManage-Logo.ico" width="20%">

A platform agnostic WebUI to manage Multipass. Making changes as PySimpleGUI went commercial.

This book will be the inspiration: https://www.manning.com/books/build-financial-software-with-generative-ai-from-scratch

Will hopefully begin a program to manage VMs in a web browser. Would be usable on a headless server (maybe links) or remotely, and so allow a machine to be a remote Multipass Server, which would be cool. Hoping to seperate the various Multipass calls into functions, and can then also build a TUI program around it for anyone who wants a single binary option. But need to see how easy this is first. 

Based on these technologies;
 - Docker (to host webapp and FastAPI)
 - Multipass (VM Engine)
 - FastAPI (API)
 - Next.js (WebUI)
 - Swagger
 - Postman
 - Potentially an MCP component for LLMs
