#!/usr/bin/env python3

###############################################################################
#                                                                             #
# RMG - Reaction Mechanism Generator                                          #
#                                                                             #
# Copyright (c) 2002-2019 Prof. William H. Green (whgreen@mit.edu),           #
# Prof. Richard H. West (r.west@neu.edu) and the RMG Team (rmg_dev@mit.edu)   #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the 'Software'),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
#                                                                             #
###############################################################################

"""
This module contains unit tests of the :mod:`arkane.ess.terachem` module.
"""

import os
import unittest

import numpy as np

from rmgpy.statmech.conformer import Conformer

from arkane.exceptions import LogError
from arkane.ess.terachem import TeraChemLog

################################################################################


class TeraChemLogTest(unittest.TestCase):
    """
    Contains unit tests for the terachem module, used for parsing TeraChem files.
    """
    @classmethod
    def setUpClass(cls):
        """
        A method that is run before all unit tests in this class.
        """
        cls.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'terachem')

    def test_get_number_of_atoms(self):
        """Uses various TeraChem log files to test that number of atoms can be properly read."""
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethane_minimize_output.out'))
        self.assertEqual(log_file.get_number_of_atoms(), 6)
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethane_coords.xyz'))
        self.assertEqual(log_file.get_number_of_atoms(), 6)
        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_coords.xyz'))
        self.assertEqual(log_file.get_number_of_atoms(), 4)
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethane_output.geometry'))
        self.assertEqual(log_file.get_number_of_atoms(), 6)
        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_output.geometry'))
        self.assertEqual(log_file.get_number_of_atoms(), 4)

    def test_load_force_constant_matrix(self):
        """Test loading the Hessian"""
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethanol_freq_output.out'))
        hessian = log_file.load_force_constant_matrix()
        self.assertEqual(len(hessian), 27)  # 9 atoms * 3 dof = 27
        self.assertEqual(len(hessian[0]), 27)

        log_file = TeraChemLog(os.path.join(self.data_path, 'ethylamine_freq_output.out'))
        hessian = log_file.load_force_constant_matrix()
        expected_hessian = [
            [914.9859609920952, -86.71893487707963, 25.53304366219221, -229.64170366910673, 9.65273601863364,
             122.37178242977485, -2.4910286499699716, 0.6227571624924929, 14.323414737327337, -42.347487049489516,
             -13.389278993588597, 43.90437995572075, -0.7784464531156161, -3.7365429749549572, 1.8682714874774786,
             -0.6227571624924929, -0.15568929062312323, -1.8682714874774786, 3.1137858124624644, -0.46706787186936966,
             -0.15568929062312323, 2.802407231216218, 0.6227571624924929, -0.31137858124624646, -99.64114599879886,
             27.40131514966969, 10.742561052995502, -545.6909636340469, 67.10208425856611, -216.40811396614131],
            [-86.71893487707963, 853.1773126147153, -244.12080769705722, -20.395297071629145, -150.7072333231833,
             73.7967237553604, 16.035996934181693, 13.389278993588597, -12.61083254047298, 9.808425309256764,
             4.982057299939943, -11.521007506111118, -41.5690405963739, -9.497046728010517, 43.74869066509763,
             0.7784464531156161, 3.1137858124624644, 0.6227571624924929, -0.6227571624924929, -0.6227571624924929,
             1.0898250343618625, -0.0, -0.46706787186936966, -6.227571624924929, 2.9580965218393414, -620.7332017143923,
             60.09606618052557, 119.72506448918175, -94.5033994082358, 95.28184586135141],
            [25.53304366219221, -244.12080769705722, 432.81622793228263, 54.95831958996249, 23.820461465337853,
             -210.49192092246258, 48.88643725566069, 14.167725446704214, -49.04212654628382, -1.5568929062312322,
             -2.9580965218393414, 11.676696796734241, 16.81444338729731, 9.808425309256764, -15.724618352935446,
             -0.6227571624924929, 0.9341357437387393, 4.82636800931682, 0.31137858124624646, 2.179650068723725,
             4.982057299939943, -0.7784464531156161, -6.850328787417422, -11.988075377980488, 11.365318215487996,
             143.23414737327337, -40.94628343388141, -155.06653346063072, 59.784687599279316, -126.88677185784543],
            [-229.64170366910673, -20.395297071629145, 54.95831958996249, 880.2672491831387, -45.92834073382135,
             71.77276297725982, -131.55745057653914, -13.54496828421172, -26.311490115307823, -390.1573623015468,
             81.1141204146472, -143.3898366638965, -84.38359551773279, 16.50306480605106, -4.35930013744745,
             -0.6227571624924929, 0.6227571624924929, 3.7365429749549572, -7.4730859499099145, -26.62286869655407,
             -44.838515699459485, 4.35930013744745, 20.550986362252267, 34.563022518333355, 2.3353393593468486,
             0.6227571624924929, 4.514989428070574, -42.970244211982006, -12.14376466860361, 49.04212654628382],
            [9.65273601863364, -150.7072333231833, 23.820461465337853, -45.92834073382135, 917.1656110608188,
             -66.63501638669673, -16.191686224804815, -175.15045195101362, -61.80864837737992, 74.57517020847602,
             -101.50941748627633, 38.455254783911435, 25.377354371569083, -464.4211539287766, 50.59901945251505,
             -8.874289565518025, -26.1558008246847, -47.95230151192195, 0.46706787186936966, 6.383260915548052,
             10.275493181126134, 3.7365429749549572, 7.7844645311561615, 17.4372005497898, -48.73074796503757,
             -17.125821968543555, 47.64092293067571, 5.449125171809313, 4.047921556201204, -11.521007506111118],
            [122.37178242977485, 73.7967237553604, -210.49192092246258, 71.77276297725982, -66.63501638669673,
             700.1347399321851, -33.00612961210212, -67.41346283981235, -223.8811999160512, -132.95865419214724,
             37.209740458926454, -132.80296490152412, -7.317396659286792, 58.383483983671205, -85.1620419708484,
             2.179650068723725, 3.2694751030855875, 6.071882334301805, -2.802407231216218, -11.209628924864871,
             -20.706675652875386, -3.8922322655780808, -11.521007506111118, -23.353393593468482, 7.628775240533038,
             -6.850328787417422, -19.616850618513528, -22.73063643097599, -9.65273601863364, 9.808425309256764],
            [-2.4910286499699716, 16.035996934181693, 48.88643725566069, -131.55745057653914, -16.191686224804815,
             -33.00612961210212, 886.3391315174406, -7.4730859499099145, -21.796500687237252, -4.35930013744745,
             -24.910286499699716, -42.03610846824327, 1.7125821968543555, 2.6467179405930947, 2.3353393593468486,
             -78.62309176467723, 21.329432815367884, -2.179650068723725, -394.04959456712487, 80.49136325215471,
             -137.00657574834844, -278.68383021539057, -74.57517020847602, 184.64749867902415, 0.15568929062312323,
             1.8682714874774786, -2.3353393593468486, 2.6467179405930947, 1.0898250343618625, 2.4910286499699716],
            [0.6227571624924929, 13.389278993588597, 14.167725446704214, -13.54496828421172, -175.15045195101362,
             -67.41346283981235, -7.4730859499099145, 850.219216092876, -70.37155936165169, 1.2455143249849858,
             5.916193043678683, 9.341357437387394, -8.7186002748949, -25.065975790322838, -46.86247647756009,
             22.1078792684835, -467.22356115999276, 54.17987313684688, 78.77878105530036, -95.9046030238439,
             38.76663336515768, -74.41948091785291, -107.42561052995504, 66.79070567731986, 0.46706787186936966,
             3.2694751030855875, 2.802407231216218, 0.6227571624924929, -1.2455143249849858, -0.9341357437387393],
            [14.323414737327337, -12.61083254047298, -49.04212654628382, -26.311490115307823, -61.80864837737992,
             -223.8811999160512, -21.796500687237252, -70.37155936165169, 750.2666915128308, -6.538950206171175,
             -13.389278993588597, -20.083918490382896, -0.9341357437387393, 0.46706787186936966, 5.916193043678683,
             -3.1137858124624644, 55.26969817120874, -86.09617771458714, -138.40777936395656, 37.98818691204207,
             -132.33589702965475, 185.27025584151662, 66.32363780545049, -249.72562215948963, -0.46706787186936966,
             -1.7125821968543555, 1.8682714874774786, -1.8682714874774786, 1.2455143249849858, 3.580853684331834],
            [-42.347487049489516, 9.808425309256764, -1.5568929062312322, -390.1573623015468, 74.57517020847602,
             -132.95865419214724, -4.35930013744745, 1.2455143249849858, -6.538950206171175, 437.17552806973,
             -82.82670261150155, 139.34191510769529, 0.31137858124624646, 2.802407231216218, -1.0898250343618625,
             0.15568929062312323, -0.46706787186936966, 0.46706787186936966, 1.8682714874774786, -0.6227571624924929,
             -0.7784464531156161, 0.46706787186936966, -0.15568929062312323, -0.9341357437387393, 0.15568929062312323,
             -0.46706787186936966, -1.2455143249849858, -3.580853684331834, -4.514989428070574, 5.2934358811861895],
            [-13.389278993588597, 4.982057299939943, -2.9580965218393414, 81.1141204146472, -101.50941748627633,
             37.209740458926454, -24.910286499699716, 5.916193043678683, -13.389278993588597, -82.82670261150155,
             97.46149593007515, -36.58698329643396, 46.239719315067596, -9.18566814676427, 18.83840416539791,
             -0.46706787186936966, 1.401203615608109, 1.5568929062312322, -1.5568929062312322, -1.2455143249849858,
             -5.449125171809313, 0.6227571624924929, 0.7784464531156161, 0.7784464531156161, -0.46706787186936966,
             0.6227571624924929, -1.401203615608109, -4.047921556201204, 0.9341357437387393, 1.0898250343618625],
            [43.90437995572075, -11.521007506111118, 11.676696796734241, -143.3898366638965, 38.455254783911435,
             -132.80296490152412, -42.03610846824327, 9.341357437387394, -20.083918490382896, 139.34191510769529,
             -36.58698329643396, 150.39585474193703, -7.006018078040545, 1.7125821968543555, -2.6467179405930947,
             0.9341357437387393, 0.15568929062312323, 2.3353393593468486, -0.46706787186936966, -5.760503753055559,
             -7.4730859499099145, 0.46706787186936966, 0.7784464531156161, 1.5568929062312322, -0.6227571624924929,
             -0.0, 1.2455143249849858, 8.25153240302553, 3.2694751030855875, -4.047921556201204],
            [-0.7784464531156161, -41.5690405963739, 16.81444338729731, -84.38359551773279, 25.377354371569083,
             -7.317396659286792, 1.7125821968543555, -8.7186002748949, -0.9341357437387393, 0.31137858124624646,
             46.239719315067596, -7.006018078040545, 85.47342055209465, -14.323414737327337, -4.982057299939943,
             1.401203615608109, -1.5568929062312322, -0.9341357437387393, 0.31137858124624646, -0.46706787186936966,
             1.2455143249849858, 0.31137858124624646, 0.31137858124624646, -0.31137858124624646, -5.760503753055559,
             -4.35930013744745, 5.2934358811861895, 1.2455143249849858, -1.0898250343618625, -1.8682714874774786],
            [-3.7365429749549572, -9.497046728010517, 9.808425309256764, 16.50306480605106, -464.4211539287766,
             58.383483983671205, 2.6467179405930947, -25.065975790322838, 0.46706787186936966, 2.802407231216218,
             -9.18566814676427, 1.7125821968543555, -14.323414737327337, 503.8105444564267, -65.54519135233488,
             -0.7784464531156161, -0.15568929062312323, -5.137746590563067, -0.6227571624924929, 1.2455143249849858,
             0.46706787186936966, 0.31137858124624646, 0.7784464531156161, -0.15568929062312323, -2.4910286499699716,
             2.4910286499699716, 0.31137858124624646, -0.15568929062312323, 0.15568929062312323, -0.6227571624924929],
            [1.8682714874774786, 43.74869066509763, -15.724618352935446, -4.35930013744745, 50.59901945251505,
             -85.1620419708484, 2.3353393593468486, -46.86247647756009, 5.916193043678683, -1.0898250343618625,
             18.83840416539791, -2.6467179405930947, -4.982057299939943, -65.54519135233488, 103.84475684562318,
             -1.5568929062312322, -5.2934358811861895, -8.25153240302553, 0.15568929062312323, 1.401203615608109,
             2.023960778100602, 0.15568929062312323, 1.5568929062312322, 2.3353393593468486, 7.7844645311561615,
             2.179650068723725, -3.580853684331834, -0.31137858124624646, -0.6227571624924929, 1.0898250343618625],
            [-0.6227571624924929, 0.7784464531156161, -0.6227571624924929, -0.6227571624924929, -8.874289565518025,
             2.179650068723725, -78.62309176467723, 22.1078792684835, -3.1137858124624644, 0.15568929062312323,
             -0.46706787186936966, 0.9341357437387393, 1.401203615608109, -0.7784464531156161, -1.5568929062312322,
             75.50930595221476, -22.73063643097599, 4.514989428070574, -0.9341357437387393, 47.018165768183216,
             -6.071882334301805, 2.802407231216218, -37.67680833079582, 3.425164393708711, 0.6227571624924929,
             0.15568929062312323, 0.6227571624924929, 0.0, 0.31137858124624646, 0.0],
            [-0.15568929062312323, 3.1137858124624644, 0.9341357437387393, 0.6227571624924929, -26.1558008246847,
             3.2694751030855875, 21.329432815367884, -467.22356115999276, 55.26969817120874, -0.46706787186936966,
             1.401203615608109, 0.15568929062312323, -1.5568929062312322, -0.15568929062312323, -5.2934358811861895,
             -22.73063643097599, 508.4812231751205, -57.760726821178714, 1.2455143249849858, -9.18566814676427,
             2.023960778100602, 0.31137858124624646, -11.05393963424175, 2.179650068723725, 1.0898250343618625,
             0.6227571624924929, -1.0898250343618625, 0.31137858124624646, -0.0, 0.15568929062312323],
            [-1.8682714874774786, 0.6227571624924929, 4.82636800931682, 3.7365429749549572, -47.95230151192195,
             6.071882334301805, -2.179650068723725, 54.17987313684688, -86.09617771458714, 0.46706787186936966,
             1.5568929062312322, 2.3353393593468486, -0.9341357437387393, -5.137746590563067, -8.25153240302553,
             4.514989428070574, -57.760726821178714, 89.8327206895421, 0.46706787186936966, 19.77253990913665,
             -3.7365429749549572, -4.670678718693697, 33.31750819334837, -4.514989428070574, 0.31137858124624646,
             1.401203615608109, -0.31137858124624646, 0.31137858124624646, -0.15568929062312323, -0.15568929062312323],
            [3.1137858124624644, -0.6227571624924929, 0.31137858124624646, -7.4730859499099145, 0.46706787186936966,
             -2.802407231216218, -394.04959456712487, 78.77878105530036, -138.40777936395656, 1.8682714874774786,
             -1.5568929062312322, -0.46706787186936966, 0.31137858124624646, -0.6227571624924929, 0.15568929062312323,
             -0.9341357437387393, 1.2455143249849858, 0.46706787186936966, 426.4329670167345, -87.18600274894901,
             155.37791204187698, -30.670790252755275, 8.7186002748949, -14.167725446704214, 0.15568929062312323,
             0.31137858124624646, 0.15568929062312323, 0.7784464531156161, 0.31137858124624646, -0.6227571624924929],
            [-0.46706787186936966, -0.6227571624924929, 2.179650068723725, -26.62286869655407, 6.383260915548052,
             -11.209628924864871, 80.49136325215471, -95.9046030238439, 37.98818691204207, -0.6227571624924929,
             -1.2455143249849858, -5.760503753055559, -0.46706787186936966, 1.2455143249849858, 1.401203615608109,
             47.018165768183216, -9.18566814676427, 19.77253990913665, -87.18600274894901, 96.06029231446702,
             -37.67680833079582, -13.07790041234235, 2.179650068723725, -7.161707368663668, 0.31137858124624646,
             0.15568929062312323, -0.15568929062312323, 0.9341357437387393, 0.6227571624924929, 0.46706787186936966],
            [-0.15568929062312323, 1.0898250343618625, 4.982057299939943, -44.838515699459485, 10.275493181126134,
             -20.706675652875386, -137.00657574834844, 38.76663336515768, -132.33589702965475, -0.7784464531156161,
             -5.449125171809313, -7.4730859499099145, 1.2455143249849858, 0.46706787186936966, 2.023960778100602,
             -6.071882334301805, 2.023960778100602, -3.7365429749549572, 155.37791204187698, -37.67680833079582,
             143.23414737327337, 30.048033090262784, -9.497046728010517, 15.724618352935446, -0.15568929062312323,
             0.31137858124624646, -0.31137858124624646, 1.8682714874774786, -0.46706787186936966, -1.7125821968543555],
            [2.802407231216218, -0.0, -0.7784464531156161, 4.35930013744745, 3.7365429749549572, -3.8922322655780808,
             -278.68383021539057, -74.41948091785291, 185.27025584151662, 0.46706787186936966, 0.6227571624924929,
             0.46706787186936966, 0.31137858124624646, 0.31137858124624646, 0.15568929062312323, 2.802407231216218,
             0.31137858124624646, -4.670678718693697, -30.670790252755275, -13.07790041234235, 30.048033090262784,
             297.67792367141163, 82.98239190212468, -205.50986362252266, 0.0, -0.15568929062312323,
             -0.15568929062312323, 0.7784464531156161, -0.6227571624924929, -0.9341357437387393],
            [0.6227571624924929, -0.46706787186936966, -6.850328787417422, 20.550986362252267, 7.7844645311561615,
             -11.521007506111118, -74.57517020847602, -107.42561052995504, 66.32363780545049, -0.15568929062312323,
             0.7784464531156161, 0.7784464531156161, 0.31137858124624646, 0.7784464531156161, 1.5568929062312322,
             -37.67680833079582, -11.05393963424175, 33.31750819334837, 8.7186002748949, 2.179650068723725,
             -9.497046728010517, 82.98239190212468, 107.58129982057814, -73.32965588349104, 0.0, -0.15568929062312323,
             -1.0898250343618625, -0.7784464531156161, 0.0, 0.31137858124624646],
            [-0.31137858124624646, -6.227571624924929, -11.988075377980488, 34.563022518333355, 17.4372005497898,
             -23.353393593468482, 184.64749867902415, 66.79070567731986, -249.72562215948963, -0.9341357437387393,
             0.7784464531156161, 1.5568929062312322, -0.31137858124624646, -0.15568929062312323, 2.3353393593468486,
             3.425164393708711, 2.179650068723725, -4.514989428070574, -14.167725446704214, -7.161707368663668,
             15.724618352935446, -205.50986362252266, -73.32965588349104, 268.40833703426443, -0.6227571624924929,
             -0.6227571624924929, 1.2455143249849858, -0.7784464531156161, 0.0, 0.31137858124624646],
            [-99.64114599879886, 2.9580965218393414, 11.365318215487996, 2.3353393593468486, -48.73074796503757,
             7.628775240533038, 0.15568929062312323, 0.46706787186936966, -0.46706787186936966, 0.15568929062312323,
             -0.46706787186936966, -0.6227571624924929, -5.760503753055559, -2.4910286499699716, 7.7844645311561615,
             0.6227571624924929, 1.0898250343618625, 0.31137858124624646, 0.15568929062312323, 0.31137858124624646,
             -0.15568929062312323, 0.0, 0.0, -0.6227571624924929, 103.06631039250756, -18.83840416539791,
             -13.389278993588597, -0.9341357437387393, 65.38950206171175, -11.676696796734241],
            [27.40131514966969, -620.7332017143923, 143.23414737327337, 0.6227571624924929, -17.125821968543555,
             -6.850328787417422, 1.8682714874774786, 3.2694751030855875, -1.7125821968543555, -0.46706787186936966,
             0.6227571624924929, -0.0, -4.35930013744745, 2.4910286499699716, 2.179650068723725, 0.15568929062312323,
             0.6227571624924929, 1.401203615608109, 0.31137858124624646, 0.15568929062312323, 0.31137858124624646,
             -0.15568929062312323, -0.15568929062312323, -0.6227571624924929, -18.83840416539791, 647.5117597015695,
             -131.86882915778537, -6.383260915548052, -14.946171899819829, -6.227571624924929],
            [10.742561052995502, 60.09606618052557, -40.94628343388141, 4.514989428070574, 47.64092293067571,
             -19.616850618513528, -2.3353393593468486, 2.802407231216218, 1.8682714874774786, -1.2455143249849858,
             -1.401203615608109, 1.2455143249849858, 5.2934358811861895, 0.31137858124624646, -3.580853684331834,
             0.6227571624924929, -1.0898250343618625, -0.31137858124624646, 0.15568929062312323, -0.15568929062312323,
             -0.31137858124624646, -0.15568929062312323, -1.0898250343618625, 1.2455143249849858, -13.389278993588597,
             -131.86882915778537, 68.03622000230486, -4.047921556201204, 24.754597209076593, -7.628775240533038],
            [-545.6909636340469, 119.72506448918175, -155.06653346063072, -42.970244211982006, 5.449125171809313,
             -22.73063643097599, 2.6467179405930947, 0.6227571624924929, -1.8682714874774786, -3.580853684331834,
             -4.047921556201204, 8.25153240302553, 1.2455143249849858, -0.15568929062312323, -0.31137858124624646, 0.0,
             0.31137858124624646, 0.31137858124624646, 0.7784464531156161, 0.9341357437387393, 1.8682714874774786,
             0.7784464531156161, -0.7784464531156161, -0.7784464531156161, -0.9341357437387393, -6.383260915548052,
             -4.047921556201204, 587.8827613929133, -116.14421080484992, 174.68338407914425],
            [67.10208425856611, -94.5033994082358, 59.784687599279316, -12.14376466860361, 4.047921556201204,
             -9.65273601863364, 1.0898250343618625, -1.2455143249849858, 1.2455143249849858, -4.514989428070574,
             0.9341357437387393, 3.2694751030855875, -1.0898250343618625, 0.15568929062312323, -0.6227571624924929,
             0.31137858124624646, -0.0, -0.15568929062312323, 0.31137858124624646, 0.6227571624924929,
             -0.46706787186936966, -0.6227571624924929, 0.0, 0.0, 65.38950206171175, -14.946171899819829,
             24.754597209076593, -116.14421080484992, 105.09027117060819, -78.15602389280787],
            [-216.40811396614131, 95.28184586135141, -126.88677185784543, 49.04212654628382, -11.521007506111118,
             9.808425309256764, 2.4910286499699716, -0.9341357437387393, 3.580853684331834, 5.2934358811861895,
             1.0898250343618625, -4.047921556201204, -1.8682714874774786, -0.6227571624924929, 1.0898250343618625, 0.0,
             0.15568929062312323, -0.15568929062312323, -0.6227571624924929, 0.46706787186936966, -1.7125821968543555,
             -0.9341357437387393, 0.31137858124624646, 0.31137858124624646, -11.676696796734241, -6.227571624924929,
             -7.628775240533038, 174.68338407914425, -78.15602389280787, 125.95263611410668]]
        np.testing.assert_almost_equal(hessian, np.array(expected_hessian, np.float64))

    def test_load_geometry(self):
        """Test loading the geometry from a TeraChem xyz output file"""
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethane_coords.xyz'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[0.66409651, 0.00395265, 0.07100793],
                              [-0.66409647, -0.00395253, -0.0710079],
                              [1.24675866, 0.88983869, -0.1613784],
                              [1.19483972, -0.8753068, 0.42244414],
                              [-1.19483975, 0.87530673, -0.42244421],
                              [-1.24675868, -0.88983873, 0.16137844]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([6, 6, 1, 1, 1, 1], np.float64))
        np.testing.assert_almost_equal(masses, np.array(
            [12., 12., 1.00782503, 1.00782503, 1.00782503, 1.00782503], np.float64))

        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_coords.xyz'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[-4.23756410e-03, 4.24348000e-05, -5.28516700e-04],
                              [1.19165823e+00, -1.75471911e-02, 1.58030931e-01],
                              [-5.96146428e-01, 9.38505681e-01, 4.33255558e-02],
                              [-5.91274235e-01, -9.21000915e-01, -2.00827970e-01]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([6, 8, 1, 1], np.float64))
        np.testing.assert_almost_equal(
            masses, np.array([12., 15.99491462, 1.00782503, 1.00782503], np.float64))

        log_file = TeraChemLog(os.path.join(self.data_path, 'ethane_output.geometry'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[0.66409651, 0.00395265, 0.07100793],
                              [-0.66409647, -0.00395253, -0.0710079],
                              [1.24675866, 0.88983869, -0.1613784],
                              [1.19483972, -0.8753068, 0.42244414],
                              [-1.19483975, 0.87530673, -0.42244421],
                              [-1.24675868, -0.88983873, 0.16137844]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([6, 6, 1, 1, 1, 1], np.float64))
        np.testing.assert_almost_equal(
            masses, np.array([12., 12., 1.00782504, 1.00782504, 1.00782504, 1.00782504], np.float64))

        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_output.geometry'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[-1.2224100e-02, 1.8041000e-04, -1.6211600e-03],
                              [1.2016482e+00, -1.7734170e-02, 1.5936241e-01],
                              [-5.9716440e-01, 9.3272817e-01, 4.2440100e-02],
                              [-5.9225970e-01, -9.1517440e-01, -2.0018135e-01]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([6, 8, 1, 1], np.float64))
        np.testing.assert_almost_equal(
            masses, np.array([12., 15.99491464, 1.00782504, 1.00782504], np.float64))

        log_file = TeraChemLog(os.path.join(self.data_path, 'ethylamine_freq_output.out'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[2.370236, 0.065481, -1.194536],
                              [0.512276, -0.516064, 0.779232],
                              [0.859257, 0.87292, 3.300986],
                              [-1.367578, -0.100279, 0.008089],
                              [0.56292, -2.564216, 1.100445],
                              [0.755566, 2.927958, 3.038153],
                              [2.705598, 0.43874, 4.141338],
                              [-0.600934, 0.336582, 4.672435],
                              [2.352825, 1.959707, -1.552162],
                              [4.141389, -0.322693, -0.540207]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([7, 6, 6, 1, 1, 1, 1, 1, 1, 1], np.float64))
        np.testing.assert_almost_equal(
            masses, np.array([14.003074, 12., 12., 1.00782503, 1.00782503, 1.00782503, 1.00782503,
                              1.00782503, 1.00782503, 1.00782503], np.float64))

        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_freq_output.out'))
        coords, numbers, masses = log_file.load_geometry()
        np.testing.assert_almost_equal(
            coords, np.array([[2.261989e+00, -1.149050e-01, 1.783170e-01],
                              [-8.108000e-03, 2.710000e-04, -6.880000e-04],
                              [-1.038653e+00, 1.827038e+00, -6.398200e-02],
                              [-1.215229e+00, -1.712404e+00, -1.136470e-01]], np.float64))
        np.testing.assert_almost_equal(numbers, np.array([8, 6, 1, 1], np.float64))
        np.testing.assert_almost_equal(
            masses, np.array([15.99491462, 12., 1.00782503, 1.00782503], np.float64))

    def test_load_conformer(self):
        """
        Test parsing frequencies and spin multiplicity from a TeraChem log file.
        Translation and rotation modes are not read from the TeraCHem log, and are instead added in statmech.
        """
        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_freq_output.out'))
        conformer, unscaled_freqs = log_file.load_conformer()
        self.assertIsInstance(conformer, Conformer)
        self.assertEqual(len(conformer.modes), 1)
        np.testing.assert_almost_equal(conformer.modes[0].frequencies.value_si, unscaled_freqs)
        expected_freqs = [1198.6352081, 1276.1991058, 1563.6275932, 1893.2440765,
                          2916.3917533, 2965.8683956]
        np.testing.assert_almost_equal(conformer.modes[0].frequencies.value_si, expected_freqs)
        self.assertEqual(conformer.spin_multiplicity, 1)

        failed_log_file = TeraChemLog(os.path.join(self.data_path, 'failed_freq_job.out'))
        with self.assertRaises(LogError):
            failed_log_file.load_conformer()

    def test_load_energy(self):
        """Test loading the energy in J/mol from a TeraChem output.out or results.dat file"""
        output_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_sp_terachem_output.out'))
        results_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_sp_terachem_results.dat'))
        freq_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_freq_output.out'))
        opt_file = TeraChemLog(os.path.join(self.data_path, 'ethane_minimize_output.out'))
        e_elect_1 = output_file.load_energy()
        e_elect_2 = results_file.load_energy()
        e_elect_3 = freq_file.load_energy()
        e_elect_4 = opt_file.load_energy()
        self.assertEqual(e_elect_1, e_elect_2)
        self.assertEqual(e_elect_1, e_elect_3)
        self.assertAlmostEqual(e_elect_1, -300621953.7863082)
        self.assertAlmostEqual(e_elect_4, -206346606.4271929)

    def test_load_zero_point_energy(self):
        """Test loading the ZPE from a TeraChem freq output file"""
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethylamine_freq_output.out'))
        zpe = log_file.load_zero_point_energy()
        self.assertAlmostEqual(zpe, 243113.46765236984)

        log_file = TeraChemLog(os.path.join(self.data_path, 'formaldehyde_freq_output.out'))
        zpe = log_file.load_zero_point_energy()
        self.assertAlmostEqual(zpe, 70663.2091453692)

    def test_load_scan_energies(self):
        """Test loading a PES scan from a TeraCHem log file"""
        log_file = TeraChemLog(os.path.join(self.data_path, 'ethanol_scan_terachem_output.out'))
        v_list, angles = log_file.load_scan_energies()
        print(angles)
        expected_v_list = [3.31469351e+00, 5.61670297e+02, 2.28894412e+03, 5.02988537e+03,
                           8.06230147e+03, 1.09146826e+04, 1.31616066e+04, 1.44091777e+04,
                           1.42173813e+04, 1.28403610e+04, 1.07514495e+04, 7.96656078e+03,
                           4.81040645e+03, 2.42069223e+03, 7.90256554e+02, 4.20132486e+00,
                           4.54592173e+02, 2.06279144e+03, 4.67391931e+03, 7.62857835e+03,
                           1.04970774e+04, 1.27455046e+04, 1.42866289e+04, 1.43930501e+04,
                           1.31587081e+04, 1.10047441e+04, 8.24254519e+03, 5.10264086e+03,
                           2.56880350e+03, 7.56736797e+02, 1.30067263e+00, 5.19872864e+02,
                           2.30963595e+03, 5.02046166e+03, 7.97285489e+03, 1.06923710e+04,
                           1.29244615e+04, 1.43422341e+04, 1.43905580e+04, 1.32047110e+04,
                           1.12088126e+04, 8.31162367e+03, 5.06568695e+03, 2.54966151e+03,
                           8.50076205e+02, 0.00000000e+00, 3.31469351e+00]
        expected_angles = [0., 0.13659098, 0.27318197, 0.40977295, 0.54636394, 0.68295492,
                           0.81954591, 0.95613689, 1.09272788, 1.22931886, 1.36590985, 1.50250083,
                           1.63909182, 1.7756828, 1.91227379, 2.04886477, 2.18545576, 2.32204674,
                           2.45863773, 2.59522871, 2.7318197, 2.86841068, 3.00500167, 3.14159265,
                           3.27818364, 3.41477462, 3.55136561, 3.68795659, 3.82454758, 3.96113856,
                           4.09772955, 4.23432053, 4.37091152, 4.5075025, 4.64409349, 4.78068447,
                           4.91727546, 5.05386644, 5.19045743, 5.32704841, 5.4636394, 5.60023038,
                           5.73682137, 5.87341235, 6.01000334, 6.14659432, 6.28318531]  # radians
        np.testing.assert_almost_equal(v_list, expected_v_list, 4)
        np.testing.assert_almost_equal(angles, expected_angles)

################################################################################


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
