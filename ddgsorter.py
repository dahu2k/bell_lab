"""
Module: dggsorter

program for sorting DDG Data

Author:
Diego Hernandez
"""

import matplotlib.pyplot as ppl

def txt_to_csv(filename_in, filename_out):
    """
        Formats .txt file of DDG Data to .csv file.
        Parameters:
        filename_in (type: string): filename of txt file with DDG data (must 
        end in .txt).
        filename_out (type: string): filename of the new csv file (must end in 
        .csv).
        Returns:
        None
    """
    infile = open(filename_in, 'r')
    outfile = open(filename_out, 'w')

    # Makes the first line the header
    header = infile.readline()
    outfile.write('#chain,WT,ResID,Mut,ddG_(kcal/mol;_>0_is_stable;_<0 is unstable)\n')

    for line in infile:
        res_temp = line.split(' ')
        res_string = ''
        for i in res_temp:
            if i != '':
                res_string += i + ','
        outfile.write(res_string[:-1])

    return None

def ddg_x_res_y(filename):
    """
    Makes a list from ddg data in .csv file and returns residue # as x value and ddg
    as y value.
    Parameters:
    filename (type: string): name of .csv file with ddg data
    Returns:
    res_x (type: list with int): list of residue numbers
    ddg_y (type: list with int): list of ddg values
    """


    ddg_data_file = open(filename, 'r', encoding="utf-8")

    ddg_data_file.readline()
    res_x = []
    ddg_y = []
    for line in ddg_data_file:
        val = line.split(",")
        res_x.append(float(val[2]))
        ddg_y.append(float(val[4]))

    return (res_x, ddg_y) # Returns a tuple of residue numbers and ddg values

def plot_ddg_vs_res(filename):
    """
    Plots ddg data on the y axis according to its residue on the x axis.
    Parameters:
    filename (type: string): name of .csv file with ddg data
    Returns:
    None
    """

    x_val, y_val = ddg_x_res_y(filename)
    ppl.scatter(x_val, y_val)
    ppl.show()
    

    return None

def main():
    choice = int(input('what do you want to do?\n1) convert .txt of ddg data to .csv\n2) plot .ddg data from .csv\nChoose by inputing interger: '))
    if choice == 1:
        filename_in = input('filename_in: ')
        filename_out = input('filename out: ')
        txt_to_csv(filename_in, filename_out)
    if choice == 2:
        filename = input('filename: ')
        plot_ddg_vs_res(filename)
if __name__ == "__main__":
    main()