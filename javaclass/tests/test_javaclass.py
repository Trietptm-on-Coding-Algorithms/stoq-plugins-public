#!/usr/bin/env python3

#   Copyright 2014-present PUNCH Cyber Analytics Group
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import logging
import asynctest

from pathlib import Path

from stoq import Request, Stoq, Payload
from stoq.data_classes import WorkerResponse
from stoq.exceptions import StoqPluginException


class TestCore(asynctest.TestCase):
    def setUp(self) -> None:
        self.plugin_name = 'javaclass'
        self.base_dir = Path(os.path.realpath(__file__)).parent
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.plugin_dir = os.path.join(self.base_dir.parent, self.plugin_name)

    def tearDown(self) -> None:
        pass

    async def test_scan(self) -> None:
        s = Stoq(plugin_dir_list=[self.plugin_dir])
        plugin = s.load_plugin(self.plugin_name)
        with open(f'{self.data_dir}/TestJavaClass.class', 'rb') as f:
            payload = Payload(f.read())
        response = await plugin.scan(payload, Request())
        self.assertIsInstance(response, WorkerResponse)
        self.assertIn('TestJavaClass', response.results['provided'])
        self.assertGreaterEqual(len(response.results['provided']), 4)
        self.assertGreaterEqual(len(response.results['required']), 2)
        self.assertGreaterEqual(len(response.results['constants']), 10)

    async def test_scan_invalid_payload(self) -> None:
        s = Stoq(plugin_dir_list=[self.plugin_dir])
        plugin = s.load_plugin(self.plugin_name)
        payload = Payload(b'definitely not a javaclass payload')
        with self.assertRaises(StoqPluginException):
            response = await plugin.scan(payload, Request())
