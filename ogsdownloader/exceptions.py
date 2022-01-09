#!/usr/bin/env python3
# coding=utf-8

class OGSDownloaderException(Exception):
    pass


class AuthenticationError(OGSDownloaderException):
    pass
