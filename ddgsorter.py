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

def plot_ddgavg_vs_res(filename):
    """
    Plots average ddg on the y axis according to its residue on the x axis.
    Parameters:
    filename (type: string): name of .csv file with ddg data
    Returns:
    None
    """
    x_val, y_val = res_avg(filename)
    ppl.scatter(x_val, y_val)
    ppl.show()

    return None

def largest_val(list_val):
    """
    Returns largest value from a list
    Parameters:
    list_val (type: list with int): list of values
    Returns:
    lar_val (type: int or float): largest value from a list
    """
    lar_val = list_val[0]
    for val in list_val:
        if val > lar_val:
            lar_val = val
    return lar_val

def calc_avg(list_val):
    """
    Returns average value from a list of values
    Parameters:
    list_val (type: list with int): list of values
    Returns:
    avg (type: float): average from list of values
    """
    sum_val = 0
    count_val = 0
    for val in list_val:
        sum_val += val
        count_val += 1
    avg = float(sum_val / count_val)

    return avg

def res_avg(filename):
    """
    Obtains the average ddg for each residue.
    Parameters:
    filename (type: string): .csv file with ddg data
    Returns:
    residue (type: list with intergers):
    ddg_average (type: list with intergers): 
    """

    # Obtains data on residue and ddg from file
    res, ddg = ddg_x_res_y(filename)
    
    # Create list with empty list for each residue
    lar_val = int(largest_val(res))
    list_res = []
    for i in range(lar_val):
        mt = []
        list_res.append(mt)
    # Puts values in list
    res_len = len(res)
    for i in range(res_len):
        list_res[int(res[i]) - 1].append(ddg[i])
    # Calculates average for each point
    residue = []
    ddg_average = []
    for i in range(lar_val):
        residue.append(i + 1)
        ddg_average.append(calc_avg(list_res[i]))

    return residue, ddg_average

def main():
    choice = int(input('what do you want to do?\n1) convert .txt of ddg data to .csv\n2) plot ddg data from .csv\n3) plot average ddg data from .csv\nChoose by inputing interger: '))
    if choice == 1:
        filename_in = input('filename_in: ')
        filename_out = input('filename out: ')
        txt_to_csv(filename_in, filename_out)
    if choice == 2:
        filename = input('filename: ')
        plot_ddg_vs_res(filename)
    if choice == 3:
        filename = input('filename: ')
        plot_ddgavg_vs_res(filename)
if __name__ == "__main__":
    main()