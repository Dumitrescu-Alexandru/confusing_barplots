# HW 3

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 350


data_folder = "/home/alex/Downloads/emission_data/"


def get_data(name ="hfc.xml" ):
    country_to_emissions_by_timeperiod = {"France":[], "Germany":[], "Canada":[], "Japan":[]}
    with open(data_folder + name) as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    year_tags = Bs_data.find_all('field', attrs={'name':"Year"})
    country_tags = Bs_data.find_all('field', attrs={'name':"Country or Area"})
    value_tages = Bs_data.find_all('field', attrs={'name':"Value"})

    five_yr_sum = 0
    for year, country, value in zip(year_tags, country_tags, value_tages):
        if int(year.text)> 2015:
            continue
        else:
            if int(year.text) % 5 == 0 and int(year.text) != 2015:
                country_to_emissions_by_timeperiod[country.text].append(five_yr_sum)
                five_yr_sum = 0
            else:
                five_yr_sum += float(value.text)
    return country_to_emissions_by_timeperiod
gas_type_emissions = {"hfc":get_data("hfc.xml"), "pfc":get_data("pfc.xml"), "nf3":get_data("nf3.xml")}

top_bars, bottom_bars = {0:[], 1:[], 2:[],3:[],4:[]}, {0:[],1:[],2:[],3:[],4:[]}
labels = []
for index, gas_type in enumerate(['hfc','pfc','nf3']):
    for country in ['France', 'Germany', 'Canada', 'Japan']:
        for i in range(5):
            top_bars[i].append(sum(gas_type_emissions[gas_type][country][i:]))
            bottom_bars[i].append(sum(gas_type_emissions[gas_type][country][i+1:]))
        labels.append(gas_type+"\n"+country)


year_periods = ["2010-2015", "2005-2010", "2000-2005", "1995-2000", "1990-1995"]
for i in range(5):
    plt.bar(labels, top_bars[i], width=0.3, label=year_periods[i], bottom=bottom_bars[i])
plt.xticks(fontsize=6)
plt.ylabel(r"Equivalent CO$_2$ tonnes", fontsize=6)
# plt.savefig("cumulative_gas_emissions_plot.pdf")
plt.yscale("log")
plt.show()
plt.close()
yticks, yticklbls = [[200000, 400000, 600000, 800000],[100000, 200000, 300000],[5000, 10000,15000, 20000]], [["200k","400k","600k","800k"],["100k","200k","300k"],["5k","10k","15k","20k"]]

fig, axs = plt.subplots(1, 3)
for ind,gt in enumerate(['hfc','pfc','nf3']):
    for i in range(5):
        if ind == 0:
            axs[ind].bar(['Fr', 'De', 'Ca', 'Jp'], top_bars[i][ind*4:(ind+1)*4], width=0.3, label=year_periods[i], bottom=bottom_bars[i][ind*4:(ind+1)*4])
        else:
            axs[ind].bar(['Fr', 'De', 'Ca', 'Jp'], top_bars[i][ind*4:(ind+1)*4], width=0.3, bottom=bottom_bars[i][ind*4:(ind+1)*4])
        axs[ind].set_title(gt)
        axs[ind].set_yticks(yticks[ind])
        axs[ind].set_yticklabels(yticklbls[ind])
fig.tight_layout(pad=3.5)
fig.text(0.02, 0.5, r"Equivalent CO$_2$ tonnes", va='center', rotation='vertical')
plt.show()



# with open(data_folder+'hfc.xml', 'r') as f:
# with open(data_folder + 'pfc.xml', 'r') as f:
# with open(data_folder+'nf3.xml', 'r') as f: