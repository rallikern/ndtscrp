import requests
import pandas as pd
import numpy as np
'''
Code to scrape nuclear quantities from nudat2
'''


def scraper(url):
    '''
    From url to dataframe
    
    '''
    req = requests.get(url)
    html = req.text
    df = pd.read_html(html)
    return df

##
#Get the acronym for all chemical elements
##
main_url = "https://en.wikipedia.org/wiki/List_of_chemical_elements"
df_elements = scraper(main_url)
elements = df_elements[0].take([1], axis=1)
elements = [j for i, j in enumerate(elements.iloc[:,0]) if i<118]

#capitalie the acronyms from He -> HE

for i, j in enumerate(elements):
    try:
        elements[i] = j[0]+j[1].capitalize()
    except:
        None
print('All elements are loaded!')

def unit_conv(from_unit, to_unit):
    '''
    Converts a time quantity in from_unit to to_unit
    '''
    unit_string = ["s","ms","µS","ns","ps","fs","as"]
    for i, j in enumerate(unit_string):
        if j == from_unit:
            from_fac = 10**(-i*3)
        if j == to_unit:
            to_fac = 10**(-i*3)
    return from_fac/to_fac


def nuclear_quantity(spin, parity, N_interval, Z_interval, parameter="Energy", half_life_unit="ps", number=0):
    '''
    Scrapes nuclear quantites (energies or half lifes) from
    nudat2 inside a interval of neutron and proton numbers for a certain state, e.g. 2+_1
    '''
    spin = str(spin)
    parity = str(parity)
    new_elements = elements[Z_interval[0]-1:Z_interval[1]]
    nucl_quant = []
    #
    for i in range(N_interval[0], N_interval[1]+1):
        for k, j in enumerate(new_elements):
            if (i % 2) == 0 and ((k+Z_interval[0]-1) % 2) == 1:
                isotope = str(i+k+Z_interval[0]) + j
                url = "https://www.nndc.bnl.gov/nudat2/getdatasetClassic.jsp?nucleus="+isotope+"&unc=nds"
                try:
                    df = scraper(url)
                    spins = df[2][2]
                    states = [i for i,j in enumerate(spins[:-1]) 
                              if j == spin+parity or j == "("+spin+")"+parity 
                              or j == "("+spin+parity+")"]
                    min_2 = states[number]
                    if parameter == "Energy":
                        energy = df[2][0][min_2]
                        space = energy.find(' ')
                        point = energy.find('.')
                        quant = [float(energy[0:space]),
                                  float(energy[space+1:])/10**(space-point-1)]
                    elif parameter == "Half-life":
                        life = df[2][3][min_2]
                        space1 = life.find(' ')
                        space2 = life.find(' ', space1+1)
                        point1 = life.find('.')
                        from_unit = life[space1+1:space2]
                        to_unit = half_life_unit
                        conv = unit_conv(from_unit, to_unit)
                        quant = [float(life[:space1])*conv,
                                  conv*float(life[space2+1:])/10**(space1-point1-1),
                                  to_unit]
                    nucl_quant.append([isotope, k+Z_interval[0], i, quant])
                except:
                    None
    return nucl_quant