'''Version 0.4'''

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    people = []
    category = ...
    sub_category = ...
    sub_sub_category = ...
    sub_sub_sub_category = ...
    if category == "tv_show":


        
        if sub_category == "best television limited series, anthology series, or motion picture made for television":
            people.append(sub_category)
        elif sub_category == "best television series":
            if sub_sub_category == "musical or comedy":
                people.append(sub_category + " - " + sub_sub_category)
            elif sub_sub_category == "drama":
                people.append(sub_category + " - " + sub_sub_category)

     

   
     

            

    elif category == "people":




        if sub_category == "best director - motion picture":
            people.append(sub_category)

        elif sub_category == "best performance":
            if sub_sub_category =="by an actor":
                if sub_sub_sub_category == "in a suporting role in a series, limited series, or motion picture made for":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a limited series, anthology series, or a motion picture made for":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a television series - musical or comedy":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a television series - drama":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a supporting role in any motion picture":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a supporting role in any motion picture":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a motion picture - musical or comedy":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a motion picture - drama":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
            elif sub_sub_category == "by an actress":
                if sub_sub_sub_category == "in a suporting role in a series, limited series, or motion picture made for":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a limited series, anthology series, or a motion picture made for":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a television series - musical or comedy":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a television series - drama":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a supporting role in any motion picture":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a supporting role in any motion picture":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a motion picture - musical or comedy":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)
                if sub_sub_sub_category == "in a motion picture - drama":
                    people.append(sub_category + sub_sub_category + sub_sub_sub_category)

    elif category == "film":
       
     
        if sub_category == "best motion picture - drama":
            people.append(sub_category)
     

        elif sub_category == "best motion picture":
            if sub_sub_category == "non-english language":
                people.append(sub_category + " - " + sub_sub_category)
            elif sub_sub_category == "animated":
                people.append(sub_category + " - " + sub_sub_category)
            elif sub_sub_category == "musical or comedy":
                people.append(sub_category + " - " + sub_sub_category)

        elif sub_category == "best screenplay - motion picture":
            people.append(sub_category)
   
    elif category == "song":
        if sub_category == "best original song - motion picture":
            people.append(sub_category)
      

    
        elif sub_category == "best original score":
            people.append(sub_category)
      

       
    return people

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    main()
