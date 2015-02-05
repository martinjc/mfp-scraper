import csv
import sys
import os
from datetime import datetime

import matplotlib as mpl
mpl.use( 'Agg' )
mpl.rc( 'font', **{ 'sans-serif':'Helvetica', 'family':'sans-serif', 'size':12.0} )   # all fonts are set relative to this
mpl.rc( 'legend', fontsize='medium' )  # i.e., normal
mpl.rc( 'axes', **{'titlesize':'medium'} )

from matplotlib import dates
from matplotlib import pyplot as plt
from matplotlib import colors

import numpy as np

colours = ['b','g','r','c','m','y','k', 'g']
markers = ['s', 'o', '^', 'd', 'h', '+', 'x']

def generate_plots(username):

    # work out where we're reading .csv files from
    cwd = os.getcwd()
    csv_dir = os.path.join(username, 'csv')
    csv_path = os.path.join(cwd, csv_dir)

    # work out where we're writing files to
    plot_dir = os.path.join(username, 'plot')
    plot_path = os.path.join(cwd, plot_dir)

    # generate line plots of food intake
    rdr = csv.reader(open(os.path.join(csv_path, 'food_totals.csv'), 'rU'))

    # two lines of headers
    rdr.next()
    rdr.next()

    titles = ['Calories','Carbs','Fat','Protein','Sugar']

    total = {}
    goal = {}
    remaining = {}

    for title in titles:
        total[title] = []
        goal[title] = []
        remaining[title] = []
    
    x_labels = []

    for row in rdr:
        date = datetime.strptime(row[0], '%Y-%m-%d')
        x_labels.append(date)
        index = 1
        for title in titles:
            total[title].append(row[index])
            goal[title].append(row[index+1])
            remaining[title].append(row[index+2])
            index += 3
    x_labels = dates.date2num(x_labels)

    for title in titles:
        plt.hold(True)
        fig = plt.figure(figsize=[16,6])

        print(x_labels)
        print(total[title])

        plt.plot_date(x_labels, total[title], fmt='-', label='Total', marker='*', color=colours[0] )
        # calculate the trend line and plot
        z = np.polyfit(x_labels, [int(y) for y in total[title]], 1)
        p = np.poly1d(z)
        plt.plot_date(x_labels, p(x_labels), 'r--', color=colours[0])

        plt.plot_date(x_labels, goal[title], fmt='-', label='Goal', marker='s', color=colours[1] )
        # calculate the trend line and plot
        z = np.polyfit(x_labels, [int(y) for y in goal[title]], 1)
        p = np.poly1d(z)
        plt.plot_date(x_labels, p(x_labels), 'r--', color=colours[1])

        plt.plot_date(x_labels, remaining[title], fmt='-', label='Remaining', marker='o', color=colours[2] )
        # calculate the trend line and plot
        z = np.polyfit(x_labels, [int(y) for y in remaining[title]], 1)
        p = np.poly1d(z)
        plt.plot_date(x_labels, p(x_labels), 'r--', color=colours[2])

        plt.xlabel('Date')
        plt.ylabel(title)

        plt.title(title)

        plt.grid(b=True)
        plt.legend(loc='upper right').draw_frame(False)   

        plt.xticks(rotation=30)

        plt.hold(False)
        output_file = title + ".pdf"
        output_path = os.path.join(plot_path, output_file)
        plt.savefig( output_path, format='pdf', bbox_inches='tight' )

    for title in titles:
        plt.hold(True)
        fig = plt.figure(figsize=[10,6])

        plt.plot_date(x_labels, remaining[title], fmt='-', label='Remaining', marker='o', color=colours[2] )

        # calculate the trend line and plot
        z = np.polyfit(x_labels, [int(y) for y in remaining[title]], 1)
        p = np.poly1d(z)
        plt.plot_date(x_labels, p(x_labels), 'r--', color=colours[0])

        plt.xlabel('Date')
        plt.ylabel(title)

        plt.title('%s Remaining' % title)

        plt.grid(b=True)
        plt.legend(loc='upper right').draw_frame(False)   

        plt.xticks(rotation=30)

        plt.hold(False)
        output_file = title + "_remaining.pdf"
        output_path = os.path.join(plot_path, output_file)
        plt.savefig( output_path, format='pdf', bbox_inches='tight' )

    
    



if __name__ == '__main__':

    args = sys.argv

    # check for username and password and optional number of days to get
    if len(args) != 2:
        print "Incorrect number of arguments"
        print "Argument pattern: username "
        exit(1)

    username = args[1]

    generate_plots(username)