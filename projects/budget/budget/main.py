import pandas as pd
import re
from typing import List
from pathlib import Path
from datetime import datetime

# keys dict provide a level of abstraction that will ensure the program can easily be made compatible with other banks csv formats.
keys = {"Description" : ["Long description"], "Debit" : ["Debit amount"], "Credit" : ["Credit amount"], "Date": ["Create date"]} # if using a new bank bank with differnt csv format, add as value 
matches =  {"TFR": ["tfr from t j alder", "tfr to t j alder"], "Declined EFT":["declined eft fee", "eft declined"], "Takeout": ["subway", "sumo salad", "mcdonalds", "bakery", "sushi", "anitagelato", "zambrero", "kfc", "ice cream", "monster cupbop", "the food co-op shop", "gangnam lane", "hello harry", "tilleys", "oporto", "ballistic burrito", "kebab", "dumpling", "eatery", "pizza", "spilt milk", "malika", "grease monkey", "colosseum italian", "melted toasties", "hungry jacks", "sharetea" ,"cartel taqueria", "chong co", "two before ten", "hikari ramen", "indian", "fox & bow", "kingsleys", "29 cafe & eatery"], "Groceries": ["woolworths", "coles", "unique meats", "iga", "ziggys", "oz fish", "aldi ", "butcher", "supabarn", "bulk nutrients", "ten tops", "mikes meats"], "Icecream":["spiltmilk"], "Petrol":["ampol", "bp", "7-eleven", "petroleum", "reddy express", "metro"], "Physio":["woden integrated", "philip snare and feng"], "Doctor":["damian smith"], "Alcohol":["bws","liqourland", "hopscotch", "dollys", "one22", "austrian australian cl", "loquita", "king o malley s", "mooseheads", "civic pub", "fun time pony", "squeaky clean bar", "hotel kingston", "fiction club", "canberra north bowling", "transit bar", "thirsty camel", "bar beirut", "casino canberra", "tathra beach bowling", "pjs in the city", "clock hotel", "tathra hotel", "vault", "the duxton", "surry hills fine win", "illawong hotel", "crown hotel", "dove and olive hotel", "strawbery hills hotel"], "Dentist":[], "Exercise":["club lime","dark carnival", "swing city", "viva leisure"], "Car Bike":["super cheap","bapcor", "bingle", "techworkz", "colmatt services", "motorcycle", "motor cycle", "amx superstores", "repco", "autobarn", "stay upright", "access canb", "ama warehouse", "access cbr", "pedders", "peter holley", "auto parts"], "Bunnings":["bunnings"], "Uber":["uber"], "Subscriptions":["remarkable", "chatgpt", "aldimobile", "apple.com/bill"], "Parking":["parking"], "Games":["playstation"], "Friends": ["blandy", "nelson", "carrick", "helmers", "mclaughlin", "orr", "rea andrew"], "Family": ["sharon alder", "chloe alder"], "Retail Online Shopping": ["ebay", "aliexpress", "big w", "kmart", "officeworks", "m j bale"], "Travel": ["simsdirect", "qantas", "thai airways", "british awys", "wise", "heinemann duty free", "whsmith sydt1 pier a", "travel insurance", "uniqlo", "flixbus", "esta appl", "fast cover"], "Chemist": ["cdc dickson village", "chemist warehouse"], "Barber": ["south pac barbers"], "Tolls": ["linkt"], "Public Transport": ["transportfornsw"], "Tax": ["ato payment"], "Rent": ["christopher k alder & wendy j al account 201244", "fadden rent"], "Investing": ["superhero"], "Concerts": ["ticketmaster", "moshtix"]}
categories = list(matches.keys())


class Transaction:
    """
    This class provides a level of abstraction that will ensure the program can easily be 
    made compatible with other banks csv formats.
    """
    def __init__(self, df: pd.DataFrame):
        self.columns = {"Description": None, "Debit": None, "Date": None, "Credit": None}
        for d in keys["Description"]:
            if d in list(df.columns): self.columns["Description"] = str(d)
        for b in keys["Debit"]:
            if b in list(df.columns): self.columns["Debit"] = str(b)
        for c in keys["Credit"]:
            if c in list(df.columns): self.columns["Credit"] = str(c)
        for t in keys["Date"]:
            if t in list(df.columns): self.columns["Date"] = str(t)


    def store(self, row):
        self.description = row[self.columns["Description"]]
        self.debit = row[self.columns["Debit"]]
        self.credit = row[self.columns["Credit"]]
        self.date = row[self.columns["Date"]]
       


