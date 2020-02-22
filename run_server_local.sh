#!/usr/bin/env bash
dotenv poetry  run uvicorn --reload app.main:app
