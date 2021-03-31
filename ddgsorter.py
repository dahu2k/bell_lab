"""
Module: dggsorter

program for sorting DDG Data

Author:
Diego Hernandez
"""

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

def main():
    filename_in = input('filename_in: ')
    filename_out = input('filename out: ')
    txt_to_csv(filename_in, filename_out)
if __name__ == "__main__":
    main()