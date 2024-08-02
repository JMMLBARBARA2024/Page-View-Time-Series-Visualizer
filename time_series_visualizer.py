import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
# from sympy.printing.pretty.pretty_symbology import line_width

register_matplotlib_converters()

## Import data (Make sure to parse dates. Consider setting index column to 'date'.) ##
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates = ["date"], index_col = "date")

## Clean data ##
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

#**********************************************************************************************#
def draw_line_plot():
    ## Draw line plot ##
    fig, ax = plt.subplots(figsize = (13, 4))
    ax.plot(df.index, df["value"], color = (0.84, 0.15, 0.25), linewidth = 1.2)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontdict = {"size": 10})
    ax.set_xlabel("Date", fontdict = {"size": 8.5})
    ax.set_ylabel("Page Views", fontdict = {"size": 8.})
    plt.xticks(fontsize = 8.5)
    plt.yticks(fontsize = 8.5)

    ## Save image and return fig (don't change this part) ##
    fig.savefig('line_plot.png')
    return fig
#**********************************************************************************************#

#**********************************************************************************************#
def draw_bar_plot():
    ## Copy and modify data for monthly bar plot ##
    df["month"] = df.index.month
    df["year"] = df.index.year
    df_bar = df.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    ## Draw bar plot ##
    fig = df_bar.plot.bar(legend = True, figsize = (6.8, 6)).figure

    plt.legend(["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"],
               title = "Months", fontsize = 8.8)

    plt.xlabel("Years", fontdict = {"size": 9.0})
    plt.ylabel("Average Page Views", fontdict = {"size": 9.0})
    plt.xticks(fontsize = 8.7)
    plt.yticks(fontsize = 8.7)

    ## Save image and return fig (don't change this part) ##
    fig.savefig('bar_plot.png')
    return fig
#**********************************************************************************************#

#**********************************************************************************************#
def draw_box_plot():
    ## Prepare data for box plots ##
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    ## Add month number to sort the data ##
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    ## Configure outliers ##
    flierprops = dict(marker = 'o', markersize = 2, linestyle = 'none', markeredgecolor = 'lightgray')

    ## Draw the box plots using Seaborn ##
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 6))

    sns.boxplot(x = 'year', y = 'value', data = df_box, ax = axes[0], linewidth = 0.5, flierprops = flierprops)
    sns.boxplot(x = 'month', y = 'value', data = df_box, ax = axes[1], linewidth = 0.5, flierprops = flierprops)

    ## Adjust axes and titles with adjusted font size and color ##
    title_fontsize = 10
    label_fontsize = 8
    title_color = (0.27, 0.27, 0.27)
    label_color = (0.27, 0.27, 0.27)

    axes[0].set_title("Year-wise Box Plot (Trend)", fontsize = title_fontsize, color = title_color)
    axes[0].set_xlabel("Year", fontsize = label_fontsize, color = label_color)
    axes[0].set_ylabel("Page Views", fontsize = label_fontsize, color = label_color)

    axes[1].set_title("Month-wise Box Plot (Seasonality)", fontsize = title_fontsize, color = title_color)
    axes[1].set_xlabel("Month", fontsize = label_fontsize, color = label_color)
    axes[1].set_ylabel("Page Views", fontsize = label_fontsize, color = label_color)

    ## Adjust axis limits and ticks ##
    axes[0].set_ylim(0, 200000)
    axes[1].set_ylim(0, 200000)

    ## Adjusting y-axis ticks values ##
    yticks = [0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000]

    ## Adjust xticks and yticks font size ##
    plt.setp(axes[0].xaxis.get_majorticklabels(), fontsize = 8)
    plt.setp(axes[0].yaxis.get_majorticklabels(), fontsize = 8)

    plt.setp(axes[1].xaxis.get_majorticklabels(), fontsize = 8)
    plt.setp(axes[1].yaxis.get_majorticklabels(), fontsize = 8)

    axes[0].set_yticks(yticks)
    axes[1].set_yticks(yticks)

    ## Make tick lines thinner ##
    for ax in axes:
        ax.tick_params(axis='both', which='both', width = 0.2)

    ## Adjusting y-axis ticks to match the second image ##
    plt.subplots_adjust(wspace = 0.2)

    ## Adjust line visibility to be thinner ##
    for ax in axes:
        for line in ax.get_lines():
            line.set_linewidth(0.5)

    ## Save the image and return the figure ##
    fig.savefig('box_plot.png')
    return fig
#**********************************************************************************************#
