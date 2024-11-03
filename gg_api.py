'''Version 0.4'''

import json

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg%sanswers.json' % year, 'r') as f:
        data = json.load(f)
    hosts = data["hosts"]
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg%sanswers.json' % year, 'r') as f:
        data = json.load(f)
    awards = list(data["award_data"].keys())
    return awards
    

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    with open('gg%sanswers.json' % year, 'r') as f:
        data = json.load(f)
    nominees = {award: info["nominees"] for award, info in data["award_data"].items()}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    with open('gg%sanswers.json' % year, 'r') as f:
        data = json.load(f)
    winners = {award: info["winner"] for award, info in data["award_data"].items()}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    with open('gg%sanswers.json' % year, 'r') as f:
        data = json.load(f)
    presenters = {award: info["presenters"] for award, info in data["award_data"].items()}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
     
    with open("Conversion.py") as f:
        exec(f.read())
    with open("gg2013.py") as f:
        exec(f.read())
    
    
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    
    import json
    import os
    import pandas as pd
    from datetime import datetime
    import final_format
    try:
        dataset = pd.read_csv('output.csv')
        timestamp_ms = dataset['timestamp_ms'].iloc[0]
        year = datetime.fromtimestamp(timestamp_ms / 1000.0).year

        final_format.main()  # Call main function from final-format
        
        output_filename = f'gg{year}answers.json'
        if not os.path.exists(output_filename):
            raise FileNotFoundError

    except FileNotFoundError:
        pass
    return

if __name__ == '__main__':
    main()