def categorise(description: str)->str:
    """
    This function sorts a Transaction.data["description"] attribute into a category.

    :param data: Transaction.data["description"] attribute.
    :type data: str
    :return: Identified category
    :rtype: str
    """
    
    # should figure out how to convert decsription to all lowercase so don't have to handle different capitalisation cases
    for cat in categories:
        for m in matches[cat]:
            if m in description.lower():
                return cat
    else:
        return "Unknown"
    
    
def main(fps: str | List[str], out: bool=False)-> None:
    """
    _summary_

    :param fp: filepath to .csv file containing bank statement of transactions.
    :type ƒp: str
    """
    # read in the data
    fps = list(fps)
    print(fps)
    df = pd.concat([pd.read_csv(fp) for fp in fps], ignore_index=True)
    df["Debit amount"] = df["Debit amount"].fillna(0)
    df["Credit amount"] = df["Credit amount"].fillna(0)
    df = df.fillna("")

    # first, find out what the description and balance headings are
    t = Transaction(df=df)
    # if description or balance were not found
    if None in list(t.columns.values()):
        raise Exception("Error! Unrecognised .csv structure...")
        
    
    # create a dataframe to hold all the sorted data (each category is a sheet)
    xlsx = {cat:{"Balance": [], "Description": [], "Date": []} for cat in categories} 
    xlsx["Unknown"] = {"Balance": [], "Description": [], "Date": []}
    xlsx["Total"] = {"Balance": []}
    xlsx["Income"] = {"Balance": []}

    for index, row in df.iterrows():
        t.store(row)
        cat = categorise(t.description)
        # ignore transfers between your own personal accounts
        if cat=="TFR":
            pass
        else:
            xlsx[cat]["Balance"].append(t.credit-t.debit)
            xlsx[cat]["Description"].append(t.description)
            xlsx[cat]["Date"].append(t.date)
        
    # # Add totals field
    grand_total = 0
    categories.remove("TFR")
    for cat in categories + ["Unknown"]:
        total = sum(xlsx[cat]["Balance"])
        print(cat, int(total))
        grand_total += total
        xlsx[cat]["Balance"].append(total)
        xlsx[cat]["Description"].append("Total")
        current_datetime = datetime.now()
        xlsx[cat]["Date"].append(current_datetime.strftime("%I:%M%p %a %-d %B, %Y").lower())
    # set total expense to be sum of individual category totals
    print("Total", grand_total)
    xlsx["Total"]["Balance"].append(grand_total)

    # write to xlsx if out is passed as arg
    if out:
        with pd.ExcelWriter('CATEGORISED_'+Path(fps[0]).stem+'.xlsx') as writer:
            for cat in categories:
                pd_df = pd.DataFrame(xlsx[cat])
                pd_df.to_excel(writer, sheet_name=cat, index=False) # not sure about double braces here
            for cat in ["Total", "Unknown"]: # handle special cases
                pd_df = pd.DataFrame(xlsx[cat])
                pd_df.to_excel(writer,sheet_name=cat, index=False)

    print(f"Categorisation complete! {df.size} total transactions were considered, { len(xlsx['Unknown']['Description'])} of which were unable to be categorised.")
    return xlsx


if __name__ == "__main__":
    result = main(
        [
            "/Users/timothyalder/Documents/tplat/projects/budget/docs/data/Transactions_2025-05-01_2026-04-28.csv",        
            "/Users/timothyalder/Documents/tplat/projects/budget/docs/data/Transactions_2025-05-01_2026-04-28 2.csv",
            "/Users/timothyalder/Documents/tplat/projects/budget/docs/data/Transactions_2025-05-01_2026-04-28 3.csv",
        ], 
        out=True
    )




