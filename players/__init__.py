#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

import os
import re
import uuid
import json
import hashlib

PROMPT = "{hp}/{max_hp} hp|{sp}/{max_sp} sp|{mp}/{max_mp} mp"

def hash_password(passwd):
    hasher = hashlib.md5()
    hasher.update(passwd)
    return hasher.hexdigest()

validate_email_pattern = re.compile(r'[\.\w]{1,}[@]\w+[.]\w+')
def validate_email(email):
    if not validate_email_pattern.match(email): return False
    return True

class PlayerInteractions(object):
    def init(self):
        # require password upon return
        if self.uuid: 
            self.client.prompt("Please enter your password: ", self.enter_password)
            return
        # require password verification upon creation
        def confirm(response):
            if not response or response.lower() == 'y':
                self.client.prompt("Please enter a password: ", self.create)
            else:
                self.client.prompt("Please enter your name: ", self.client.connect)
        # being character creation
        self.client.prompt("Character not found. Would you like to create the character '%s'? [Y/n]: " %
            self.name, confirm)

    def enter_password(self, password):
        # determine current attempts
        self._enter_password_attempt = getattr(self, '_enter_password_attempt', 0) + 1
        # disconnect on maximum attempts
        if self._enter_password_attempt > 3:
            self.client.write("Maximum password attempts. Disconnecting...")
            self.client.close()
            return
        # verify player password
        if hash_password(self.uuid + password) != self.password:
            self.client.prompt("Incorrect password. Please enter your password: ", self.enter_password)
            return
        # save player
        self.player.save()
        # authenticate player
        self.auth("Welcome back!")

    def create(self, password):
        # require password
        if not password:
            # determine current attempts
            self._create_attempt = getattr(self, '_create_attempt', 0) + 1
            # disconnect on maximum attempts
            if self._create_attempt > 3:
                self.client.write("Maximum creation attempts. Disconnecting...")
                self.client.close()
                return
            # prompt for required password
            self.client.prompt("A password required. Please enter a password: ", self.create)
            return
        # set player uuid
        self.uuid = str(uuid.uuid4())
        # set password
        self.password = hash_password(self.uuid + password)
        # verify password
        self.client.prompt("Please verify your password: ", self.verify_password)

    def verify_password(self, password):
        # require password
        if not password:
            # determine current attempts
            self._verify_password_attempt = getattr(self, '_verify_password_attempt', 0) + 1
            # disconnect on maximum attempts
            if self._verify_password_attempt > 2:
                self.client.write("Maximum password verification attempts. Disconnecting...")
                self.client.close()
                return
            # reset verification attempts
            self._verify_password = 0
            self.client.prompt("Password verification required. Please verify your password: ", self.verify_password)
            return
        # reset verification attempts
        self._verify_password_attempt = 0
        # verify player password
        if hash_password(self.uuid + password) != self.password:
            # determine current verification attempt
            self._verify_password = getattr(self, '_verify_password', 0) + 1
            # disconnect on maximum attempts
            if self._verify_password > 3:
                self.client.write("Maximum password verification attempts. Disconnecting...")
                self.client.close()
                return
            self.client.prompt("Passwords do not match. Please verify your password: ", self.verify_password)
            return
        # enter player email
        self.client.prompt("Please enter your email address for password retrieval: ", self.enter_email)

    def enter_email(self, email):
        # require email
        if not validate_email(email):
            # determine current attempts
            self._enter_email_attempt = getattr(self, '_enter_email_attempt', 0) + 1
            # disconnect on maximum attempts
            if self._enter_email_attempt > 3:
                self.client.write("Maximum email verification attempts. Disconnecting...")
                self.client.close()
                return
            # prompt for required email
            self.client.prompt("A valid email address required. Please enter a valid email address: ", self.enter_email)
            return
        # set email
        self.email = email
        # verify email
        self.client.prompt("Please verify your email address: ", self.verify_email)

    def verify_email(self, email):
        # require email
        if not validate_email(email):
            # determine current attempts
            self._verify_email_attempt = getattr(self, '_verify_email_attempt', 0) + 1
            # disconnect on maximum attempts
            if self._verify_email_attempt > 2:
                self.client.write("Maximum email address verification attempts. Disconnecting...")
                self.client.close()
                return
            # reset verification attempts
            self._verify_email = 0
            self.client.prompt("A valid email address is required for verificationEmail address. Please verify a valid email address: ", self.verify_email)
            return
        # reset verification attempts
        self._verify_email_attempt = 0
        # verify player email
        if email != self.email:
            # determine current verification attempt
            self._verify_email = getattr(self, '_verify_email', 0) + 1
            # disconnect on maximum attempts
            if self._verify_email > 3:
                self.client.write("Maximum email address verification attempts. Disconnecting...")
                self.client.close()
                return
            self.client.prompt("Email addresses do not match. Please verify your email: ", self.verify_email)
            return
        # save player
        self.save()
        # authenticate player
        self.auth("Welcome. Please enjoy the MUD!")

    def auth(self, msg=None):
        self.authed = True
        if msg: self.client.write(msg)

class Player(PlayerInteractions):
    def __init__(self, client, name):
        # define instance defaults
        self.uuid = 0
        self.admin  = False
        self.authed = False
        # assign instance properties
        self.client   = client
        self.name     = name
        self.email    = ''
        self.password = ''
        # load character data
        self.load()

    @property
    def max_hp(self):
        return 2500
    @property
    def max_sp(self):
        return 1000
    @property
    def max_mp(self):
        return 2000

    @property
    def prompt(self):
        import random
        prompt = getattr(self, 'PROMPT', PROMPT)
        return "%s > " % prompt.format(
            hp=random.randint(1, self.max_hp), max_hp=self.max_hp,
            sp=random.randint(1, self.max_sp), max_sp=self.max_sp,
            mp=random.randint(1, self.max_mp), max_mp=self.max_mp
        )
    @prompt.setter
    def prompt(self, prompt):
        self.PROMPT = prompt

    def load(self):
        try:
            with open('players/%s.json' % self.name, 'r') as f:
                data = json.load(f)
        except IOError:
            return
        # decode data
        for key, val in data.items():
            setattr(self, key, val)

    def save(self, msg=None):
        data = {
            'PROMPT': self.prompt,
            'uuid': self.uuid,
            'admin': self.admin,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
        with open('players/%s.json' % self.name, 'w') as f:
            json.dump(data, f)
        if msg: self.client.write(msg)
