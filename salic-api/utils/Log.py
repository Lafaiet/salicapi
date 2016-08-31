# Copyright (c) 2013-2014, RNP (http://www.rnp.br)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# Neither the name of the RNP nor the names of its contributors may be used to
# endorse or promote products derived from this software without specific
# prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

##
# @author:  Bruno Soares, Cleber Alcantara
# @since:  02/04/2015
#

import os
import sys

import logging
import inspect

sys.path.append('../')
from app import app


##
# Log Class provides a unique way to record log messages of this program.
#
class Log():
    logger = None

    ##
    # Creates a new instance of Log class.
    # @param streamType - String containing the stream type name.
    # @param logLevel - String containing the name of the level to be used in the log.
    #
    @classmethod
    def instantiate( cls, streamType = "SCREEN", logLevel = "INFO" ):
        try:
            logging.VERBOSE = 5
            logging.addLevelName(logging.VERBOSE, "VERBOSE")
            logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
            logging.verbose = lambda msg, *args, **kwargs: logging.log(logging.VERBOSE, msg, *args, **kwargs)

            cls.logger = logging.getLogger()

            if logLevel not in logging._levelNames:
                raise Exception( 'Invalid file level' )

            cls.logger.setLevel( logging._levelNames[logLevel] )

            streamType = app.config['STREAMTYPE']

            if streamType == "SCREEN":
                stream = logging.StreamHandler()
            else:
                stream = logging.FileHandler( app.config['LOGFILE'] )

            formatter = logging.Formatter( '[%(levelname)-7s - %(asctime)s] %(message)s' )
            stream.setFormatter( formatter )
            cls.logger.addHandler( stream )
        except Exception, e:
            print( 'Unable to get/set log configurations. Error: %s'%( e ) )
            cls.logger = None


    ##
    # Records a message in a file and/or displays it in the screen.
    # @param level - String containing the name of the log message.
    # @param message - String containing the message to be recorded.
    #
    @classmethod
    def log( cls, level, message, caller = None ):
        if not cls.logger:
            cls.instantiate( logLevel = app.config['LEVELOFLOG'] )

        try:
            if level not in logging._levelNames:
                cls.log( "ERROR", 'Invalid file level \'%s\''%( level ) )

            logLevel = logging._levelNames[level]
            if not caller:
                callers = Log.getCallers( inspect.stack() )
            else:
                callers = caller
            message = '%s.%s - %s'%( callers[0], callers[1] , message )

            cls.logger.log( logLevel, message )
        except Exception, e:
            print 'Unable to record the log. Error: %s'%( e )

    @classmethod
    def info( cls, message ):
        cls.log("INFO", message, Log.getCallers( inspect.stack() ))

    @classmethod
    def error( cls, message ):
        cls.log("ERROR", message, Log.getCallers( inspect.stack() ))

    @classmethod
    def warn( cls, message ):
        cls.log("WARN", message, Log.getCallers( inspect.stack() ))

    @classmethod
    def debug( cls, message ):
        cls.log("DEBUG", message, Log.getCallers( inspect.stack() ))

    @classmethod
    def verbose( cls, message ):
        cls.log("VERBOSE", message, Log.getCallers( inspect.stack() ))

    ##
    # Gets the data about the caller of the log method.
    # @param stack Array containing the system calling stack.
    # @return Array containing the caller class name and the caller method, respectively.
    #
    @staticmethod
    def getCallers( stack ):
        caller_class = None
        caller_method = None
        if stack:
            if len(stack) > 1:
                if stack[1][3] == '<module>':
                    caller_method = stack[1][0].f_locals.get('__name__')
                    caller_class = ((str(stack[1][0].f_locals.get('__file__'))).split('/')[-1]).split('.')[0]
                else:
                    caller_method = stack[1][3]
                    if 'self' in stack[1][0].f_locals:
                        caller_class = stack[1][0].f_locals.get('self').__class__.__name__
                    elif 'cls' in stack[1][0].f_locals:
                        caller_class = stack[1][0].f_locals.get('cls').__name__
                    else:
                        caller_class = 'NoneType'
        return ( caller_class, caller_method )
