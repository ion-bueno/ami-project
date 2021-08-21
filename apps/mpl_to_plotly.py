
import plotly.tools as tls
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def get_plotly_figure(mpl_axes, costum_xlabels=False):
    mpl_axes.get_legend().remove()
    fig = mpl_axes.get_figure()
    #fig.set_dpi(1000)
    fig.tight_layout()
    #fig.set_size_inches(12.8*2, 9.6*2, forward=True)
    x_labels = [tick.get_text() for tick in mpl_axes.get_xticklabels()[1:-1]]
    x_positions = [pos for pos in mpl_axes.get_xticks()[1:-1]]
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_legend = go.layout.Legend()
    if costum_xlabels:
        plotly_fig.update_xaxes(rangeslider_visible=True, tickvals=x_positions, ticktext=x_labels)
    else:
        plotly_fig.update_xaxes(rangeslider_visible=True)
    plotly_fig.update_layout(title={'x': 0.5, 'xanchor': 'center', 'yanchor':'top'}, showlegend=True, legend=plotly_legend,
                             autosize=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             width=768, height=576)
    return plotly_fig
