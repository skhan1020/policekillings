import pandas as pd
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.text import Annotation
import seaborn as sns

# Set Style
sns.set_style('white')

# Read in Sheet 1 from Excel File
df1 = pd.read_excel('MPVDatasetDownload.xlsx', '2013-2018 Police Killings')


# Relationship between Frequency of Casualties in Police Shootings and Race (2013 - 2018)

df2 = df1[["Victim's name","Victim's race"]]
df2 = df2.set_index("Victim's race")
df2 = df2.groupby(level=0)["Victim's name"].count().drop_duplicates()
Avg = np.average(df2.values)

# Bar Plot of Number of Casualties versus Race. Interactive feature allows the user
# to select a particular frequency value ( y -axis) which changes the colors of the bars accordingly. 
# If the bar is above (below) the selected value, bar color is red (blue) and white if it is exactly equal.

class Event:
    def __init__(self, df, y):
        
        self.df = df
        diff = y - df.values
        if diff.max() < 0:
            shade = diff.abs()/diff.min()
        else:
            shade = diff/diff.max()
        reds = cm.Reds
        blues = cm.Blues
        color = ['white' if x == 0 else reds(abs(x)) if x < 0 else blues(abs(x)) for x in shade]
        
        self.fig = plt.figure(figsize = (20,12))
        self.ax = self.fig.add_subplot(1,1,1)
        xvals = list(range(len(df)))
        self.bars = self.ax.bar(xvals, df.values, color = color, capsize = 15, picker = 5)
        plt.xticks(xvals, df.index, fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.tick_params(top = 'off', bottom = 'off', labelbottom = 'on')
        plt.title('Police Killings (2013 - 2018) versus Victim Race', fontsize = 25)
        
        
        
        plt.gcf().canvas.mpl_connect('pick_event', self.onpick)
        
    def onpick(self, event):
        
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata
        
        try:    
            self.line.set_ydata(y)
        except:
            self.line = self.ax.axhline(y=y, color = 'black')
            
        newdiff = y - df2.values
        if newdiff.max() < 0:
            newshade = newdiff.abs()/newdiff.min()
        else:
            newshade = newdiff/newdiff.max()
        reds= cm.Reds
        blues = cm.Blues
        newcolor = ['white' if a == 0 else reds(abs(a)) if a < 0 else blues(abs(a)) for a in newshade]
        
             
        for bar, col in zip(self.bars, newcolor):
            bar.set_facecolor(col)

        self.fig.canvas.draw()
        
        
p = Event(df2,Avg)
plt.show()

## Reading in Sheet 2 of the Excel File

df1 = pd.read_excel('MPVDatasetDownload.xlsx', '2013-2017 Killings by PD')

# Test how often are black people killed as opposed to people 
# from other communities across all the states in the US

df3 = df1[['State', 'All People Killed by Police (1/1/2013-12/31/2017)', 'Black People Killed by Police (1/1/2013-12/31/2017)']].dropna()
df3 = df3.set_index('State')
df3 = df3.rename(columns={'All People Killed by Police (1/1/2013-12/31/2017)': 'Total', 'Black People Killed by Police (1/1/2013-12/31/2017)': 'Black'})

d = {'Total':'Sum1', 'Black':'Sum2'}
df3 = df3.groupby(level = 0).agg({'Total':'sum', 'Black':'sum'}).rename(columns=d)
df3 = df3.drop(['United States'])


# Bar plot of Number of black people killed and total number of people killed in the different states of US (2013 - 2017)

ind = np.arange(len(df3))
width = 0.4

fig = plt.figure(figsize = (20, 25))
ax = fig.add_subplot(1,1,1)

ax.barh(ind, df3.Sum1, width, color='red', label='Total killed by Police', alpha = 0.5)
ax.barh(ind + width, df3.Sum2, width, color='green', label='Black People killed by Police', alpha = 0.5)

ax.set(yticks=ind + width, yticklabels=df3.index, ylim=[2*width - 1, len(df3)])

plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
ax.legend()

plt.show()

# Relationship between Violent Crime Rate and Murder Rate in the US (2013 - 2017)

df4 = df1[['State', 'Violent Crime Rate', 'Murder Rate']].dropna()
df4 = df4.set_index('State')

d = {'Violent Crime Rate' : 'VC', 'Murder Rate': 'MR'}
df4 = df4.groupby(level=0).agg({'Violent Crime Rate' : 'sum', 'Murder Rate' : 'sum'}).rename(columns = d)
df4 = df4.drop(['United States'])
df4['size'] = df4['VC']/df4['MR']

# labels for each state 
labels = df4.index


# Scatter plot of Violent Crime Rate (x-axis) and Murder Rate (y-axis) across the different states. 
# State names appear next to the data point by clicking on the chosen data point with mouse

fig = plt.figure(figsize = (12, 9))
ax = plt.subplot()
cm = plt.cm.get_cmap('RdYlBu')
sc = ax.scatter(x = df4['VC'].values, y = df4['MR'].values, s = 50, c = df4['size'].values, cmap = cm, picker = True)
plt.colorbar(sc)
plt.title('Murder Rate versus Violent Crime Rate in US states (2013 - 2017)',fontsize = 15, y = 1.0)
plt.xlabel('Violent Crime Rate', fontsize = 15, labelpad = 20)
plt.ylabel('Murder Rate', fontsize = 15, labelpad = 20)
plt.grid(axis = 'y', color ='gray', linestyle = '--', linewidth = 2, alpha = 0.25)
plt.box(on = None)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)

# Annotation : Generate text labels for each data point 
def annotate(axis, text, x, y):
    
    text_annotation = Annotation(text, xy = (x,y), xycoords = 'data')
    axis.add_artist(text_annotation)

# Interactive feature 
def onpick(event):

    # Locate the index of the data point
    ind = event.ind
    
    # Gather the x and y coordinates on clicking for positioning the text label
    xpos = event.mouseevent.xdata
    ypos = event.mouseevent.ydata
    
    # offset prevents overlapping of text labels
    offset = 0
    
    # Assigning labels on the plot to each data point
    for i in ind:
        
        label = labels[i]
 
        annotate(ax, label, xpos + offset, ypos + offset)

        ax.figure.canvas.draw()
        
        offset += 1.0

fig.canvas.mpl_connect('pick_event', onpick)
plt.show()

# Seaborn Jointplot of Violent Crime Rate and Murder Rate
# Probability Density of the two variables are plotted along with a Contour Plot

plt.figure(figsize = (15, 15))
h = sns.jointplot(df4.VC.values, df4.MR.values, kind = 'kde', space = 0, alpha = 0.4)
h.set_axis_labels('Violent Crime Rate', 'Murder Rate', fontsize=15)
h.fig.suptitle('Violent Crime Rate versus Murder Rate', y = 1.0,fontsize = 15)
plt.show()
