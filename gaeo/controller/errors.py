# -*- coding: utf-8 -*-
#
# Copyright 2008 Lin-Chieh Shangkuan & Liang-Heng Chen
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
#

""" The gaeo controller errors """

class ControllerError(Exception):
    """ Base error class of controllers' errors """

class ControllerInitError(ControllerError):
    pass

class ControllerRenderError(ControllerError):
    """ error occured while render """

class ControllerRenderTypeError(ControllerRenderError):
    """ Render an invalid type """
