# Copyright (C) 2015 UCSC Computational Genomics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from toil.job import Job
from toil.test import ToilTest
import logging
from toil.realtimeLogger import RealtimeLogger

class RealtimeLoggerTest(ToilTest):
    def testRealtimeLogger(self):
        options = Job.Runner.getDefaultOptions(self._getTestJobStorePath())
        options.logLevel = "WARNING"
        
        detector = MessageDetector()
        
        # Set up a log message detector
        logging.getLogger().addHandler(detector)
        
        Job.Runner.startToil(LogTest(), options)
        
        # We need the message we're supposed to see
        self.assertTrue(detector.detected)
        # But not the message that shouldn't be logged.
        self.assertFalse(detector.over_logged)
        
class MessageDetector(logging.Handler):
    """
    Detect the secret message and set a flag.
    """
    
    def __init__(self):
        self.detected = False # Have we seen the message we want?
        self.over_logged = False # Have we seen the message we don't want?
        super(MessageDetector, self).__init__()
    
    def emit(self, record):
        if record.msg == "This should be logged at warning level":
            self.detected = True
        if record.msg == "This should be logged at info level":
            self.over_logged = True
            

class LogTest(Job):
    def __init__(self):
        Job.__init__(self,  memory=100000, cores=2, disk="3G")

    def run(self, fileStore):
        RealtimeLogger.info("This should be logged at info level")
        RealtimeLogger.warning("This should be logged at warning level")
        

