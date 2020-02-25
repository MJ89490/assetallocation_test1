# from .times import format_data_and_calc
# from assetallocation_arp.arp_strategies import write_output_to_excel

"""
Created on Fri Nov  15 17:27:51 2019
CURP
@author: JL89005
"""

import pandas as pd
import numpy as np

def run_model():


def import_data_IR():
    # import interest rate data
    # 1st part: Bloomberg carry tab

def import_data_returns():
    # import carry adjusted returns
    # 2nd part, Bloomberg RET tab

def import_inputs();
    # import input data from the model run settings

def prepare_IR_data():
    # calculate the IR differentials
    # For the IR differentials, first generate 2 matrices. TThe first is the IR for the 1st currency in the pair, the second is the IR for the second

    # now simply subtract the second matrix from the first

def prepare_XS_returns_index():
    # simply generate the indexed returns
    # this is the XSReturnsRET tab

def define_input_parameters_globally():
    # This data comes from the import of data in import_inputs
    # make sure stuff is defined globally!

def valuation_tab():
    # this is the valuation tab
    # here, will need to use the global variables 'window' and 'historical level averaging'

def calculate_signals():
    # calculate the signals, using the formula: IR differential -((1+valuation)^(window/12)-1)*DynHedgeMeanReversion

    # There are then some additional steps to do in the tables to the right

    # the first does a look up on the parameters to know how to round the signal to a more round number

    # the second then adds up the values of the longs and subtracts the value of the shorts

def generate_graph_one_data():
    # just need to take the final row of the matrix from signals, then sort

def generate_graph_two_data():
    # need to figure this out