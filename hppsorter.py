"""
Module: hppsorter

program for sorting H++ Data

Author:
Diego Hernandez
"""

def txt_to_csv(filename_in, filename_out):
    """
    Formats .txt file of H++ Data to .csv file. Formatted .csv file will
    look like this...
        Residue,pKint,pK_(1/2)
        NTMET-1,7.208,7.715
        LYS-3,10.176,>12.000
        GLU-18,4.965,4.857
        …
        LYS-313,6.729,8.107
        CTLYS-313,4.524,1.716
    Parameters:
    filename_in (type: string): filename of txt file with H++ data (must 
    end in .txt).
    filename_out (type: string): filename of the new csv file (must end in 
    .csv).
    Returns:
    None
    """
    
    infile = open(filename_in, 'r')
    outfile = open(filename_out, 'w')

    # Makes the first line the protein name
    protein_name = filename_out.split('.')
    protein_name = protein_name[0]
    outfile.write(',' + protein_name +',' + '\n')
    # Makes the second line the header
    header = infile.readline()
    outfile.write('Residue,pKint,pK_(1/2)\n')

    ntmet = False
    ntmet_count = 0
    while ntmet != True:
        line = infile.readline()
        res_temp = line.split(' ')
        res_string = ''
        icount = 0
        for i in res_temp:
            if i != '' and icount < 2:
                res_string += i + ','
                icount += 1
            elif i != '':
                res_string += i
            # Signals end of file (ends while loop) by checking if NTMET-1 
            # appears twice in document
            if i == 'NTMET-1':
                ntmet_count += 1
                if ntmet_count > 1:
                    ntmet = True
        if ntmet != True:
            outfile.write(res_string)

    infile.close()
    outfile.close()

    return None

def convert_filenames_to_list(filenames):
    """
    Converts a string of filenames to a list of filenames.
    Parameters:
    filenames (type: string): names of files, separated by commas, so they
    may be converted into a list
    Returns:
    nl (type: list): list of separated filenames.
    """
    # Convert "filenames" to string without spaces
    ns = ""
    for i in filenames:
        if i != " ":
            ns += i
    #splits string into list
    nl = ns.split(',')
    return nl

def convert_all_csv_and_largest_residue(fn_in, fn_out):
    """
    Converts multiple .txt files into .csv files, and returns the largest 
    residue number.
    Parameters:
    fn_in (type: list): list of (string) names of .txt files that will be 
    converted.
    fn_out (type: list): list of (string) names of new .csv files
    Returns:
    largest_residue (type: int): largest residue number in all files.
    """

    # Connverts each filename to .csv file
    fn_out_names = [] # Stores list of opened file names
    largest_residue = 0 # Stores largest residue
    for i in range(len(fn_in)):
        # Converts to .csv and opens each filename
        p_name = "file" + str(i)
        fn_out_names.append(p_name)
        txt_to_csv(fn_in[i], fn_out[i])
        fn_out_names[i] = open(fn_out[i], 'r')
        # Gets largest residue # from all the files
        f_find_largest = fn_out_names[i]
        for line in f_find_largest:
            vals = line.split(',')
            res_str = ''
            for j in vals[0]:
                if j in "0123456789":
                    res_str += j
                    if res_str != '':
                        res_int = int(res_str)
                    else:
                        res_int = 0
                    if res_int > largest_residue:
                        largest_residue = res_int
        fn_out_names[i].close()

    return largest_residue

def csv_align(filenames_in, filenames_out, filename_out):
    """
    Aligns multiple .csv files (as formatted by txt_to_csv function) with 
    H++ data according to residue number.
    Parameters:
    filenames_in (type: string):
    filenames_out (type: string): multiple .csv filenames. (eg. "filename_1.csv, 
    filename_2.csv, ..., filename_n.csv").
    filename_out ():
    Returns:
    None
    """

    # Converts string to list
    fn_in = convert_filenames_to_list(filenames_in)
    fn_out = convert_filenames_to_list(filenames_out)

    aligned_csv = open(filename_out, 'w')

    # Connverts each filename to .csv file and finds largest residue
    largest_residue = convert_all_csv_and_largest_residue(fn_in, fn_out)
    
    fn_out_len = len(fn_out)
    # Makes list for every line (2 lines for headers and line for each residue)
    res_list = []
    for i in range(largest_residue + 2):
        # Makes list of tuples, where the # of tuples is the same as the # of files
        list_tup_mt = [('', '', '')] * fn_out_len # "" will be used to check if all the tuples in list contain only "", then don't add to file

        res_list.append(list_tup_mt)
    
    fn_out_names = []
    for i in range(fn_out_len):
        #Opens each file
        p_name = "file" + str(i)
        fn_out_names.append(p_name)
        fn_out_names[i] = open(fn_out[i], 'r')
        f_open = fn_out_names[i]
        #Put headers in list
        header1 = f_open.readline()
        header1_vals = header1.split(',')
        header1_tup = []
        for x in header1_vals:
            header1_tup.append(x)
        header2 = f_open.readline()
        header2_vals = header2.split(',')
        header2_tup = []
        for x in header2_vals:
            header2_tup.append(x)
        res_list[0][i] = header1_tup
        res_list[1][i] = header2_tup
        #Put rest of file in list
        for line in f_open:
            vals = line.split(',')
            vals_tup = []
            # Makes tuple of vals
            for j in vals:
                vals_tup.append(j)
            # Find residue number
            residue = vals[0]
            res_num_str = ''
            for k in residue:
                if k in "0123456789":
                    res_num_str += k
            res_num = int(res_num_str)
            res_list[res_num + 1][i] = vals_tup
        f_open.close()

    # Write list into aligned file
    # Make string for each line
    for i in range(len(res_list)):
        line_str = ''
        res_list_1 = res_list[i]
        for j in range(len(res_list_1)):
            res_list_2 = res_list_1[j]
            for k in range(len(res_list_2)): # Need to remove \n from string and need to add commas
                if '\n' in res_list_2[k]: #removes \n from string
                    res_list_3 = res_list_2[k][:-1]
                else:
                    res_list_3 = res_list_2[k]
                line_str += res_list_3 + ','
        
        if line_str != ',,,' * fn_out_len:
            aligned_csv.write(line_str[:-1] + '\n')  

    aligned_csv.close()
    
    return res_list

def main():
    choose_function = int(input('What would you like to do? (type interger)\n1) convert H++ .txt to .csv\n2) align H++ files (.txt or .csv)\n Type interger: '))
    if choose_function == 1:
        filename_in = input('What is the name of the file to be modified: ')
        filename_out = input ('What is the name of the new file: ')

        txt_to_csv(filename_in, filename_out)
    elif choose_function == 2:
        filenames_in = input('What are the names of the files to be modified? \n(separate each filename with a comma, spaces do not matter): ')
        filenames_out = input('What are the names of the new .csv files: ')
        filename_out = input('What is the name of the new aligned file? \n(must end in .csv): ')

        csv_align(filenames_in, filenames_out, filename_out)
    return None

if __name__ == "__main__":
    main()